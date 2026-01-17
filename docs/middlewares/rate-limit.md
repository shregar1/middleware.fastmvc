# RateLimitMiddleware

Protects your API from abuse with configurable rate limiting using a sliding window algorithm.

## Installation

```python
from src import RateLimitMiddleware, RateLimitConfig
```

## Quick Start

```python
from fastapi import FastAPI
from src import RateLimitMiddleware

app = FastAPI()

# Default: 60 requests per minute
app.add_middleware(RateLimitMiddleware)
```

## Configuration

### RateLimitConfig

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `requests_per_minute` | `int` | `60` | Requests allowed per minute |
| `requests_per_hour` | `int \| None` | `None` | Requests allowed per hour |
| `burst_limit` | `int \| None` | `None` | Maximum burst requests |
| `key_func` | `Callable` | IP-based | Function to extract rate limit key |
| `error_message` | `str` | `"Rate limit exceeded"` | Error message |
| `error_status_code` | `int` | `429` | Too Many Requests status |

## Response Headers

| Header | Description |
|--------|-------------|
| `X-RateLimit-Limit` | Maximum requests allowed |
| `X-RateLimit-Remaining` | Requests remaining in window |
| `X-RateLimit-Reset` | Unix timestamp when limit resets |
| `Retry-After` | Seconds until retry (when limited) |

## Examples

### Basic Rate Limiting

```python
from src import RateLimitMiddleware, RateLimitConfig

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
    """Rate limit by user ID if authenticated."""
    if hasattr(request.state, "auth"):
        user_id = request.state.auth.get("sub", "unknown")
        return f"user:{user_id}"
    
    # Fall back to IP address
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

### Per-API-Key Rate Limiting

```python
def get_api_key(request: Request) -> str:
    """Rate limit by API key."""
    api_key = request.headers.get("X-API-Key", "anonymous")
    return f"api:{api_key}"

config = RateLimitConfig(
    requests_per_minute=1000,
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

def get_tiered_key(request: Request) -> str:
    tier = "free"
    if hasattr(request.state, "auth"):
        tier = request.state.auth.get("tier", "free")
    
    user_id = request.state.auth.get("sub", "anon") if hasattr(request.state, "auth") else "anon"
    return f"{tier}:{user_id}"

# Note: For different limits per tier, use multiple instances
# or implement custom logic in the key function
```

### Exclude Paths

```python
app.add_middleware(
    RateLimitMiddleware,
    config=config,
    exclude_paths={"/health", "/metrics", "/docs"},
)
```

## Custom Storage Backend

```python
from src import RateLimitStore

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
        """Check if rate limited.
        
        Returns:
            (is_allowed, remaining, reset_time)
        """
        current = await self.redis.get(f"rate:{key}")
        # Implement sliding window logic
        ...
    
    async def record_request(self, key: str, window: int) -> None:
        """Record a request."""
        await self.redis.incr(f"rate:{key}")
        await self.redis.expire(f"rate:{key}", window)

# Use custom store
store = RedisRateLimitStore(redis_client)
app.add_middleware(RateLimitMiddleware, store=store)
```

## Response Examples

### Normal Response

```http
HTTP/1.1 200 OK
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1704067260
```

### Rate Limited Response

```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/json
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1704067260
Retry-After: 45

{
    "detail": "Rate limit exceeded"
}
```

## Client Handling

### JavaScript Example

```javascript
async function fetchWithRetry(url, options = {}) {
    const response = await fetch(url, options);
    
    if (response.status === 429) {
        const retryAfter = response.headers.get('Retry-After');
        const waitTime = parseInt(retryAfter) * 1000;
        
        console.log(`Rate limited. Retrying in ${retryAfter}s`);
        await new Promise(r => setTimeout(r, waitTime));
        
        return fetchWithRetry(url, options);
    }
    
    return response;
}
```

### Python Example

```python
import httpx
import asyncio

async def request_with_retry(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            await asyncio.sleep(retry_after)
            return await request_with_retry(url)
        
        return response
```

## Best Practices

1. **Set reasonable limits** - Balance protection with usability
2. **Use per-user limits** when possible - Fairer than IP-based
3. **Implement tiered limits** - Different limits for different plans
4. **Exclude health checks** - Don't rate limit monitoring
5. **Monitor rate limit hits** - Track abuse patterns
6. **Document limits** - Let API consumers know the limits

## Related

- [AuthenticationMiddleware](authentication.md) - Authentication
- [IdempotencyMiddleware](idempotency.md) - Safe retries

