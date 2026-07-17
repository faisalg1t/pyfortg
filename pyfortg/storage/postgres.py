"""PostgreSQL storage backend."""

import json
import logging
from typing import Any, Optional

from .base import BaseStorage

logger = logging.getLogger(__name__)


class PostgresStorage(BaseStorage):
    """PostgreSQL-based storage backend."""
    
    def __init__(
        self,
        dsn: str = "postgresql://localhost/pyfortg",
        table_name: str = "pyfortg_storage",
    ):
        """
        Initialize PostgreSQL storage.
        
        Args:
            dsn: PostgreSQL connection string
            table_name: Table name for storage
        """
        self.dsn = dsn
        self.table_name = table_name
        self.pool = None
    
    async def _ensure_connection(self):
        """Ensure PostgreSQL connection pool is established."""
        if self.pool is None:
            try:
                import asyncpg
                self.pool = await asyncpg.create_pool(self.dsn)
                await self._create_table()
            except ImportError:
                raise ImportError(
                    "asyncpg is required for PostgresStorage. "
                    "Install it with: pip install pyfortg[postgres]"
                )
    
    async def _create_table(self):
        """Create storage table if it doesn't exist."""
        async with self.pool.acquire() as conn:
            await conn.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ttl_at TIMESTAMP
                )
            """)
            
            # Create index on ttl_at for cleanup queries
            await conn.execute(f"""
                CREATE INDEX IF NOT EXISTS {self.table_name}_ttl_idx 
                ON {self.table_name} (ttl_at) 
                WHERE ttl_at IS NOT NULL
            """)
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from PostgreSQL."""
        await self._ensure_connection()
        try:
            async with self.pool.acquire() as conn:
                row = await conn.fetchrow(
                    f"""
                    SELECT value FROM {self.table_name} 
                    WHERE key = $1 AND (ttl_at IS NULL OR ttl_at > CURRENT_TIMESTAMP)
                    """,
                    key,
                )
                if row:
                    return row['value']
                return None
        except Exception as e:
            logger.error(f"Error getting key {key}: {str(e)}")
            return None
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in PostgreSQL."""
        await self._ensure_connection()
        try:
            value_str = value if isinstance(value, str) else str(value)
            
            async with self.pool.acquire() as conn:
                if ttl:
                    await conn.execute(
                        f"""
                        INSERT INTO {self.table_name} (key, value, ttl_at)
                        VALUES ($1, $2, CURRENT_TIMESTAMP + ($3 || ' seconds')::INTERVAL)
                        ON CONFLICT (key) DO UPDATE SET
                            value = $2,
                            updated_at = CURRENT_TIMESTAMP,
                            ttl_at = CURRENT_TIMESTAMP + ($3 || ' seconds')::INTERVAL
                        """,
                        key,
                        value_str,
                        ttl,
                    )
                else:
                    await conn.execute(
                        f"""
                        INSERT INTO {self.table_name} (key, value, ttl_at)
                        VALUES ($1, $2, NULL)
                        ON CONFLICT (key) DO UPDATE SET
                            value = $2,
                            updated_at = CURRENT_TIMESTAMP,
                            ttl_at = NULL
                        """,
                        key,
                        value_str,
                    )
            return True
        except Exception as e:
            logger.error(f"Error setting key {key}: {str(e)}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete value from PostgreSQL."""
        await self._ensure_connection()
        try:
            async with self.pool.acquire() as conn:
                result = await conn.execute(
                    f"DELETE FROM {self.table_name} WHERE key = $1",
                    key,
                )
            return "1" in result  # asyncpg returns DELETE count
        except Exception as e:
            logger.error(f"Error deleting key {key}: {str(e)}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists in PostgreSQL."""
        await self._ensure_connection()
        try:
            async with self.pool.acquire() as conn:
                row = await conn.fetchval(
                    f"""
                    SELECT 1 FROM {self.table_name} 
                    WHERE key = $1 AND (ttl_at IS NULL OR ttl_at > CURRENT_TIMESTAMP)
                    """,
                    key,
                )
            return row is not None
        except Exception as e:
            logger.error(f"Error checking key {key}: {str(e)}")
            return False
    
    async def clear(self) -> bool:
        """Clear all data from PostgreSQL."""
        await self._ensure_connection()
        try:
            async with self.pool.acquire() as conn:
                await conn.execute(f"DELETE FROM {self.table_name}")
            return True
        except Exception as e:
            logger.error(f"Error clearing storage: {str(e)}")
            return False
    
    async def cleanup_expired(self) -> int:
        """Clean up expired keys. Returns count of deleted rows."""
        await self._ensure_connection()
        try:
            async with self.pool.acquire() as conn:
                result = await conn.execute(
                    f"""
                    DELETE FROM {self.table_name} 
                    WHERE ttl_at IS NOT NULL AND ttl_at <= CURRENT_TIMESTAMP
                    """
                )
            # Extract count from result string like "DELETE 5"
            count = int(result.split()[-1]) if result else 0
            return count
        except Exception as e:
            logger.error(f"Error cleaning up expired keys: {str(e)}")
            return 0
    
    async def close(self):
        """Close PostgreSQL connection pool."""
        if self.pool:
            await self.pool.close()
