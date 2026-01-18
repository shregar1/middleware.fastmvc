# RateLimitMiddleware

Protects your API from abuse with sliding window rate limiting, configurable limits, and custom key functions.

## Installation

```python
from fastmiddleware import (
    RateLimitMiddleware,
    RateLimitConfig,
    RateLimitStore,
    InMemoryRateLimitStore,
)

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import RateLimitMiddleware

app = FastAPI()

# Default: 60 requests per minute
app.add_middleware(RateLimitMiddleware)

```

## Configuration

### RateLimitConfig

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `requests_per_minute` | `int` | `60` | Requests allowed per minute |
| `requests_per_hour` | `int \| None` | `None` | Requests allowed per hour |
| `burst_limit` | `int \| None` | `None` | Maximum burst requests |
| `key_func` | `Callable` | IP-based | Key extraction function |
| `error_message` | `str` | `"Rate limit exceeded"` | Error message |
| `include_headers` | `bool` | `True` | Include rate limit headers |

## Examples

### Basic Rate Limiting

```python
from fastmiddleware import RateLimitMiddleware, RateLimitConfig

config = RateLimitConfig(
    requests_per_minute=100,
    requests_per_hour=1000,
)

app.add_middleware(RateLimitMiddleware, config=config)

```

### Per-User Rate Limiting

```python
from starlette.requests import Request

def get_user_key(request: Request) -> str:
    """Rate limit by authenticated user."""
    if hasattr(request.state, "auth"):
        user_id = request.state.auth.get("user_id", "unknown")
        return f"user:{user_id}"

    # Fall back to IP for unauthenticated requests
    return get_ip_key(request)

def get_ip_key(request: Request) -> str:
    """Rate limit by IP address."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return f"ip:{forwarded.split(',')[0].strip()}"
    return f"ip:{request.client.host if request.client else 'unknown'}"

config = RateLimitConfig(
    requests_per_minute=100,
    key_func=get_user_key,
)

app.add_middleware(RateLimitMiddleware, config=config)

```

### API Key Based Limits

```python
def get_api_key(request: Request) -> str:
    """Rate limit by API key."""
    api_key = request.headers.get("X-API-Key", "")
    if api_key:
        return f"api:{api_key[:16]}"  # Use prefix for privacy
    return get_ip_key(request)

config = RateLimitConfig(
    requests_per_minute=1000,  # Higher limit for API keys
    key_func=get_api_key,
)

```

### Tiered Rate Limits

```python
TIER_LIMITS = {
    "free": 60,
    "pro": 300,
    "enterprise": 1000,
}

def get_tier_key(request: Request) -> str:
    """Rate limit based on user tier."""
    tier = "free"
    if hasattr(request.state, "auth"):
        tier = request.state.auth.get("tier", "free")

    user_id = request.state.auth.get("user_id", "anon") if hasattr(request.state, "auth") else "anon"
    return f"{tier}:{user_id}"

```

### With Burst Limit

```python
config = RateLimitConfig(
    requests_per_minute=60,
    burst_limit=10,  # Allow 10 requests instantly
)

```

## Response Headers

Rate limit information is included in response headers:

| Header | Description | Example |
| -------- | ------------- | --------- |
| `X-RateLimit-Limit` | Maximum requests allowed | `60` |
| `X-RateLimit-Remaining` | Remaining requests | `45` |
| `X-RateLimit-Reset` | Unix timestamp when limit resets | `1704067200` |
| `Retry-After` | Seconds until allowed (when limited) | `30` |

### Normal Response

```http
HTTP/1.1 200 OK
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1704067200

```

### Rate Limited Response

```http
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1704067200
Retry-After: 30
Content-Type: application/json

{
    "detail": "Rate limit exceeded. Try again in 30 seconds."
}

```

## Custom Storage Backend

For distributed systems, implement a custom storage backend:

```python
from fastmiddleware import RateLimitStore

class RedisRateLimitStore(RateLimitStore):
    """Redis-backed rate limit storage."""

    def __init__(self, redis_client):
        self.redis = redis_client

    async def check_rate_limit(
        self,
        key: str,
        limit: int,
        window: int,
    ) -> tuple[bool, int, int]:
        """Check if rate limited and return remaining count."""
        pipe = self.redis.pipeline()
        now = time.time()
        window_start = now - window

        # Remove old entries
        pipe.zremrangebyscore(key, 0, window_start)
        # Count current entries
        pipe.zcard(key)
        # Add current request
        pipe.zadd(key, {str(now): now})
        # Set expiration
        pipe.expire(key, window)

        results = await pipe.execute()
        current_count = results[1]

        allowed = current_count < limit
        remaining = max(0, limit - current_count - 1)
        reset_time = int(now + window)

        return allowed, remaining, reset_time

    async def record_request(self, key: str) -> None:
        """Record a request (already done in check_rate_limit)."""
        pass

# Usage
import redis.asyncio as redis

redis_client = redis.from_url("redis://localhost")
store = RedisRateLimitStore(redis_client)

app.add_middleware(
    RateLimitMiddleware,
    store=store,
    config=RateLimitConfig(requests_per_minute=100),
)

```

## Path Exclusion

Exclude paths from rate limiting:

```python
app.add_middleware(
    RateLimitMiddleware,
    exclude_paths={"/health", "/metrics", "/docs"},
)

```

## Best Practices

1. **Use Redis for distributed systems** - In-memory store doesn't share across instances
2. **Rate limit by user, not just IP** - Shared IPs affect multiple users
3. **Set reasonable limits** - Too strict causes friction, too loose allows abuse
4. **Exclude health checks** - Don't rate limit monitoring
5. **Log rate limit events** - Track potential abuse patterns

## Algorithm

This middleware uses the **sliding window** algorithm:

1. Track request timestamps within window
2. Count requests in current window
3. Allow if count < limit
4. Reject with 429 if count >= limit

Benefits over fixed window:

- No burst at window boundaries

- More accurate rate enforcement

- Smoother rate limiting experience

## Related Middlewares

- [AuthenticationMiddleware](./authentication.md) - Authenticate before rate limiting
- [RequestIDMiddleware](./request-id.md) - Track rate limited requests
- [MetricsMiddleware](./metrics.md) - Monitor rate limit events
