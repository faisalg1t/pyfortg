# Getting Started with PyForTG

## Prerequisites

- Python 3.9 or higher
- A Telegram account and a Telegram bot token

## Creating a Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Send the command `/newbot`
3. Follow the instructions to name your bot
4. Copy the **API token** provided
5. Save it securely (don't share!)

## Installation

### Quick Start

```bash
pip install pyfortg
```

### With Optional Features

```bash
# With Redis support
pip install pyfortg[redis]

# With PostgreSQL support
pip install pyfortg[postgres]

# With all features
pip install pyfortg[all]
```

## Your First Bot

Create a file called `bot.py`:

```python
import asyncio
from pyfortg import TelegramBot, Filters

async def main():
    bot = TelegramBot(token="YOUR_BOT_TOKEN_HERE")

    @bot.on_command("start")
    async def handle_start(bot, update, context):
        await bot.send_message(
            chat_id=update.message.chat.id,
            text="Hello! I'm your first PyForTG bot! 🎉"
        )

    @bot.on_message(Filters.text)
    async def handle_text(bot, update, context):
        text = update.message.text
        await bot.send_message(
            chat_id=update.message.chat.id,
            text=f"You said: {text}"
        )

    await bot.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
```

Replace `YOUR_BOT_TOKEN_HERE` with your actual token from BotFather.

### Run Your Bot

```bash
python bot.py
```

Now open Telegram, find your bot, and send it a message!

## Common Patterns

### Handling Commands

```python
@bot.on_command("help")
async def handle_help(bot, update, context):
    await bot.send_message(
        chat_id=update.message.chat.id,
        text="Here's how to use me..."
    )

@bot.on_command("start")
async def handle_start(bot, update, context):
    await bot.send_message(
        chat_id=update.message.chat.id,
        text="Welcome!"
    )
```

### Using Filters

```python
from pyfortg import Filters

# Only handle text messages
@bot.on_message(Filters.text)
async def handle_text(bot, update, context):
    pass

# Only handle photos
@bot.on_message(Filters.photo)
async def handle_photo(bot, update, context):
    pass

# Combine filters with AND
@bot.on_message(Filters.text & Filters.from_user(user_id=123))
async def handle_specific_user(bot, update, context):
    pass

# Combine with OR
@bot.on_message(Filters.photo | Filters.video)
async def handle_media(bot, update, context):
    pass
```

### Interactive Keyboards

```python
from pyfortg.keyboards import InlineKeyboardMarkup

keyboard = InlineKeyboardMarkup()
keyboard.add_button("Button 1", callback_data="btn_1")
keyboard.add_button("Button 2", callback_data="btn_2")

await bot.send_message(
    chat_id=update.message.chat.id,
    text="Choose an option:",
    reply_markup=keyboard
)

@bot.on_callback_query()
async def handle_button(bot, update, context):
    callback_data = update.callback_query.data
    if callback_data == "btn_1":
        # Handle button 1 click
        pass
```

### User State Management

```python
from pyfortg.storage import RedisStorage

storage = RedisStorage(url="redis://localhost")

@bot.on_message(Filters.text)
async def handle_message(bot, update, context):
    user_id = str(update.message.from_user.id)
    
    # Get user data
    user_data = await storage.get(f"user:{user_id}")
    
    # Update user data
    if not user_data:
        user_data = {"messages": 0}
    
    user_data["messages"] += 1
    await storage.set(f"user:{user_id}", user_data)
    
    await bot.send_message(
        chat_id=update.message.chat.id,
        text=f"You've sent {user_data['messages']} messages"
    )
```

### Error Handling

```python
try:
    result = await bot.send_message(
        chat_id=chat_id,
        text=message
    )
except Exception as e:
    print(f"Error sending message: {e}")
    # Handle error appropriately
```

## Environment Variables

Keep your bot token secure using environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()
bot_token = os.getenv("BOT_TOKEN")

if not bot_token:
    raise ValueError("BOT_TOKEN not found in environment")

bot = TelegramBot(token=bot_token)
```

Create a `.env` file:

```
BOT_TOKEN=your_actual_token_here
```

## Running with Webhooks

For production deployments, use webhooks instead of polling:

```python
await bot.run_webhook(
    host="0.0.0.0",
    port=8080,
    webhook_path="/webhook"
)
```

Configure the webhook:

```python
await bot.set_webhook(url="https://your-domain.com/webhook")
```

## Deployment Options

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN pip install pyfortg[all]

COPY . .

CMD ["python", "bot.py"]
```

Build and run:

```bash
docker build -t my-bot .
docker run -e BOT_TOKEN=your_token my-bot
```

### Heroku

```bash
heroku login
heroku create my-bot
git push heroku main
heroku config:set BOT_TOKEN=your_token
```

### VPS

```bash
ssh user@your-vps
git clone your-repo
cd your-repo
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
nohup python bot.py &
```

## Next Steps

1. **Read the API Reference**: Check `docs/API_REFERENCE.md`
2. **Explore Examples**: Look at the `examples/` folder
3. **Storage Setup**: See `docs/STORAGE.md` for database setup
4. **Advanced Patterns**: Check `examples/06_production_bot.py`

## Getting Help

- **GitHub Issues**: https://github.com/pyfortg/pyfortg/issues
- **Documentation**: https://pyfortg.readthedocs.io
- **Telegram Bot API**: https://core.telegram.org/bots/api

## Common Issues

### "Bot token not found"
Make sure you have the correct token from @BotFather and set it in your code or environment.

### "Connection refused"
Ensure your internet connection is working and Telegram servers are accessible.

### "Handler not being called"
Check that your filter conditions match the incoming updates. Use logging to debug.

### "AttributeError: module 'pyfortg' has no attribute..."
Ensure you're using the correct import path. Check the documentation.

## Best Practices

1. ✅ Use environment variables for tokens
2. ✅ Add error handling to all handlers
3. ✅ Use logging for debugging
4. ✅ Test handlers locally before deployment
5. ✅ Use meaningful command names
6. ✅ Provide help text to users
7. ✅ Handle edge cases
8. ✅ Monitor bot performance

Happy botting! 🤖
