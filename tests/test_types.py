"""Tests for types module."""

import pytest

from pyfortg.types import User, Chat, Message, Update


def test_user_creation():
    """Test User model creation."""
    user = User(
        id=123456,
        is_bot=False,
        first_name="John",
        last_name="Doe",
        username="johndoe",
    )
    
    assert user.id == 123456
    assert user.first_name == "John"
    assert user.username == "johndoe"


def test_chat_creation():
    """Test Chat model creation."""
    chat = Chat(
        id=-100123456789,
        type="supergroup",
        title="Test Group",
    )
    
    assert chat.id == -100123456789
    assert chat.type == "supergroup"
    assert chat.title == "Test Group"


def test_message_creation():
    """Test Message model creation."""
    user = User(id=123, is_bot=False, first_name="Test")
    chat = Chat(id=456, type="private")
    
    message = Message(
        message_id=1,
        date=1234567890,
        chat=chat,
        text="Hello",
    )
    
    assert message.message_id == 1
    assert message.text == "Hello"
    assert message.chat.id == 456


def test_update_creation():
    """Test Update model creation."""
    user = User(id=123, is_bot=False, first_name="Test")
    chat = Chat(id=456, type="private")
    message = Message(
        message_id=1,
        date=1234567890,
        chat=chat,
        text="Hello",
    )
    
    update = Update(
        update_id=1,
        message=message,
    )
    
    assert update.update_id == 1
    assert update.message is not None
    assert update.message.text == "Hello"
