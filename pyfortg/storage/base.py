"""Base storage interface."""

import json
from typing import Any, Optional
from abc import ABC, abstractmethod


class BaseStorage(ABC):
    """Abstract base class for storage backends."""
    
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Get value by key."""
        pass
    
    @abstractmethod
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value with optional TTL in seconds."""
        pass
    
    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete value by key."""
        pass
    
    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if key exists."""
        pass
    
    @abstractmethod
    async def clear(self) -> bool:
        """Clear all data."""
        pass
    
    async def get_user_data(self, user_id: int) -> dict:
        """Get user data."""
        key = f"user:{user_id}"
        data = await self.get(key)
        return json.loads(data) if data else {}
    
    async def set_user_data(self, user_id: int, data: dict, ttl: Optional[int] = None) -> bool:
        """Set user data."""
        key = f"user:{user_id}"
        return await self.set(key, json.dumps(data), ttl)
    
    async def update_user_data(self, user_id: int, data: dict, ttl: Optional[int] = None) -> bool:
        """Update user data (merge with existing)."""
        key = f"user:{user_id}"
        existing = await self.get_user_data(user_id)
        existing.update(data)
        return await self.set(key, json.dumps(existing), ttl)
    
    async def get_user_state(self, user_id: int) -> Optional[str]:
        """Get user state."""
        key = f"user_state:{user_id}"
        return await self.get(key)
    
    async def set_user_state(self, user_id: int, state: str, ttl: Optional[int] = None) -> bool:
        """Set user state."""
        key = f"user_state:{user_id}"
        return await self.set(key, state, ttl)


class MemoryStorage(BaseStorage):
    """In-memory storage backend."""
    
    def __init__(self):
        self.data: dict = {}
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from memory."""
        return self.data.get(key)
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in memory."""
        self.data[key] = value
        return True
    
    async def delete(self, key: str) -> bool:
        """Delete value from memory."""
        if key in self.data:
            del self.data[key]
            return True
        return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists in memory."""
        return key in self.data
    
    async def clear(self) -> bool:
        """Clear all data from memory."""
        self.data.clear()
        return True
