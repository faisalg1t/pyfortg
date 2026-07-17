"""Tests for storage backends."""

import pytest
import json

from pyfortg.storage import MemoryStorage, BaseStorage


@pytest.mark.asyncio
async def test_memory_storage_set_get():
    """Test memory storage set and get."""
    storage = MemoryStorage()
    
    assert await storage.set("key1", "value1") is True
    assert await storage.get("key1") == "value1"


@pytest.mark.asyncio
async def test_memory_storage_delete():
    """Test memory storage delete."""
    storage = MemoryStorage()
    
    await storage.set("key1", "value1")
    assert await storage.delete("key1") is True
    assert await storage.get("key1") is None


@pytest.mark.asyncio
async def test_memory_storage_exists():
    """Test memory storage exists check."""
    storage = MemoryStorage()
    
    await storage.set("key1", "value1")
    assert await storage.exists("key1") is True
    assert await storage.exists("key2") is False


@pytest.mark.asyncio
async def test_memory_storage_clear():
    """Test memory storage clear."""
    storage = MemoryStorage()
    
    await storage.set("key1", "value1")
    await storage.set("key2", "value2")
    assert await storage.clear() is True
    assert await storage.get("key1") is None
    assert await storage.get("key2") is None


@pytest.mark.asyncio
async def test_user_data_methods():
    """Test user data convenience methods."""
    storage = MemoryStorage()
    user_id = 123
    
    # Set user data
    data = {"name": "John", "age": 30}
    assert await storage.set_user_data(user_id, data) is True
    
    # Get user data
    retrieved = await storage.get_user_data(user_id)
    assert retrieved == data
    
    # Update user data
    assert await storage.update_user_data(user_id, {"age": 31}) is True
    retrieved = await storage.get_user_data(user_id)
    assert retrieved["age"] == 31
    assert retrieved["name"] == "John"


@pytest.mark.asyncio
async def test_user_state_methods():
    """Test user state convenience methods."""
    storage = MemoryStorage()
    user_id = 123
    
    # Set state
    assert await storage.set_user_state(user_id, "waiting_name") is True
    
    # Get state
    state = await storage.get_user_state(user_id)
    assert state == "waiting_name"
