# CacheMiddleware

HTTP caching with ETag generation and conditional request support.

## Installation

```python
from src import CacheMiddleware, CacheConfig
```

## Quick Start

```python
from fastapi import FastAPI
from src import CacheMiddleware

app = FastAPI()

app.add_middleware(CacheMiddleware)
```

## Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `default_max_age` | `int` | `0` | Default cache time (seconds) |
| `enable_etag` | `bool` | `True` | Generate ETags |
| `private` | `bool` | `False` | Use private cache |
| `no_store` | `bool` | `False` | Disable caching |
| `vary_headers` | `tuple` | Accept headers | Vary headers |
| `path_rules` | `dict` | `{}` | Path-specific rules |

## Response Headers

```http
Cache-Control: public, max-age=3600
ETag: "abc123..."
Vary: Accept, Accept-Encoding
```

## Examples

### Basic Caching

```python
from src import CacheMiddleware, CacheConfig

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
        "/static": {"max_age": 86400, "public": True},
        "/api/user": {"no_store": True, "private": True},
    },
)
```

### Conditional Requests

Client sends `If-None-Match` with ETag:
```http
GET /api/data HTTP/1.1
If-None-Match: "abc123"
```

Server returns 304 if unchanged:
```http
HTTP/1.1 304 Not Modified
ETag: "abc123"
```

## Best Practices

1. **Use ETags** - Enable conditional requests
2. **Set appropriate max-age** - Balance freshness with performance
3. **Use private for user data** - Don't cache in shared caches
4. **Use no-store for sensitive data** - Prevent any caching

## Related

- [CompressionMiddleware](compression.md) - Response compression

