"""Tests for filters module."""

import pytest

from pyfortg.filters import (
    TextFilter,
    CommandFilter,
    PrivateChatFilter,
    GroupChatFilter,
    Filters,
)
from pyfortg.types import User, Chat, Message, Update


@pytest.mark.asyncio
async def test_text_filter_exact_match():
    """Test TextFilter with exact text match."""
    filter_obj = TextFilter(text="hello")
    
    user = User(id=1, is_bot=False, first_name="Test")
    chat = Chat(id=1, type="private")
    message = Message(message_id=1, date=123, chat=chat, text="hello")
    update = Update(update_id=1, message=message)
    
    assert await filter_obj.check(message) is True


@pytest.mark.asyncio
async def test_text_filter_pattern():
    """Test TextFilter with pattern."""
    filter_obj = TextFilter(pattern=r"^\d{3}$")
    
    user = User(id=1, is_bot=False, first_name="Test")
    chat = Chat(id=1, type="private")
    message = Message(message_id=1, date=123, chat=chat, text="123")
    
    assert await filter_obj.check(message) is True


@pytest.mark.asyncio
async def test_command_filter():
    """Test CommandFilter."""
    filter_obj = CommandFilter(commands=["start", "help"])
    
    user = User(id=1, is_bot=False, first_name="Test")
    chat = Chat(id=1, type="private")
    message = Message(message_id=1, date=123, chat=chat, text="/start")
    
    assert await filter_obj.check(message) is True


@pytest.mark.asyncio
async def test_private_chat_filter():
    """Test PrivateChatFilter."""
    filter_obj = PrivateChatFilter()
    
    user = User(id=1, is_bot=False, first_name="Test")
    chat = Chat(id=1, type="private")
    message = Message(message_id=1, date=123, chat=chat)
    
    assert await filter_obj.check(message) is True


@pytest.mark.asyncio
async def test_group_chat_filter():
    """Test GroupChatFilter."""
    filter_obj = GroupChatFilter()
    
    user = User(id=1, is_bot=False, first_name="Test")
    chat = Chat(id=-1, type="supergroup")
    message = Message(message_id=1, date=123, chat=chat)
    
    assert await filter_obj.check(message) is True


@pytest.mark.asyncio
async def test_filter_combination():
    """Test combining filters with AND operator."""
    filter_obj = Filters.private_chat() & Filters.text(pattern=r"hello")
    
    user = User(id=1, is_bot=False, first_name="Test")
    chat = Chat(id=1, type="private")
    message = Message(message_id=1, date=123, chat=chat, text="hello world")
    
    assert await filter_obj.check(message) is True
