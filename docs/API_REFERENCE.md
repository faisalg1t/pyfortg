# API Reference

## TelegramBot

Main bot class for handling Telegram Bot API interactions.

### Initialization

```python
from pyfortg import TelegramBot

bot = TelegramBot(
    token="YOUR_BOT_TOKEN",
    timeout=30,
    request_kwargs={}
)
```

**Parameters:**
- `token` (str): Telegram Bot API token
- `timeout` (int): Request timeout in seconds (default: 30)
- `request_kwargs` (dict): Additional kwargs for aiohttp client

### Methods

#### send_message()

```python
await bot.send_message(
    chat_id=123456,
    text="Hello!",
    parse_mode="HTML",
    reply_markup=keyboard
)
```

#### send_photo()

```python
await bot.send_photo(
    chat_id=123456,
    photo="file_id_or_url",
    caption="Photo caption"
)
```

#### send_document()

```python
await bot.send_document(
    chat_id=123456,
    document="file_path_or_url"
)
```

#### send_video()

```python
await bot.send_video(
    chat_id=123456,
    video="file_path_or_url",
    duration=120
)
```

#### send_audio()

```python
await bot.send_audio(
    chat_id=123456,
    audio="file_path_or_url",
    title="Song Title"
)
```

#### edit_message_text()

```python
await bot.edit_message_text(
    chat_id=123456,
    message_id=789,
    text="Updated text",
    reply_markup=keyboard
)
```

#### delete_message()

```python
await bot.delete_message(chat_id=123456, message_id=789)
```

#### answer_callback_query()

```python
await bot.answer_callback_query(
    callback_query_id="callback_id",
    text="Notification",
    show_alert=False
)
```

#### get_file()

```python
file_info = await bot.get_file(file_id)
file_path = file_info['file_path']
```

#### download_file()

```python
file_bytes = await bot.download_file(file_id)
```

#### set_webhook()

```python
await bot.set_webhook(
    url="https://example.com/webhook",
    certificate=None,
    max_connections=100
)
```

#### delete_webhook()

```python
await bot.delete_webhook()
```

#### run_polling()

```python
await bot.run_polling(
    timeout=30,
    allowed_updates=["message", "callback_query"]
)
```

#### run_webhook()

```python
await bot.run_webhook(
    host="0.0.0.0",
    port=8080,
    webhook_path="/webhook"
)
```

## Handlers

### Message Handler

```python
@bot.on_message(Filters.text)
async def handle_message(bot, update, context):
    await bot.send_message(
        chat_id=update.message.chat.id,
        text=f"You said: {update.message.text}"
    )
```

### Command Handler

```python
@bot.on_command("start")
async def handle_start(bot, update, context):
    await bot.send_message(
        chat_id=update.message.chat.id,
        text="Welcome!"
    )
```

### Callback Handler

```python
@bot.on_callback_query()
async def handle_callback(bot, update, context):
    callback_data = update.callback_query.data
    await bot.answer_callback_query(
        callback_query_id=update.callback_query.id,
        text=f"You pressed: {callback_data}"
    )
```

## Filters

### Basic Filters

```python
from pyfortg import Filters

# Text messages
Filters.text

# Commands
Filters.command

# Media
Filters.photo
Filters.video
Filters.document
Filters.audio

# Custom filter
Filters.custom(lambda msg: len(msg.text) > 10)
```

### Filter Combinations

```python
# AND operator
Filters.text & Filters.from_user(user_id=123)

# OR operator
Filters.photo | Filters.video

# NOT operator
~Filters.command
```

## Keyboards

### InlineKeyboard

```python
from pyfortg.keyboards import InlineKeyboardMarkup, InlineKeyboardButton

keyboard = InlineKeyboardMarkup()
keyboard.add_button("Click me", callback_data="button_1")
keyboard.add_button("Go to Google", url="https://google.com")
keyboard.row()  # New row
keyboard.add_button("Cancel", callback_data="cancel")
```

### ReplyKeyboard

```python
from pyfortg.keyboards import ReplyKeyboardMarkup, KeyboardButton

keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
keyboard.add_button("Option 1")
keyboard.add_button("Option 2")
keyboard.row()
keyboard.add_button("Cancel")
```

## Middleware

### Creating Custom Middleware

```python
from pyfortg.middleware import BaseMiddleware

class LoggingMiddleware(BaseMiddleware):
    async def pre_process(self, bot, update, context):
        print(f"Processing update: {update.update_id}")
        return update

    async def post_process(self, bot, update, context, result):
        print("Update processed")
        return result

# Register middleware
bot.add_middleware(LoggingMiddleware())
```

## Storage

### Redis Storage

```python
from pyfortg.storage import RedisStorage

storage = RedisStorage(url="redis://localhost")
await storage.set("user_123", {"name": "John"})
user = await storage.get("user_123")
```

### PostgreSQL Storage

```python
from pyfortg.storage import PostgresStorage

storage = PostgresStorage(dsn="postgresql://user:pass@localhost/botdb")
await storage.connect()
await storage.set("user_123", {"name": "John"})
```

## Update Types

### Message

```python
update.message.message_id
update.message.chat.id
update.message.from_user.id
update.message.text
update.message.photo
update.message.video
update.message.document
```

### CallbackQuery

```python
update.callback_query.id
update.callback_query.from_user.id
update.callback_query.message.message_id
update.callback_query.data
```

## Exceptions

```python
from pyfortg.exceptions import (
    PyForTGError,
    APIError,
    ValidationError,
    NetworkError,
    TimeoutError
)
```
