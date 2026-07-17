# Storage Backend Configuration

PyForTG supports multiple storage backends for managing user sessions, state, and persistent data.

## Redis Storage

Redis is ideal for caching, session management, and temporary data storage.

### Installation

```bash
pip install pyfortg[redis]
```

### Basic Usage

```python
from pyfortg import TelegramBot
from pyfortg.storage import RedisStorage

# Create bot
bot = TelegramBot(token="YOUR_BOT_TOKEN")

# Initialize Redis storage
storage = RedisStorage(
    url="redis://localhost:6379",
    db=0
)

# Use storage
@bot.on_message(Filters.text)
async def handle_message(bot, update, context):
    user_id = str(update.message.from_user.id)
    
    # Get user data
    user_data = await storage.get(f"user:{user_id}")
    
    if user_data is None:
        user_data = {"count": 0}
    
    # Update counter
    user_data["count"] += 1
    await storage.set(f"user:{user_id}", user_data)
    
    await bot.send_message(
        chat_id=update.message.chat.id,
        text=f"Message count: {user_data['count']}"
    )
```

### Configuration

```python
storage = RedisStorage(
    url="redis://localhost:6379",  # Redis URL
    db=0,                            # Database number
    password=None,                   # Password if required
    encoding="utf-8",                # Encoding for strings
    decode_responses=True            # Auto-decode responses
)
```

### Advanced Features

```python
# Set with expiration (TTL)
await storage.set("session:123", data, ttl=3600)  # 1 hour

# Check existence
exists = await storage.exists("key")

# Delete key
await storage.delete("key")

# Increment counter
await storage.incr("counter")

# Append to list
await storage.append("list:key", item)

# Get list
items = await storage.list_get("list:key")
```

## PostgreSQL Storage

PostgreSQL is best for persistent, relational data storage with ACID guarantees.

### Installation

```bash
pip install pyfortg[postgres]
```

### Setup

First, create the required tables:

```sql
CREATE TABLE IF NOT EXISTS bot_data (
    key VARCHAR(255) PRIMARY KEY,
    value JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_sessions (
    user_id BIGINT PRIMARY KEY,
    session_data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);

CREATE INDEX idx_user_sessions_expires ON user_sessions(expires_at);
```

### Basic Usage

```python
from pyfortg import TelegramBot
from pyfortg.storage import PostgresStorage

bot = TelegramBot(token="YOUR_BOT_TOKEN")

# Initialize PostgreSQL storage
storage = PostgresStorage(
    dsn="postgresql://user:password@localhost:5432/botdb"
)

# Connect (for connection pooling)
await storage.connect()

# Use storage
@bot.on_command("start")
async def handle_start(bot, update, context):
    user_id = update.message.from_user.id
    
    # Get user data
    user_data = await storage.get(f"user:{user_id}")
    
    if user_data is None:
        user_data = {"first_seen": datetime.now().isoformat()}
        await storage.set(f"user:{user_id}", user_data)
    
    await bot.send_message(
        chat_id=update.message.chat.id,
        text="Welcome!"
    )
```

### Configuration

```python
storage = PostgresStorage(
    dsn="postgresql://user:password@localhost:5432/botdb",
    min_size=10,           # Minimum pool size
    max_size=20,           # Maximum pool size
    timeout=5              # Connection timeout
)
```

### Advanced Features

```python
# Execute custom query
result = await storage.execute(
    "SELECT * FROM bot_data WHERE key LIKE $1",
    ("user:%",)
)

# Get all keys with pattern
keys = await storage.get_keys("user:*")

# Delete with pattern
await storage.delete_pattern("session:*")

# Batch operations
await storage.set_many({
    "key1": data1,
    "key2": data2
})
```

## Switching Between Storage Backends

```python
async def setup_storage(storage_type="redis"):
    if storage_type == "redis":
        return RedisStorage(url="redis://localhost")
    elif storage_type == "postgres":
        storage = PostgresStorage(dsn="postgresql://...")
        await storage.connect()
        return storage
    else:
        raise ValueError(f"Unknown storage type: {storage_type}")

# Usage
storage = await setup_storage("postgres")
```

## Best Practices

### Data Organization

```python
# Use prefixes for organization
user_key = f"user:{user_id}"
session_key = f"session:{user_id}"
cache_key = f"cache:{data_type}:{id}"
```

### Error Handling

```python
try:
    data = await storage.get(key)
except Exception as e:
    logger.error(f"Storage error: {e}")
    data = None
```

### Performance Tips

1. **Use Redis for:** Session data, temporary state, caching, real-time features
2. **Use PostgreSQL for:** User profiles, historical data, reports, transactions
3. **Combine both:** Redis for fast access, PostgreSQL for persistence

### Migration Between Backends

```python
async def migrate_redis_to_postgres(redis_storage, postgres_storage):
    """Migrate data from Redis to PostgreSQL"""
    # Get all keys from Redis
    keys = await redis_storage.get_keys("*")
    
    # Copy to PostgreSQL
    for key in keys:
        value = await redis_storage.get(key)
        await postgres_storage.set(key, value)
    
    print(f"Migrated {len(keys)} keys")
```

## Monitoring and Debugging

### Redis Monitoring

```bash
# Connect to Redis CLI
redis-cli

# Check keys
KEYS *

# Get value
GET key_name

# Monitor in real-time
MONITOR
```

### PostgreSQL Monitoring

```bash
# Connect to psql
psql -U user -d botdb

# Check tables
\dt

# Query data
SELECT * FROM bot_data LIMIT 10;

# Check table size
SELECT pg_size_pretty(pg_total_relation_size('bot_data'));
```

## Connection Pooling

### Redis Connection Pool

```python
storage = RedisStorage(
    url="redis://localhost",
    pool_size=10  # Connection pool size
)
```

### PostgreSQL Connection Pool

```python
storage = PostgresStorage(
    dsn="postgresql://...",
    min_size=5,   # Minimum connections
    max_size=20   # Maximum connections
)
```

## Backup and Recovery

### Redis Backup

```bash
# Create backup
redis-cli BGSAVE

# Check backup location
redis-cli CONFIG GET dir
```

### PostgreSQL Backup

```bash
# Full backup
pg_dump -U user botdb > backup.sql

# Restore
psql -U user botdb < backup.sql
```
