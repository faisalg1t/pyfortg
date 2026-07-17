"""
Example: Production-Ready Bot

Demonstrates best practices:
- Middleware for logging and error handling
- PostgreSQL for persistent data
- Environment variable configuration
- Proper error handling and validation
"""

import asyncio
import logging
import os
from datetime import datetime
from pyfortg import TelegramBot, Filters
from pyfortg.middleware import BaseMiddleware
from pyfortg.storage import PostgresStorage
from pyfortg.keyboards import InlineKeyboardMarkup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseMiddleware):
    """Middleware for logging all updates"""

    async def pre_process(self, bot, update, context):
        logger.info(f"Processing update {update.update_id}")
        return update

    async def post_process(self, bot, update, context, result):
        logger.info(f"Update {update.update_id} completed")
        return result


class ErrorHandlingMiddleware(BaseMiddleware):
    """Middleware for handling errors gracefully"""

    async def pre_process(self, bot, update, context):
        return update

    async def post_process(self, bot, update, context, result):
        if isinstance(result, Exception):
            logger.error(f"Error in update {update.update_id}: {result}")
        return result


async def main():
    # Configuration from environment
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    POSTGRES_DSN = os.getenv(
        "POSTGRES_DSN",
        "postgresql://user:password@localhost/botdb"
    )
    
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN environment variable not set")

    # Initialize bot
    bot = TelegramBot(token=BOT_TOKEN)
    
    # Initialize storage
    storage = PostgresStorage(dsn=POSTGRES_DSN)
    await storage.connect()
    
    # Add middleware
    bot.add_middleware(LoggingMiddleware())
    bot.add_middleware(ErrorHandlingMiddleware())

    # Helper function to track user
    async def track_user(user_id: int, action: str):
        """Track user actions in database"""
        try:
            key = f"user:{user_id}"
            user_data = await storage.get(key) or {
                "first_seen": datetime.now().isoformat(),
                "actions": []
            }
            user_data["actions"].append({
                "action": action,
                "timestamp": datetime.now().isoformat()
            })
            user_data["last_seen"] = datetime.now().isoformat()
            await storage.set(key, user_data)
        except Exception as e:
            logger.error(f"Error tracking user {user_id}: {e}")

    # Handlers
    @bot.on_command("start")
    async def handle_start(bot, update, context):
        user_id = update.message.from_user.id
        user_name = update.message.from_user.first_name
        
        await track_user(user_id, "start")
        
        keyboard = InlineKeyboardMarkup()
        keyboard.add_button("View Stats", callback_data="stats")
        keyboard.add_button("Help", callback_data="help")
        
        try:
            await bot.send_message(
                chat_id=update.message.chat.id,
                text=f"Welcome {user_name}! 👋",
                reply_markup=keyboard
            )
        except Exception as e:
            logger.error(f"Error sending message: {e}")

    @bot.on_callback_query()
    async def handle_callback(bot, update, context):
        user_id = update.callback_query.from_user.id
        callback_data = update.callback_query.data

        if callback_data == "stats":
            await track_user(user_id, "view_stats")
            
            try:
                user_data = await storage.get(f"user:{user_id}")
                if user_data:
                    stats_text = f"""
📊 Your Stats:
First Seen: {user_data.get('first_seen', 'N/A')}
Last Seen: {user_data.get('last_seen', 'N/A')}
Total Actions: {len(user_data.get('actions', []))}
                    """
                else:
                    stats_text = "No stats available yet."
                
                await bot.send_message(
                    chat_id=update.callback_query.message.chat.id,
                    text=stats_text
                )
            except Exception as e:
                logger.error(f"Error fetching stats: {e}")
                await bot.send_message(
                    chat_id=update.callback_query.message.chat.id,
                    text="Error fetching stats. Please try again later."
                )

        elif callback_data == "help":
            await track_user(user_id, "view_help")
            
            help_text = """
📖 Help Guide:
/start - Start the bot
/help - Show this message
/stats - View your statistics

Send any message to interact with me!
            """
            
            await bot.send_message(
                chat_id=update.callback_query.message.chat.id,
                text=help_text
            )

    @bot.on_command("help")
    async def handle_help(bot, update, context):
        user_id = update.message.from_user.id
        await track_user(user_id, "help_command")
        
        help_text = """
📖 Help Guide:
/start - Start the bot
/stats - View your statistics
/help - Show this message

Features:
- User tracking
- Statistics
- Database storage
- Error handling
        """
        
        await bot.send_message(
            chat_id=update.message.chat.id,
            text=help_text
        )

    @bot.on_message(Filters.text)
    async def handle_text(bot, update, context):
        user_id = update.message.from_user.id
        
        try:
            await track_user(user_id, "send_message")
            
            await bot.send_message(
                chat_id=update.message.chat.id,
                text=f"You said: {update.message.text}"
            )
        except Exception as e:
            logger.error(f"Error handling text message: {e}")
            await bot.send_message(
                chat_id=update.message.chat.id,
                text="Sorry, an error occurred. Please try again."
            )

    # Graceful shutdown
    try:
        logger.info("Starting bot...")
        await bot.run_polling()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
    finally:
        await storage.close()
        logger.info("Cleanup completed")


if __name__ == "__main__":
    asyncio.run(main())
