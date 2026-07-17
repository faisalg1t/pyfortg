"""Base handler classes."""

import asyncio
from typing import Callable, Optional, Tuple, Any
from abc import ABC, abstractmethod

from ..types import Message, CallbackQuery, Update
from ..filters import BaseFilter


class BaseHandler(ABC):
    """Base class for all handlers."""
    
    def __init__(
        self,
        callback: Callable,
        filters: Tuple[BaseFilter, ...] = (),
    ):
        self.callback = callback
        self.filters = filters
    
    @abstractmethod
    async def check(self, obj: Any) -> bool:
        """Check if handler should process the object."""
        pass
    
    async def _check_filters(self, obj: Any) -> bool:
        """Check all filters."""
        if not self.filters:
            return True
        
        for filter_obj in self.filters:
            # Handle Update objects
            if isinstance(obj, Update):
                if not await filter_obj.check(obj):
                    return False
            # For Message/CallbackQuery, create Update wrapper
            else:
                update = Update(update_id=0)
                if isinstance(obj, Message):
                    update.message = obj
                elif isinstance(obj, CallbackQuery):
                    update.callback_query = obj
                
                if not await filter_obj.check(update):
                    return False
        
        return True


class MessageHandler(BaseHandler):
    """Handler for message updates."""
    
    async def check(self, message: Message) -> bool:
        """Check if message matches filters."""
        return await self._check_filters(message)


class CallbackHandler(BaseHandler):
    """Handler for callback query updates."""
    
    async def check(self, callback_query: CallbackQuery) -> bool:
        """Check if callback query matches filters."""
        return await self._check_filters(callback_query)


class CommandHandler(BaseHandler):
    """Handler for command messages."""
    
    async def check(self, obj: Any) -> bool:
        """Check if object is a command."""
        # Commands are checked during message processing
        return True
