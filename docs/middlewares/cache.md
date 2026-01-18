# CacheMiddleware

HTTP caching with ETag generation, conditional requests (304), and cache control headers.

## Installation

```python
from fastmiddleware import CacheMiddleware, CacheConfig, InMemoryCacheStore

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import CacheMiddleware

app = FastAPI()

app.add_middleware(CacheMiddleware)

```

## Configuration

### CacheConfig

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `default_max_age` | `int` | `0` | Default cache time (seconds) |
| `enable_etag` | `bool` | `True` | Generate ETag headers |
| `private` | `bool` | `False` | Use private cache |
| `no_store` | `bool` | `False` | Disable caching |
| `vary_headers` | `tuple` | `("Accept", ...)` | Vary headers |
| `path_rules` | `dict` | `{}` | Path-specific rules |
| `cacheable_methods` | `set` | `{"GET", "HEAD"}` | Methods to cache |
| `cacheable_status_codes` | `set` | `{200, 301, ...}` | Status codes to cache |

## Response Headers

```http
Cache-Control: public, max-age=3600
ETag: "a3f2b8c4d5e6..."
Vary: Accept, Accept-Encoding

```

## Examples

### Basic Caching

```python
from fastmiddleware import CacheMiddleware, CacheConfig

config = CacheConfig(
    default_max_age=300,  # 5 minutes
    enable_etag=True,
)

app.add_middleware(CacheMiddleware, config=config)

```

### Path-Specific Rules

```python
config = CacheConfig(
    default_max_age=60,
    path_rules={
        "/static": {
            "max_age": 86400,  # 1 day
            "public": True,
        },
        "/api/user": {
            "max_age": 0,
            "no_store": True,
            "private": True,
        },
        "/api/public": {
            "max_age": 3600,
            "public": True,
        },
    },
)

app.add_middleware(CacheMiddleware, config=config)

```

### Private Cache (User-Specific Data)

```python
config = CacheConfig(
    default_max_age=300,
    private=True,  # Only browser can cache, not CDN
)

app.add_middleware(CacheMiddleware, config=config)

```

### No Store (Sensitive Data)

```python
config = CacheConfig(
    no_store=True,  # Never cache
)

app.add_middleware(CacheMiddleware, config=config)

```

### Immutable Assets

```python
config = CacheConfig(
    path_rules={
        "/assets": {
            "max_age": 31536000,  # 1 year
            "public": True,
            "immutable": True,
        },
    },
)

```

## Conditional Requests (304)

### How It Works

1. First request:
   ```http
   GET /api/data HTTP/1.1

   HTTP/1.1 200 OK
   ETag: "abc123"
   Content: {...}
   ```

2. Subsequent request:
   ```http
   GET /api/data HTTP/1.1
   If-None-Match: "abc123"

   HTTP/1.1 304 Not Modified
   ETag: "abc123"
   ```

### Client Usage

```javascript
// Browser handles this automatically
fetch('/api/data')
    .then(response => {
        if (response.status === 304) {
            // Use cached version
        }
    });

```

```bash

# curl with conditional request
curl -H "If-None-Match: \"abc123\"" https://api.example.com/data

```

## Cache-Control Directives

| Directive | Description |
| ----------- | ------------- |
| `public` | Can be cached by CDN/proxies |
| `private` | Only browser can cache |
| `max-age=N` | Cache for N seconds |
| `no-cache` | Must revalidate with server |
| `no-store` | Never cache |
| `immutable` | Never changes |

### Examples

```http

# Public, cached for 1 hour
Cache-Control: public, max-age=3600

# Private, cached for 5 minutes
Cache-Control: private, max-age=300

# Must always revalidate
Cache-Control: no-cache

# Never cache (sensitive data)
Cache-Control: no-store, no-cache, must-revalidate

```

## Custom Cache Store

For distributed caching:

```python
from fastmiddleware import CacheStore

class RedisCacheStore(CacheStore):
    def __init__(self, redis_client):
        self.redis = redis_client

    async def get_etag(self, key: str) -> str | None:
        return await self.redis.get(f"etag:{key}")

    async def set_etag(self, key: str, etag: str, ttl: int) -> None:
        await self.redis.setex(f"etag:{key}", ttl, etag)

    async def get_response(self, key: str) -> bytes | None:
        return await self.redis.get(f"response:{key}")

    async def set_response(self, key: str, data: bytes, ttl: int) -> None:
        await self.redis.setex(f"response:{key}", ttl, data)

store = RedisCacheStore(redis_client)
app.add_middleware(CacheMiddleware, store=store)

```

## Vary Headers

Control cache variants:

```python
config = CacheConfig(
    vary_headers=("Accept", "Accept-Encoding", "Accept-Language"),
)

```

This creates separate cached versions for:

- Different Accept types (JSON vs XML)

- Different encodings (gzip vs identity)

- Different languages

## Path Exclusion

Exclude paths from caching:

```python
app.add_middleware(
    CacheMiddleware,
    exclude_paths={"/auth", "/admin", "/user"},
)

```

## Best Practices

1. **Set appropriate max-age** - Balance freshness vs performance
2. **Use private for user data** - Prevent CDN caching
3. **Use no-store for sensitive data** - Passwords, tokens
4. **Enable ETags** - Efficient revalidation
5. **Use immutable for versioned assets** - `/app.abc123.js`

## Cache Invalidation

Options for cache invalidation:

- Change URL (versioned assets)

- Reduce max-age

- Use no-cache (always revalidate)

- Clear CDN cache manually

## Security Considerations

- Never cache authenticated responses as `public`
- Use `no-store` for sensitive data
- Be careful with `Vary` headers (cache bloat)
- Consider cache-timing attacks

## Related Middlewares

- [CompressionMiddleware](./compression.md) - Compress before caching
- [SecurityHeadersMiddleware](./security-headers.md) - Security headers
