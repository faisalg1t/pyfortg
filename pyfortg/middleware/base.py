"""Middleware implementation."""

import asyncio
import logging
from typing import Callable, List, Optional
from abc import ABC, abstractmethod

from ..types import Update

logger = logging.getLogger(__name__)


class Middleware(ABC):
    """Base middleware class."""
    
    @abstractmethod
    async def process(self, update: Update) -> Update:
        """
        Process update through middleware.
        
        Args:
            update: Telegram Update object
        
        Returns:
            Processed Update object
        """
        pass


class MiddlewareChain:
    """Chain of responsibility for middleware processing."""
    
    def __init__(self):
        self.middlewares: List[Middleware] = []
    
    def add_middleware(self, middleware: Middleware) -> None:
        """Add middleware to chain."""
        self.middlewares.append(middleware)
        logger.debug(f"Added middleware: {middleware.__class__.__name__}")
    
    async def process(self, update: Update) -> Update:
        """Process update through all middleware."""
        for middleware in self.middlewares:
            try:
                update = await middleware.process(update)
            except Exception as e:
                logger.error(
                    f"Error in middleware {middleware.__class__.__name__}: {str(e)}",
                    exc_info=True,
                )
                raise
        
        return update


class LoggingMiddleware(Middleware):
    """Middleware that logs all updates."""
    
    async def process(self, update: Update) -> Update:
        """Log update details."""
        if update.message:
            logger.info(
                f"Message from {update.message.from_user.id}: {update.message.text[:100] if update.message.text else '[No text]'}"
            )
        elif update.callback_query:
            logger.info(
                f"Callback from {update.callback_query.from_user.id}: {update.callback_query.data}"
            )
        
        return update


class RateLimitMiddleware(Middleware):
    """Middleware for rate limiting by user."""
    
    def __init__(self, requests_per_second: float = 10):
        self.requests_per_second = requests_per_second
        self.user_requests: dict = {}
    
    async def process(self, update: Update) -> Update:
        """Rate limit by user."""
        user_id = None
        
        if update.message and update.message.from_user:
            user_id = update.message.from_user.id
        elif update.callback_query:
            user_id = update.callback_query.from_user.id
        
        if user_id is None:
            return update
        
        # Simple token bucket implementation
        now = asyncio.get_event_loop().time()
        
        if user_id not in self.user_requests:
            self.user_requests[user_id] = {
                "tokens": self.requests_per_second,
                "last_update": now,
            }
        else:
            user_data = self.user_requests[user_id]
            time_passed = now - user_data["last_update"]
            user_data["tokens"] = min(
                self.requests_per_second,
                user_data["tokens"] + time_passed * self.requests_per_second,
            )
            user_data["last_update"] = now
            
            if user_data["tokens"] < 1:
                logger.warning(f"Rate limit exceeded for user {user_id}")
                await asyncio.sleep(1 / self.requests_per_second)
            else:
                user_data["tokens"] -= 1
        
        return update


class ContextMiddleware(Middleware):
    """Middleware for storing context in updates."""
    
    def __init__(self):
        self.context: dict = {}
    
    async def process(self, update: Update) -> Update:
        """Add context to update."""
        # Store context reference on update
        if not hasattr(update, "context"):
            update.context = self.context
        
        return update
