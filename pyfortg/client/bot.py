"""High-level Telegram Bot API wrapper."""

import asyncio
import logging
from typing import Optional, Dict, Any, Callable, List, Coroutine

from .base import TelegramClient
from ..types import Update, Message, CallbackQuery, User
from ..handlers import MessageHandler, CallbackHandler, CommandHandler
from ..middleware import MiddlewareChain
from ..storage.base import BaseStorage

logger = logging.getLogger(__name__)


class TelegramBot(TelegramClient):
    """High-level Telegram Bot with handlers and middleware support."""
    
    def __init__(
        self,
        token: str,
        storage: Optional[BaseStorage] = None,
        timeout: int = 30,
    ):
        """
        Initialize Telegram Bot.
        
        Args:
            token: Telegram bot token
            storage: Optional storage backend for sessions/state
            timeout: Request timeout in seconds
        """
        super().__init__(token, timeout)
        self.storage = storage
        self.middleware_chain = MiddlewareChain()
        
        self.message_handlers: List[MessageHandler] = []
        self.callback_handlers: List[CallbackHandler] = []
        self.command_handlers: Dict[str, CommandHandler] = {}
        
        self._polling = False
        self._polling_offset = 0
        self._polling_task: Optional[asyncio.Task] = None
    
    def add_message_handler(self, handler: MessageHandler) -> None:
        """Add message handler."""
        self.message_handlers.append(handler)
        logger.debug(f"Added message handler: {handler.callback.__name__}")
    
    def add_callback_handler(self, handler: CallbackHandler) -> None:
        """Add callback query handler."""
        self.callback_handlers.append(handler)
        logger.debug(f"Added callback handler: {handler.callback.__name__}")
    
    def add_command_handler(self, command: str, handler: CommandHandler) -> None:
        """Add command handler."""
        self.command_handlers[command.lstrip("/")] = handler
        logger.debug(f"Added command handler for /{command}")
    
    def on_message(self, *filters):
        """Decorator to register message handler."""
        def decorator(func: Callable) -> Callable:
            handler = MessageHandler(func, filters=filters)
            self.add_message_handler(handler)
            return func
        return decorator
    
    def on_callback(self, *filters):
        """Decorator to register callback handler."""
        def decorator(func: Callable) -> Callable:
            handler = CallbackHandler(func, filters=filters)
            self.add_callback_handler(handler)
            return func
        return decorator
    
    def on_command(self, *commands):
        """Decorator to register command handler."""
        def decorator(func: Callable) -> Callable:
            handler = CommandHandler(func)
            for command in commands:
                self.add_command_handler(command, handler)
            return func
        return decorator
    
    async def process_update(self, update: Update) -> None:
        """
        Process incoming update through handlers and middleware.
        
        Args:
            update: Telegram Update object
        """
        try:
            # Process through middleware
            update = await self.middleware_chain.process(update)
            
            if update.message:
                await self._process_message(update.message)
            elif update.callback_query:
                await self._process_callback_query(update.callback_query)
        except Exception as e:
            logger.error(f"Error processing update {update.update_id}: {str(e)}", exc_info=True)
    
    async def _process_message(self, message: Message) -> None:
        """Process message update."""
        # Check for command
        if message.text and message.text.startswith("/"):
            command = message.text.split()[0][1:].split("@")[0]
            if command in self.command_handlers:
                handler = self.command_handlers[command]
                await self._call_handler(handler.callback, message)
                return
        
        # Check message handlers
        for handler in self.message_handlers:
            if await handler.check(message):
                await self._call_handler(handler.callback, message)
                return
    
    async def _process_callback_query(self, callback_query: CallbackQuery) -> None:
        """Process callback query update."""
        for handler in self.callback_handlers:
            if await handler.check(callback_query):
                await self._call_handler(handler.callback, callback_query)
                return
    
    async def _call_handler(self, handler_func: Callable, *args, **kwargs) -> Any:
        """Call handler function with proper error handling."""
        try:
            if asyncio.iscoroutinefunction(handler_func):
                return await handler_func(self, *args, **kwargs)
            else:
                return handler_func(self, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in handler {handler_func.__name__}: {str(e)}", exc_info=True)
            raise
    
    async def start_polling(
        self,
        poll_interval: float = 1.0,
        timeout: int = 30,
        allowed_updates: Optional[List[str]] = None,
    ) -> None:
        """
        Start polling for updates.
        
        Args:
            poll_interval: Delay between polls in seconds
            timeout: Long polling timeout
            allowed_updates: Types of updates to receive
        """
        logger.info("Starting bot polling...")
        self._polling = True
        
        try:
            while self._polling:
                try:
                    updates = await self.get_updates(
                        offset=self._polling_offset,
                        timeout=timeout,
                        allowed_updates=allowed_updates,
                    )
                    
                    for update in updates:
                        await self.process_update(update)
                        self._polling_offset = update.update_id + 1
                    
                    if not updates:
                        await asyncio.sleep(poll_interval)
                
                except Exception as e:
                    logger.error(f"Error in polling loop: {str(e)}", exc_info=True)
                    await asyncio.sleep(poll_interval)
        
        finally:
            logger.info("Stopped bot polling")
    
    def stop_polling(self) -> None:
        """Stop polling for updates."""
        self._polling = False
        logger.info("Stopping bot polling...")
    
    async def start_webhook(
        self,
        webhook_url: str,
        port: int = 8000,
        path: str = "/webhook",
    ) -> None:
        """
        Start bot with webhook.
        
        Args:
            webhook_url: Public webhook URL
            port: Server port
            path: Webhook path
        """
        # This is a placeholder. Full webhook implementation would use aiohttp
        # or FastAPI for the web server
        logger.info(f"Setting webhook to {webhook_url}")
        await self.set_webhook(webhook_url)
        logger.info(f"Webhook set. Server should listen on port {port}{path}")
    
    async def handle_webhook_update(self, update_data: Dict[str, Any]) -> None:
        """Handle webhook update."""
        try:
            update = Update(**update_data)
            await self.process_update(update)
        except Exception as e:
            logger.error(f"Error handling webhook update: {str(e)}", exc_info=True)
            raise
    
    async def initialize(self) -> None:
        """Initialize bot and get bot info."""
        bot_info = await self.get_me()
        logger.info(f"Bot initialized: @{bot_info.username} ({bot_info.first_name})")
        return bot_info
