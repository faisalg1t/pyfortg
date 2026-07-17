"""
Webhook-based PyForTG Bot Example

This example demonstrates:
- Using webhooks instead of polling
- FastAPI integration
- Production-ready setup
"""

import logging
import os

from fastapi import FastAPI, Request
import uvicorn

from pyfortg import TelegramBot, Filters, InlineKeyboard

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI()

# Bot instance
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")
bot = TelegramBot(token=BOT_TOKEN)

# Register handlers
@bot.on_command("start")
async def handle_start(bot, message):
    """Handle /start command."""
    keyboard = InlineKeyboard()
    keyboard.add_button("Learn More", url="https://pyfortg.dev")
    keyboard.row()
    keyboard.add_button("GitHub", url="https://github.com/pyfortg/pyfortg")
    
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"Welcome {message.from_user.first_name}! 🚀\n\nThis is a webhook-based PyForTG bot.",
        reply_markup=keyboard.to_dict(),
    )

@bot.on_message(Filters.text())
async def handle_message(bot, message):
    """Echo user messages."""
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"You said: {message.text}",
    )

@bot.on_callback()
async def handle_callback(bot, callback):
    """Handle callback queries."""
    await bot.answer_callback_query(
        callback_query_id=callback.id,
        text="Button clicked!",
        show_alert=False,
    )


# FastAPI routes
@app.get("/")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/webhook")
async def webhook(request: Request):
    """Webhook endpoint for Telegram updates."""
    try:
        update_data = await request.json()
        await bot.handle_webhook_update(update_data)
        return {"ok": True}
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return {"ok": False, "error": str(e)}


@app.post("/set-webhook")
async def set_webhook(webhook_url: str):
    """Set webhook URL."""
    try:
        success = await bot.set_webhook(webhook_url)
        if success:
            return {"ok": True, "message": f"Webhook set to {webhook_url}"}
        else:
            return {"ok": False, "message": "Failed to set webhook"}
    except Exception as e:
        logger.error(f"Error setting webhook: {str(e)}")
        return {"ok": False, "error": str(e)}


@app.post("/delete-webhook")
async def delete_webhook():
    """Delete webhook."""
    try:
        success = await bot.delete_webhook()
        if success:
            return {"ok": True, "message": "Webhook deleted"}
        else:
            return {"ok": False, "message": "Failed to delete webhook"}
    except Exception as e:
        logger.error(f"Error deleting webhook: {str(e)}")
        return {"ok": False, "error": str(e)}


@app.get("/webhook-info")
async def get_webhook_info():
    """Get webhook info."""
    try:
        info = await bot.get_webhook_info()
        return {"ok": True, "data": info}
    except Exception as e:
        logger.error(f"Error getting webhook info: {str(e)}")
        return {"ok": False, "error": str(e)}


if __name__ == "__main__":
    # Run with: uvicorn 03_webhook_bot:app --reload --host 0.0.0.0 --port 8000
    # Then set webhook with: curl -X POST http://localhost:8000/set-webhook?webhook_url=https://yourserver.com/webhook
    
    logger.info("Starting webhook bot server...")
    logger.info("Set webhook URL by calling: POST /set-webhook?webhook_url=https://yourserver.com/webhook")
    logger.info("For local testing with ngrok: ngrok http 8000")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
