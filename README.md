# PyForTG - Production-Ready Telegram Bot Framework

[![PyPI version](https://badge.fury.io/py/pyfortg.svg)](https://badge.fury.io/py/pyfortg)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A high-performance, production-ready Python framework for building Telegram bots with async-first architecture, webhook support, and built-in database backends.

## Features

✨ **Production Ready**
- Async-first architecture using asyncio and aiohttp
- High-concurrency support with webhooks and long-polling
- Comprehensive error handling and logging
- Type hints with Pydantic validation
- Thread-safe operations

🎯 **Developer Friendly**
- Decorator-based routing (@bot.on_message, @bot.on_command, @bot.on_callback)
- Filter system for message routing (text, command, callback, file types, etc.)
- Middleware support for request/response processing
- Built-in rate limiting and logging middleware
- Simple, intuitive API

💾 **Storage & State**
- Memory storage for development
- Redis backend for caching and sessions
- PostgreSQL backend for persistent data
- User state management
- Session handling

🎮 **Rich UI Components**
- Inline keyboards with buttons
- Reply keyboards with shortcuts
- Callback query handling
- File upload/download support
- Message editing and deletion

📡 **Telegram Bot API**
- Full coverage of Telegram Bot API methods
- Message sending (text, photo, audio, video, document)
- File handling and downloads
- User profile management
- Chat operations

## Installation

### From PyPI

```bash
pip install pyfortg

# With Redis support
pip install pyfortg[redis]

# With PostgreSQL support
pip install pyfortg[postgres]

# With all features
pip install pyfortg[full]
```

### From GitHub

```bash
git clone https://github.com/pyfortg/pyfortg.git
cd pyfortg
pip install -e .
```

## Quick Start

### Basic Bot

```python
import asyncio
from pyfortg import TelegramBot, Filters, InlineKeyboard

async def main():
    bot = TelegramBot(token="YOUR_BOT_TOKEN")
    
    @bot.on_command("start")
    async def start(bot, message):
        keyboard = InlineKeyboard()
        keyboard.add_button("Click me!", callback_data="btn_1")
        
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"Hello {message.from_user.first_name}!",
            reply_markup=keyboard.to_dict(),
        )
    
    @bot.on_callback()
    async def callback_handler(bot, callback):
        await bot.answer_callback_query(
            callback_query_id=callback.id,
            text="Button clicked!",
        )
    
    await bot.initialize()
    await bot.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
```

### With Storage

```python
from pyfortg import TelegramBot
from pyfortg.storage import RedisStorage  # or PostgresStorage

async def main():
    storage = RedisStorage("redis://localhost:6379")
    bot = TelegramBot(token="YOUR_BOT_TOKEN", storage=storage)
    
    @bot.on_command("start")
    async def start(bot, message):
        user_id = message.from_user.id
        
        # Store user data
        await storage.set_user_data(user_id, {
            "name": message.from_user.first_name,
            "username": message.from_user.username,
        })
        
        # Retrieve user data
        user_data = await storage.get_user_data(user_id)
        
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"Welcome {user_data['name']}!",
        )
    
    await bot.initialize()
    await bot.start_polling()
```

### Webhook Setup

```python
from fastapi import FastAPI, Request
from pyfortg import TelegramBot
import uvicorn

app = FastAPI()
bot = TelegramBot(token="YOUR_BOT_TOKEN")

@bot.on_command("start")
async def start(bot, message):
    await bot.send_message(
        chat_id=message.chat.id,
        text="Hello from webhook!",
    )

@app.post("/webhook")
async def webhook(request: Request):
    update = await request.json()
    await bot.handle_webhook_update(update)
    return {"ok": True}

# Set webhook: curl -X POST http://localhost:8000/set-webhook?webhook_url=https://yourserver.com/webhook
# Then run: uvicorn app:app --host 0.0.0.0 --port 8000
```

## Message Handling

### Commands

```python
@bot.on_command("start", "help", "about")
async def handle_commands(bot, message):
    await bot.send_message(
        chat_id=message.chat.id,
        text="Command received!",
    )
```

### Message Text Filters

```python
@bot.on_message(Filters.text("hello", "hi"))
async def greet(bot, message):
    await bot.send_message(
        chat_id=message.chat.id,
        text="Hello there!",
    )

# Regex pattern matching
@bot.on_message(Filters.text(pattern=r"^\d{3}-\d{3}-\d{4}$"))
async def phone_number(bot, message):
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"Valid phone: {message.text}",
    )
```

### Callback Queries

```python
@bot.on_callback(Filters.callback_query(data_pattern=r"action_\d+"))
async def handle_callback(bot, callback):
    await bot.answer_callback_query(
        callback_query_id=callback.id,
        text="Action received!",
    )
```

### File Handling

```python
@bot.on_message(Filters.file_type(["photo", "document"]))
async def handle_files(bot, message):
    file_id = None
    if message.photo:
        file_id = message.photo[0].file_id
    elif message.document:
        file_id = message.document.file_id
    
    file_url = await bot.get_file_url(file_id)
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"File: {file_url}",
    )
```

### Chat Type Filters

```python
@bot.on_message(Filters.private_chat())
async def private_only(bot, message):
    await bot.send_message(
        chat_id=message.chat.id,
        text="Private chat only!",
    )

@bot.on_message(Filters.group_chat())
async def group_only(bot, message):
    await bot.send_message(
        chat_id=message.chat.id,
        text="Group message!",
    )
```

## Keyboards

### Inline Keyboard

```python
keyboard = InlineKeyboard()
keyboard.add_button("Option 1", callback_data="opt_1")
keyboard.add_button("Option 2", callback_data="opt_2")
keyboard.row()  # New row
keyboard.add_button("Google", url="https://google.com")

await bot.send_message(
    chat_id=chat_id,
    text="Choose an option:",
    reply_markup=keyboard.to_dict(),
)
```

### Reply Keyboard

```python
from pyfortg import ReplyKeyboard

keyboard = ReplyKeyboard(one_time_keyboard=True)
keyboard.add_button("Yes")
keyboard.add_button("No")
keyboard.row()
keyboard.add_contact_button("Share Contact")

await bot.send_message(
    chat_id=chat_id,
    text="Make a choice:",
    reply_markup=keyboard.to_dict(),
)
```

## Middleware

```python
from pyfortg.middleware import Middleware, LoggingMiddleware, RateLimitMiddleware

# Add built-in middleware
bot.middleware_chain.add_middleware(LoggingMiddleware())
bot.middleware_chain.add_middleware(RateLimitMiddleware(requests_per_second=10))

# Custom middleware
class MyMiddleware(Middleware):
    async def process(self, update):
        print(f"Processing update {update.update_id}")
        return update

bot.middleware_chain.add_middleware(MyMiddleware())
```

## State Management

```python
# Set user state
await storage.set_user_state(user_id, "waiting_for_name")

# Get user state
state = await storage.get_user_state(user_id)

# User data
await storage.set_user_data(user_id, {"name": "John"})
data = await storage.get_user_data(user_id)

# Update data
await storage.update_user_data(user_id, {"age": 25})
```

## Sending Messages

```python
# Send text message
await bot.send_message(
    chat_id=chat_id,
    text="Hello!",
    parse_mode="HTML",  # or Markdown, MarkdownV2
)

# Send with keyboard
await bot.send_message(
    chat_id=chat_id,
    text="Choose:",
    reply_markup=keyboard.to_dict(),
)

# Send photo
await bot.send_photo(
    chat_id=chat_id,
    photo="file_id_or_url",
    caption="My photo",
)

# Send document
await bot.send_document(
    chat_id=chat_id,
    document="file_id_or_url",
    caption="My document",
)

# Edit message
await bot.edit_message_text(
    chat_id=chat_id,
    message_id=message_id,
    text="Edited text",
)

# Delete message
await bot.delete_message(
    chat_id=chat_id,
    message_id=message_id,
)
```

## Error Handling

```python
from pyfortg.exceptions import APIException, ValidationException, PyForTGException

try:
    await bot.send_message(chat_id=chat_id, text="Hello")
except APIException as e:
    print(f"API Error {e.error_code}: {e.description}")
except ValidationException as e:
    print(f"Validation error: {e}")
except PyForTGException as e:
    print(f"PyForTG error: {e}")
```

## Configuration

### Environment Variables

```bash
# Bot token
BOT_TOKEN=123456789:ABCdEfGhIjKlMnOpQrStUvWxYz

# Redis configuration
REDIS_URL=redis://localhost:6379
REDIS_DB=0

# PostgreSQL configuration
DATABASE_URL=postgresql://user:password@localhost/pyfortg
```

### Storage Configuration

```python
# Memory storage
from pyfortg.storage import MemoryStorage
storage = MemoryStorage()

# Redis storage
from pyfortg.storage import RedisStorage
storage = RedisStorage(
    url="redis://localhost:6379",
    db=0,
    prefix="mybot:",
)

# PostgreSQL storage
from pyfortg.storage import PostgresStorage
storage = PostgresStorage(
    dsn="postgresql://user:password@localhost/pyfortg",
    table_name="bot_storage",
)
```

## Examples

See the `examples/` directory for complete working examples:

1. **01_basic_bot.py** - Simple bot with commands and callbacks
2. **02_advanced_bot.py** - Advanced features with storage and state
3. **03_webhook_bot.py** - Webhook-based bot with FastAPI

## Testing

```bash
# Install dev dependencies
pip install pyfortg[dev]

# Run tests
pytest

# Run with coverage
pytest --cov=pyfortg

# Format code
black pyfortg

# Sort imports
isort pyfortg

# Linting
flake8 pyfortg

# Type checking
mypy pyfortg
```

## Performance Tips

1. **Use Webhooks for Production** - Webhooks are more efficient than polling
2. **Enable Rate Limiting** - Prevent abuse with RateLimitMiddleware
3. **Use Redis for Caching** - Store session data in Redis, not PostgreSQL
4. **Connection Pooling** - Both Redis and PostgreSQL use connection pooling
5. **Async-first** - Always use async handlers for better concurrency

## Deployment

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
```

### Heroku

```bash
git push heroku main
# Set webhook via Telegram API
curl -X POST https://api.telegram.org/botYOUR_TOKEN/setWebhook \
  -H "Content-Type: application/json" \
  -d '{"url":"https://your-heroku-app.herokuapp.com/webhook"}'
```

### AWS Lambda

```python
# Use webhook-based bot with AWS Lambda + API Gateway
# Deploy as a Docker image or Python function
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Write tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📧 Email: support@pyfortg.dev
- 💬 GitHub Issues: https://github.com/pyfortg/pyfortg/issues
- 📖 Documentation: https://pyfortg.dev

## Changelog

### Version 1.0.0 (Initial Release)

- Full Telegram Bot API support
- Async-first architecture
- Webhook and polling support
- Redis and PostgreSQL backends
- Comprehensive middleware system
- Filter-based routing
- Keyboard builders
- Rate limiting
- Logging

## Acknowledgments

Built with ❤️ for the Telegram bot developer community.

---

**Made with PyForTG** - The future of Telegram bot development in Python 🚀
