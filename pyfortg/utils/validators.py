"""Validation utilities."""

import re
from ..exceptions import ValidationException


def validate_token(token: str) -> bool:
    """Validate Telegram bot token format."""
    # Token format: 123456789:ABCdEfGhIjKlMnOpQrStUvWxYz
    pattern = r'^\d+:[A-Za-z0-9_-]+$'
    if not re.match(pattern, token):
        raise ValidationException(f"Invalid token format: {token}")
    return True


def validate_chat_id(chat_id: int) -> bool:
    """Validate chat ID."""
    if not isinstance(chat_id, int):
        raise ValidationException(f"Chat ID must be integer, got {type(chat_id)}")
    if chat_id == 0:
        raise ValidationException("Chat ID cannot be 0")
    return True


def validate_message_text(text: str, max_length: int = 4096) -> bool:
    """Validate message text."""
    if not isinstance(text, str):
        raise ValidationException(f"Message text must be string, got {type(text)}")
    if len(text) == 0:
        raise ValidationException("Message text cannot be empty")
    if len(text) > max_length:
        raise ValidationException(f"Message text too long: {len(text)} > {max_length}")
    return True


def validate_callback_data(data: str, max_length: int = 64) -> bool:
    """Validate callback data."""
    if not isinstance(data, str):
        raise ValidationException(f"Callback data must be string, got {type(data)}")
    if len(data) == 0:
        raise ValidationException("Callback data cannot be empty")
    if len(data) > max_length:
        raise ValidationException(f"Callback data too long: {len(data)} > {max_length}")
    return True


def validate_button_text(text: str, max_length: int = 64) -> bool:
    """Validate button text."""
    if not isinstance(text, str):
        raise ValidationException(f"Button text must be string, got {type(text)}")
    if len(text) == 0:
        raise ValidationException("Button text cannot be empty")
    if len(text) > max_length:
        raise ValidationException(f"Button text too long: {len(text)} > {max_length}")
    return True
