"""
Advanced PyForTG Bot Example

This example demonstrates:
- Using storage backends (Redis/PostgreSQL)
- User state management
- Middleware usage
- File handling
- Complex keyboards
"""

import asyncio
import logging

from pyfortg import TelegramBot, Filters, InlineKeyboard, ReplyKeyboard
from pyfortg.storage import MemoryStorage  # Use RedisStorage or PostgresStorage in production
from pyfortg.middleware import LoggingMiddleware, RateLimitMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    # Create bot with storage
    storage = MemoryStorage()  # Use RedisStorage("redis://localhost") for production
    bot = TelegramBot(token="YOUR_BOT_TOKEN", storage=storage)
    
    # Add middleware
    bot.middleware_chain.add_middleware(LoggingMiddleware())
    bot.middleware_chain.add_middleware(RateLimitMiddleware(requests_per_second=10))
    
    # State constants
    STATE_MAIN = "main"
    STATE_AWAITING_NAME = "awaiting_name"
    STATE_AWAITING_EMAIL = "awaiting_email"
    
    @bot.on_command("start", "help")
    async def handle_start_help(bot, message):
        """Handle /start and /help commands."""
        user_id = message.from_user.id
        
        # Initialize user data
        await storage.set_user_state(user_id, STATE_MAIN)
        await storage.set_user_data(user_id, {
            "username": message.from_user.username or "Unknown",
            "first_name": message.from_user.first_name,
        })
        
        # Show main menu
        keyboard = ReplyKeyboard(one_time_keyboard=True)
        keyboard.add_button("Register Profile")
        keyboard.add_button("View Profile")
        keyboard.row()
        keyboard.add_button("Download File")
        
        await bot.send_message(
            chat_id=message.chat.id,
            text="Welcome! What would you like to do?",
            reply_markup=keyboard.to_dict(),
        )
    
    @bot.on_message(Filters.text("Register Profile"))
    async def handle_register(bot, message):
        """Start registration flow."""
        user_id = message.from_user.id
        await storage.set_user_state(user_id, STATE_AWAITING_NAME)
        
        await bot.send_message(
            chat_id=message.chat.id,
            text="Please enter your name:",
        )
    
    @bot.on_message(Filters.text("View Profile"))
    async def handle_view_profile(bot, message):
        """View user profile."""
        user_id = message.from_user.id
        user_data = await storage.get_user_data(user_id)
        
        if user_data:
            profile_text = f"""
Profile Information:
Name: {user_data.get('name', 'Not set')}
Email: {user_data.get('email', 'Not set')}
First Name: {user_data.get('first_name', 'Unknown')}
Username: {user_data.get('username', 'Unknown')}
            """
            await bot.send_message(
                chat_id=message.chat.id,
                text=profile_text,
            )
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text="No profile found. Please register first.",
            )
    
    @bot.on_message(Filters.text("Download File"))
    async def handle_download_file(bot, message):
        """Handle file download request."""
        keyboard = InlineKeyboard()
        keyboard.add_button("Download Sample PDF", url="https://example.com/sample.pdf")
        keyboard.row()
        keyboard.add_button("Download Sample Image", url="https://example.com/sample.jpg")
        
        await bot.send_message(
            chat_id=message.chat.id,
            text="Select a file to download:",
            reply_markup=keyboard.to_dict(),
        )
    
    @bot.on_message()  # Catch all messages
    async def handle_message(bot, message):
        """Handle message based on user state."""
        user_id = message.from_user.id
        state = await storage.get_user_state(user_id)
        
        if state == STATE_AWAITING_NAME and message.text:
            # Save name
            await storage.update_user_data(user_id, {"name": message.text})
            await storage.set_user_state(user_id, STATE_AWAITING_EMAIL)
            
            await bot.send_message(
                chat_id=message.chat.id,
                text="Now please enter your email:",
            )
        
        elif state == STATE_AWAITING_EMAIL and message.text:
            # Save email
            await storage.update_user_data(user_id, {"email": message.text})
            await storage.set_user_state(user_id, STATE_MAIN)
            
            await bot.send_message(
                chat_id=message.chat.id,
                text="Profile registered successfully! Use /start to return to menu.",
            )
    
    # Initialize and run
    await bot.initialize()
    
    try:
        await bot.start_polling()
    except KeyboardInterrupt:
        logger.info("Bot stopped")
        bot.stop_polling()
    finally:
        await bot.close()


if __name__ == "__main__":
    asyncio.run(main())
