"""
PyForTG - Production-ready Python package for building high-concurrency Telegram bots.

This package provides:
- Async-first architecture with webhook and polling support
- High-performance message handling
- Built-in Redis and PostgreSQL support
- Middleware and filter systems
- Decorator-based routing
- Type safety with Pydantic validation
"""

__version__ = "1.0.0"
__author__ = "PyForTG Contributors"
__license__ = "MIT"

from .client import TelegramClient, TelegramBot
from .handlers import MessageHandler, CallbackHandler, CommandHandler
from .middleware import Middleware, MiddlewareChain
from .keyboards import InlineKeyboard, ReplyKeyboard, KeyboardButton, InlineButton
from .types import (
    Update,
    Message,
    CallbackQuery,
    User,
    Chat,
    Document,
    PhotoSize,
    Audio,
    Video,
    File,
)
from .filters import Filters
from .exceptions import PyForTGException, APIException, ValidationException

__all__ = [
    "TelegramClient",
    "TelegramBot",
    "MessageHandler",
    "CallbackHandler",
    "CommandHandler",
    "Middleware",
    "MiddlewareChain",
    "InlineKeyboard",
    "ReplyKeyboard",
    "KeyboardButton",
    "InlineButton",
    "Update",
    "Message",
    "CallbackQuery",
    "User",
    "Chat",
    "Document",
    "PhotoSize",
    "Audio",
    "Video",
    "File",
    "Filters",
    "PyForTGException",
    "APIException",
    "ValidationException",
]
