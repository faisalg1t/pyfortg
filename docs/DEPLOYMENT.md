# Deployment Guide

This guide covers deploying PyForTG bots to various platforms.

## Local Development

### Prerequisites
- Python 3.9+
- Redis (optional, for sessions)
- PostgreSQL (optional, for persistent data)

### Setup

```bash
# Clone repository
git clone <your-repo>
cd pyfortg

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install with all extras
pip install -e ".[all]"

# Copy .env.example to .env and set your token
cp .env.example .env

# Run bot
python bot.py
```

## Docker Deployment

### Single Bot Container

```bash
# Build image
docker build -t my-bot:latest .

# Run bot
docker run -e BOT_TOKEN=your_token my-bot

# With storage
docker run \
  -e BOT_TOKEN=your_token \
  -e REDIS_URL=redis://redis:6379 \
  -e POSTGRES_DSN=postgresql://user:pass@postgres/db \
  my-bot
```

### Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f bot

# Stop services
docker-compose down
```

The `docker-compose.yml` includes Redis and PostgreSQL setup.

## VPS Deployment

### Using systemd

Create `/etc/systemd/system/telegram-bot.service`:

```ini
[Unit]
Description=Telegram Bot Service
After=network.target

[Service]
Type=simple
User=botuser
WorkingDirectory=/home/botuser/pyfortg
Environment="BOT_TOKEN=your_token"
Environment="REDIS_URL=redis://localhost:6379"
ExecStart=/home/botuser/pyfortg/venv/bin/python bot.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then:

```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
sudo systemctl status telegram-bot
```

### Using Supervisor

Create `/etc/supervisor/conf.d/telegram-bot.conf`:

```ini
[program:telegram-bot]
command=/home/botuser/pyfortg/venv/bin/python /home/botuser/pyfortg/bot.py
directory=/home/botuser/pyfortg
user=botuser
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/telegram-bot.log
environment=BOT_TOKEN="your_token"
```

Then:

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start telegram-bot
```

## Cloud Platforms

### Heroku

Create `Procfile`:

```
worker: python bot.py
```

Deploy:

```bash
heroku login
heroku create my-telegram-bot
heroku addons:create heroku-postgresql:hobby-dev
heroku addons:create heroku-redis:premium-0
git push heroku main
heroku config:set BOT_TOKEN=your_token
heroku ps:scale worker=1
```

### Railway

Create `railway.toml`:

```toml
[build]
builder = "dockerfile"

[deploy]
startCommand = "python bot.py"
```

Deploy:

```bash
railway link
railway up
```

### AWS Lambda with Webhooks

```python
# lambda_handler.py
import json
from pyfortg import TelegramBot, Filters

bot = TelegramBot(token="YOUR_TOKEN")

@bot.on_message(Filters.text)
async def handle_text(bot, update, context):
    await bot.send_message(...)

def lambda_handler(event, context):
    import asyncio
    update = json.loads(event['body'])
    asyncio.run(bot.process_update(update))
    return {"statusCode": 200}
```

Configure:
1. Create API Gateway endpoint
2. Set webhook: `await bot.set_webhook(url="<api_gateway_url>")`
3. Deploy Lambda function

### Google Cloud Run

Create `.gcloudignore`:

```
venv
__pycache__
*.pyc
.git
```

Deploy:

```bash
gcloud run deploy pyfortg-bot \
  --source . \
  --platform managed \
  --region us-central1 \
  --set-env-vars BOT_TOKEN=your_token,POSTGRES_DSN=...
```

### DigitalOcean App Platform

Create `.do/app.yaml`:

```yaml
name: pyfortg-bot
services:
  - name: bot
    github:
      repo: pyfortg/pyfortg
      branch: main
    build_command: pip install -e ".[all]"
    run_command: python bot.py
    envs:
      - key: BOT_TOKEN
        scope: RUN_AND_BUILD_TIME
        value: ${BOT_TOKEN}
```

Deploy:

```bash
doctl apps create --spec .do/app.yaml
```

## Production Best Practices

### Environment Configuration

Never hardcode tokens. Use environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not set")
```

### Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
```

### Error Handling

```python
try:
    await bot.send_message(...)
except Exception as e:
    logger.error(f"Error sending message: {e}")
    # Handle gracefully
```

### Health Monitoring

```python
@bot.on_command("health")
async def health_check(bot, update, context):
    # Check database, storage, etc.
    status = "OK"
    await bot.send_message(
        chat_id=update.message.chat.id,
        text=f"Health: {status}"
    )
```

### Performance Optimization

1. **Use connection pooling** for databases
2. **Cache frequently accessed data** with Redis
3. **Batch API calls** when possible
4. **Use webhooks** instead of polling for production
5. **Monitor bot performance** with logging

### Webhooks vs Polling

**Polling** (simpler):
```python
await bot.run_polling()
```

**Webhooks** (production):
```python
await bot.set_webhook(url="https://example.com/webhook")
await bot.run_webhook(host="0.0.0.0", port=8080)
```

### Database Migrations

For PostgreSQL:

```bash
# Create migration script
psql -U botuser -d botdb -f migrations/001_init.sql

# Or use SQLAlchemy/Alembic for complex migrations
alembic init alembic
alembic revision --autogenerate -m "Initial"
alembic upgrade head
```

## Scaling Multiple Bots

Use a supervisor or orchestration:

```yaml
# docker-compose.yml for multiple bots
services:
  bot1:
    build: .
    environment:
      BOT_TOKEN: ${BOT_TOKEN_1}
      
  bot2:
    build: .
    environment:
      BOT_TOKEN: ${BOT_TOKEN_2}
      
  shared-redis:
    image: redis:7-alpine
```

## Monitoring and Alerts

### Logging

```python
import logging

logger = logging.getLogger(__name__)
logger.info("Bot started")
logger.error("Error occurred", exc_info=True)
```

### Metrics

```python
from datetime import datetime

class BotMetrics:
    messages_processed = 0
    errors = 0
    
    @classmethod
    def record_message(cls):
        cls.messages_processed += 1
        
    @classmethod
    def record_error(cls):
        cls.errors += 1
```

### External Monitoring

- **Sentry** - Error tracking
- **New Relic** - Performance monitoring
- **Datadog** - Infrastructure monitoring
- **CloudWatch** - AWS monitoring

## Backup and Recovery

### PostgreSQL

```bash
# Backup
pg_dump -U botuser botdb > backup.sql

# Restore
psql -U botuser botdb < backup.sql
```

### Redis

```bash
# Enable persistence in redis.conf
appendonly yes

# Manual backup
redis-cli BGSAVE
```

## Troubleshooting

### Bot Not Responding

1. Check bot token validity
2. Verify internet connectivity
3. Check logs for errors
4. Verify webhook URL (if using webhooks)

### Database Connection Issues

1. Verify connection string
2. Check database is running
3. Check firewall/network rules
4. Verify credentials

### Memory Issues

1. Monitor memory usage
2. Implement cleanup routines
3. Use caching appropriately
4. Monitor storage size

## Rollback Procedure

```bash
# With git
git revert <commit>
git push

# With docker
docker pull my-bot:previous-version
docker run my-bot:previous-version
```

## Next Steps

1. Choose your deployment platform
2. Set up monitoring and logging
3. Configure backups
4. Test failover procedures
5. Document deployment process

For more help, see the full [documentation](INDEX.md).
