# PyForTG Documentation Index

Welcome to the PyForTG documentation! This index will help you navigate all available resources.

## Quick Links

- **[Getting Started](GETTING_STARTED.md)** - Start here! Create your first bot in 5 minutes
- **[Installation](INSTALLATION.md)** - Install PyForTG and its dependencies
- **[API Reference](API_REFERENCE.md)** - Complete API documentation
- **[Storage Guide](STORAGE.md)** - Setup Redis and PostgreSQL
- **[Examples](#examples)** - Real-world bot examples

## Documentation

### For Beginners

1. **[Getting Started](GETTING_STARTED.md)**
   - Create a Telegram bot token
   - Install PyForTG
   - Build your first bot
   - Common patterns and use cases

2. **[Installation](INSTALLATION.md)**
   - PyPI installation
   - Development setup
   - Optional dependencies
   - Docker setup

### For Development

3. **[API Reference](API_REFERENCE.md)**
   - TelegramBot methods
   - Handlers (message, command, callback)
   - Filters and filtering
   - Keyboards and UI components
   - Middleware system
   - Update types

4. **[Storage Guide](STORAGE.md)**
   - Redis setup and usage
   - PostgreSQL setup and usage
   - Combining storage backends
   - Backup and recovery

### For Contributors

5. **[Contributing Guide](../CONTRIBUTING.md)**
   - Development environment setup
   - Code style guidelines
   - Testing procedures
   - Pull request process

## Examples

### Example Bots

Located in `/examples/`:

1. **01_basic_bot.py** - Simple bot with basic commands
   - /start command
   - /help command
   - Echo messages
   - **Best for:** Learning fundamentals

2. **02_advanced_bot.py** - More complex features
   - Keyboard interactions
   - Multiple handlers
   - Filter combinations
   - **Best for:** Understanding features

3. **03_webhook_bot.py** - Production setup
   - Webhook instead of polling
   - Error handling
   - Logging
   - **Best for:** Production deployments

4. **04_stateful_bot.py** - User state management
   - Redis storage
   - Conversation flows
   - State machines
   - **Best for:** Complex conversations

5. **05_media_bot.py** - Media handling
   - Photo processing
   - Document handling
   - Video/audio processing
   - File download/upload
   - **Best for:** Media bots

6. **06_production_bot.py** - Production template
   - PostgreSQL storage
   - Middleware system
   - Error handling
   - Logging
   - Environment variables
   - **Best for:** Production bots

## Features

### Core Features

- ✅ Full Telegram Bot API support
- ✅ Async/await syntax
- ✅ Decorator-based routing
- ✅ Advanced filter system
- ✅ Keyboard builders (inline & reply)
- ✅ Middleware system
- ✅ Type hints throughout

### Storage

- ✅ Redis backend (caching, sessions)
- ✅ PostgreSQL backend (persistent data)
- ✅ Custom storage implementations

### Deployment

- ✅ Long polling
- ✅ Webhook support
- ✅ Docker ready
- ✅ Environment configuration

## Architecture

### Package Structure

```
pyfortg/
├── client/              # Core Telegram API client
│   ├── base.py         # BaseClient with API methods
│   ├── bot.py          # High-level TelegramBot
│   └── __init__.py
│
├── handlers/            # Update handlers
│   ├── base.py         # Base handler classes
│   └── __init__.py
│
├── middleware/          # Request/response middleware
│   ├── base.py         # BaseMiddleware
│   └── __init__.py
│
├── storage/             # Data storage backends
│   ├── base.py         # StorageBackend interface
│   ├── redis.py        # Redis implementation
│   ├── postgres.py     # PostgreSQL implementation
│   └── __init__.py
│
├── keyboards.py         # Keyboard builders
├── filters.py          # Filter system
├── types.py            # Type definitions
├── exceptions.py       # Custom exceptions
├── utils/              # Utility functions
│   ├── validators.py   # Input validation
│   ├── text.py         # Text utilities
│   └── __init__.py
└── __init__.py
```

## Common Use Cases

### Simple Bot (Polling)
See: **01_basic_bot.py** or **Getting Started**

```python
bot = TelegramBot(token="YOUR_TOKEN")
@bot.on_command("start")
async def handle_start(bot, update, context):
    await bot.send_message(...)
await bot.run_polling()
```

### Interactive Bot with Buttons
See: **02_advanced_bot.py** or **05_media_bot.py**

```python
keyboard = InlineKeyboardMarkup()
keyboard.add_button("Click me", callback_data="btn_1")
await bot.send_message(..., reply_markup=keyboard)
```

### Production Bot with Storage
See: **06_production_bot.py** or **Storage Guide**

```python
storage = RedisStorage(url="redis://localhost")
user_data = await storage.get(f"user:{user_id}")
```

### Webhook Deployment
See: **03_webhook_bot.py**

```python
await bot.set_webhook(url="https://example.com/webhook")
await bot.run_webhook(host="0.0.0.0", port=8080)
```

## API Overview

### Main Classes

- **TelegramBot** - Main bot class
- **Filters** - Message filtering system
- **InlineKeyboardMarkup** - Inline keyboard builder
- **ReplyKeyboardMarkup** - Reply keyboard builder
- **RedisStorage** - Redis backend
- **PostgresStorage** - PostgreSQL backend
- **BaseMiddleware** - Middleware base class

### Main Methods

- `send_message()` - Send text messages
- `send_photo/video/audio/document()` - Send media
- `edit_message_text()` - Edit sent messages
- `delete_message()` - Delete messages
- `answer_callback_query()` - Respond to button clicks
- `download_file()` - Download files
- `set_webhook()` - Setup webhook
- `run_polling()` - Start polling
- `run_webhook()` - Start webhook server

### Decorators

- `@bot.on_message()` - Handle messages
- `@bot.on_command()` - Handle commands
- `@bot.on_callback_query()` - Handle button clicks

## Troubleshooting

### Bot Doesn't Respond

1. Check bot token is correct
2. Verify internet connection
3. Check handler filters
4. Enable logging: `logging.basicConfig(level=logging.DEBUG)`

### Storage Connection Issues

1. Verify Redis/PostgreSQL is running
2. Check connection string
3. Look at error messages
4. See **Storage Guide** for details

### Deployment Issues

1. Check environment variables are set
2. Verify network/firewall rules
3. Check logs for errors
4. See **Installation** for Docker setup

## Getting Help

1. **Check the documentation** - This guide
2. **Look at examples** - Real working code
3. **GitHub Issues** - Report bugs or ask questions
4. **Telegram Bot API Docs** - For API details

## Related Resources

- [Telegram Bot API](https://core.telegram.org/bots/api) - Official API documentation
- [Python asyncio](https://docs.python.org/3/library/asyncio.html) - Async programming
- [aiohttp](https://docs.aiohttp.org/) - HTTP client library
- [Redis Documentation](https://redis.io/documentation) - Redis guide
- [PostgreSQL Documentation](https://www.postgresql.org/docs/) - Database guide

## Version History

See [CHANGELOG.md](../CHANGELOG.md) for detailed version history.

## License

PyForTG is licensed under the MIT License. See [LICENSE](../LICENSE) for details.
