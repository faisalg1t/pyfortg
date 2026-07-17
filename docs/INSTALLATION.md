# Installation Guide

## PyPI Installation (Recommended)

### Basic Installation

```bash
pip install pyfortg
```

### With Optional Dependencies

#### Redis Support
```bash
pip install pyfortg[redis]
```

#### PostgreSQL Support
```bash
pip install pyfortg[postgres]
```

#### All Extras
```bash
pip install pyfortg[all]
```

## Development Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/pyfortg/pyfortg.git
cd pyfortg

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with all extras
pip install -e ".[dev,all]"
```

## Verification

Verify the installation:

```python
import pyfortg

print(pyfortg.__version__)
print(pyfortg.__all__)
```

## System Requirements

- **Python Version:** 3.9 or higher
- **Operating System:** Linux, macOS, Windows
- **RAM:** Minimum 256MB (2GB+ recommended for production)
- **Network:** Internet connection for Telegram Bot API

## Optional Dependencies

### Redis (for session management)
```bash
pip install aioredis>=2.0.0
```

### PostgreSQL (for persistent storage)
```bash
pip install asyncpg>=0.27.0
```

## Quick Start After Installation

```python
from pyfortg import TelegramBot, Filters

# Create bot
bot = TelegramBot(token="YOUR_BOT_TOKEN")

# Register handler
@bot.on_message(Filters.text)
async def handle_text(bot, update, context):
    await bot.send_message(
        chat_id=update.message.chat.id,
        text="Hello!"
    )

# Run bot
if __name__ == "__main__":
    bot.run_polling()
```

## Troubleshooting

### ImportError: No module named 'pyfortg'
- Ensure you have installed the package: `pip install pyfortg`
- Check Python version: `python --version` (requires 3.9+)

### Redis connection error
- Install Redis: `sudo apt-get install redis-server` (Linux)
- Or use: `pip install pyfortg[redis]` for the driver

### PostgreSQL connection error
- Install asyncpg: `pip install asyncpg`
- Ensure PostgreSQL server is running
- Verify connection parameters in your code

## Virtual Environment Setup (Recommended)

```bash
# Create virtual environment
python -m venv mybot_env

# Activate it
source mybot_env/bin/activate  # Linux/macOS
# or
mybot_env\Scripts\activate  # Windows

# Install PyForTG
pip install pyfortg[all]
```

## Docker Installation

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN pip install pyfortg[all]

COPY . .

CMD ["python", "bot.py"]
```

Build and run:
```bash
docker build -t my-telegram-bot .
docker run -e BOT_TOKEN=YOUR_TOKEN my-telegram-bot
```
