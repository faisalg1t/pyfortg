"""Redis storage backend."""

import json
import logging
from typing import Any, Optional

from .base import BaseStorage

logger = logging.getLogger(__name__)


class RedisStorage(BaseStorage):
    """Redis-based storage backend."""
    
    def __init__(
        self,
        url: str = "redis://localhost:6379",
        db: int = 0,
        prefix: str = "pyfortg:",
    ):
        """
        Initialize Redis storage.
        
        Args:
            url: Redis connection URL
            db: Database number
            prefix: Key prefix for all operations
        """
        self.url = url
        self.db = db
        self.prefix = prefix
        self.redis = None
    
    async def _ensure_connection(self):
        """Ensure Redis connection is established."""
        if self.redis is None:
            try:
                import aioredis
                self.redis = await aioredis.from_url(self.url, db=self.db)
            except ImportError:
                raise ImportError(
                    "aioredis is required for RedisStorage. "
                    "Install it with: pip install pyfortg[redis]"
                )
    
    def _get_key(self, key: str) -> str:
        """Get prefixed key."""
        return f"{self.prefix}{key}"
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from Redis."""
        await self._ensure_connection()
        try:
            value = await self.redis.get(self._get_key(key))
            if value is None:
                return None
            # Try to decode as string, otherwise return as bytes
            if isinstance(value, bytes):
                try:
                    return value.decode('utf-8')
                except UnicodeDecodeError:
                    return value
            return value
        except Exception as e:
            logger.error(f"Error getting key {key}: {str(e)}")
            return None
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in Redis."""
        await self._ensure_connection()
        try:
            if isinstance(value, str):
                value_bytes = value.encode('utf-8')
            else:
                value_bytes = str(value).encode('utf-8')
            
            if ttl:
                await self.redis.setex(
                    self._get_key(key),
                    ttl,
                    value_bytes,
                )
            else:
                await self.redis.set(self._get_key(key), value_bytes)
            return True
        except Exception as e:
            logger.error(f"Error setting key {key}: {str(e)}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete value from Redis."""
        await self._ensure_connection()
        try:
            result = await self.redis.delete(self._get_key(key))
            return bool(result)
        except Exception as e:
            logger.error(f"Error deleting key {key}: {str(e)}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists in Redis."""
        await self._ensure_connection()
        try:
            result = await self.redis.exists(self._get_key(key))
            return bool(result)
        except Exception as e:
            logger.error(f"Error checking key {key}: {str(e)}")
            return False
    
    async def clear(self) -> bool:
        """Clear all data with the prefix."""
        await self._ensure_connection()
        try:
            keys = await self.redis.keys(f"{self.prefix}*")
            if keys:
                await self.redis.delete(*keys)
            return True
        except Exception as e:
            logger.error(f"Error clearing storage: {str(e)}")
            return False
    
    async def close(self):
        """Close Redis connection."""
        if self.redis:
            await self.redis.close()
