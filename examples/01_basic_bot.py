"""
Basic PyForTG Bot Example

This example demonstrates:
- Creating a simple bot
- Message handlers with decorators
- Command handlers
- Sending messages
"""

import asyncio
import logging

from pyfortg import TelegramBot, Filters, InlineKeyboard

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    # Create bot instance
    bot = TelegramBot(token="YOUR_BOT_TOKEN")
    
    # Register /start command handler
    @bot.on_command("start")
    async def handle_start(bot, message):
        """Handle /start command."""
        keyboard = InlineKeyboard()
        keyboard.add_button("Click me!", callback_data="btn_clicked")
        
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"Hello {message.from_user.first_name}! Welcome to PyForTG bot.",
            reply_markup=keyboard.to_dict(),
        )
    
    # Register /help command handler
    @bot.on_command("help")
    async def handle_help(bot, message):
        """Handle /help command."""
        help_text = """
Available commands:
/start - Start the bot
/help - Show this message
/echo - Echo your message
        """
        await bot.send_message(
            chat_id=message.chat.id,
            text=help_text,
        )
    
    # Register message handler for echo command
    @bot.on_message(Filters.command("echo"))
    async def handle_echo(bot, message):
        """Handle /echo command."""
        args = message.text.split(maxsplit=1)
        if len(args) > 1:
            echo_text = args[1]
            await bot.send_message(
                chat_id=message.chat.id,
                text=f"Echo: {echo_text}",
            )
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text="Usage: /echo <text>",
            )
    
    # Register callback query handler
    @bot.on_callback(Filters.callback_query())
    async def handle_callback(bot, callback_query):
        """Handle callback queries."""
        await bot.answer_callback_query(
            callback_query_id=callback_query.id,
            text="Button clicked!",
            show_alert=False,
        )
    
    # Initialize bot
    await bot.initialize()
    
    # Start polling
    try:
        await bot.start_polling()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        bot.stop_polling()
    finally:
        await bot.close()


if __name__ == "__main__":
    asyncio.run(main())
