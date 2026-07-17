"""Message and update filters for handler routing."""

import re
from typing import Callable, Optional, List, Any
from abc import ABC, abstractmethod

from .types import Message, Update, CallbackQuery


class BaseFilter(ABC):
    """Base class for all filters."""
    
    @abstractmethod
    async def check(self, update: Update) -> bool:
        """Check if update matches the filter."""
        pass
    
    def __and__(self, other: 'BaseFilter') -> 'AndFilter':
        return AndFilter(self, other)
    
    def __or__(self, other: 'BaseFilter') -> 'OrFilter':
        return OrFilter(self, other)
    
    def __invert__(self) -> 'NotFilter':
        return NotFilter(self)


class AndFilter(BaseFilter):
    """Combines multiple filters with AND logic."""
    
    def __init__(self, left: BaseFilter, right: BaseFilter):
        self.left = left
        self.right = right
    
    async def check(self, update: Update) -> bool:
        return await self.left.check(update) and await self.right.check(update)


class OrFilter(BaseFilter):
    """Combines multiple filters with OR logic."""
    
    def __init__(self, left: BaseFilter, right: BaseFilter):
        self.left = left
        self.right = right
    
    async def check(self, update: Update) -> bool:
        return await self.left.check(update) or await self.right.check(update)


class NotFilter(BaseFilter):
    """Inverts a filter."""
    
    def __init__(self, filter: BaseFilter):
        self.filter = filter
    
    async def check(self, update: Update) -> bool:
        return not await self.filter.check(update)


class TextFilter(BaseFilter):
    """Filter by message text."""
    
    def __init__(self, text: Optional[str] = None, pattern: Optional[str] = None):
        self.text = text
        self.pattern = re.compile(pattern) if pattern else None
    
    async def check(self, update: Update) -> bool:
        if not update.message or not update.message.text:
            return False
        
        if self.text is not None:
            return update.message.text == self.text
        
        if self.pattern is not None:
            return bool(self.pattern.match(update.message.text))
        
        return True


class CommandFilter(BaseFilter):
    """Filter for command messages."""
    
    def __init__(self, commands: Optional[List[str]] = None):
        self.commands = [cmd.lstrip('/') for cmd in commands] if commands else None
    
    async def check(self, update: Update) -> bool:
        if not update.message or not update.message.text:
            return False
        
        text = update.message.text.split()[0]
        if not text.startswith('/'):
            return False
        
        command = text[1:].split('@')[0]
        
        if self.commands is None:
            return True
        
        return command in self.commands


class ChatTypeFilter(BaseFilter):
    """Filter by chat type."""
    
    def __init__(self, chat_types: List[str]):
        self.chat_types = chat_types
    
    async def check(self, update: Update) -> bool:
        if update.message:
            return update.message.chat.type in self.chat_types
        return False


class PrivateChatFilter(BaseFilter):
    """Filter for private chats."""
    
    async def check(self, update: Update) -> bool:
        if update.message:
            return update.message.chat.type == "private"
        return False


class GroupChatFilter(BaseFilter):
    """Filter for group chats."""
    
    async def check(self, update: Update) -> bool:
        if update.message:
            return update.message.chat.type in ["group", "supergroup"]
        return False


class ChannelPostFilter(BaseFilter):
    """Filter for channel posts."""
    
    async def check(self, update: Update) -> bool:
        return update.channel_post is not None


class CallbackQueryFilter(BaseFilter):
    """Filter for callback queries."""
    
    def __init__(self, data_pattern: Optional[str] = None):
        self.data_pattern = re.compile(data_pattern) if data_pattern else None
    
    async def check(self, update: Update) -> bool:
        if not update.callback_query or not update.callback_query.data:
            return False
        
        if self.data_pattern is None:
            return True
        
        return bool(self.data_pattern.match(update.callback_query.data))


class FileTypeFilter(BaseFilter):
    """Filter by file type."""
    
    def __init__(self, file_types: List[str]):
        self.file_types = file_types
    
    async def check(self, update: Update) -> bool:
        if not update.message:
            return False
        
        message = update.message
        
        if "photo" in self.file_types and message.photo:
            return True
        if "document" in self.file_types and message.document:
            return True
        if "audio" in self.file_types and message.audio:
            return True
        if "video" in self.file_types and message.video:
            return True
        
        return False


class UserFilter(BaseFilter):
    """Filter by user ID."""
    
    def __init__(self, user_ids: List[int]):
        self.user_ids = user_ids
    
    async def check(self, update: Update) -> bool:
        user_id = None
        
        if update.message and update.message.from_user:
            user_id = update.message.from_user.id
        elif update.callback_query:
            user_id = update.callback_query.from_user.id
        
        if user_id is None:
            return False
        
        return user_id in self.user_ids


class CustomFilter(BaseFilter):
    """Custom filter with user-defined check function."""
    
    def __init__(self, check_func: Callable[[Update], bool]):
        self.check_func = check_func
    
    async def check(self, update: Update) -> bool:
        if callable(self.check_func):
            result = self.check_func(update)
            if hasattr(result, '__await__'):
                return await result
            return result
        return False


class Filters:
    """Convenient filter factory for common use cases."""
    
    @staticmethod
    def text(text: Optional[str] = None, pattern: Optional[str] = None) -> TextFilter:
        """Filter by text content."""
        return TextFilter(text=text, pattern=pattern)
    
    @staticmethod
    def command(commands: Optional[List[str]] = None) -> CommandFilter:
        """Filter for command messages."""
        return CommandFilter(commands=commands)
    
    @staticmethod
    def private_chat() -> PrivateChatFilter:
        """Filter for private chats."""
        return PrivateChatFilter()
    
    @staticmethod
    def group_chat() -> GroupChatFilter:
        """Filter for group chats."""
        return GroupChatFilter()
    
    @staticmethod
    def callback_query(data_pattern: Optional[str] = None) -> CallbackQueryFilter:
        """Filter for callback queries."""
        return CallbackQueryFilter(data_pattern=data_pattern)
    
    @staticmethod
    def file_type(file_types: List[str]) -> FileTypeFilter:
        """Filter by file type (photo, document, audio, video)."""
        return FileTypeFilter(file_types=file_types)
    
    @staticmethod
    def user(user_ids: List[int]) -> UserFilter:
        """Filter by user ID."""
        return UserFilter(user_ids=user_ids)
    
    @staticmethod
    def channel_post() -> ChannelPostFilter:
        """Filter for channel posts."""
        return ChannelPostFilter()
    
    @staticmethod
    def custom(check_func: Callable[[Update], bool]) -> CustomFilter:
        """Create custom filter with function."""
        return CustomFilter(check_func=check_func)
