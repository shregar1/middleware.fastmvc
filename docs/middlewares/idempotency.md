# IdempotencyMiddleware

Provides idempotency key support for safe request retries, preventing duplicate operations.

## Installation

```python
from fastMiddleware import IdempotencyMiddleware, IdempotencyConfig, InMemoryIdempotencyStore
```

## Quick Start

```python
from fastapi import FastAPI
from fastMiddleware import IdempotencyMiddleware

app = FastAPI()
app.add_middleware(IdempotencyMiddleware)
```

## Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `header_name` | `str` | `"Idempotency-Key"` | Header name |
| `ttl_seconds` | `int` | `86400` | Cache TTL (24 hours) |
| `require_key` | `bool` | `False` | Require key for POST/PUT/PATCH |
| `required_methods` | `set` | POST/PUT/PATCH | Methods requiring idempotency |

## Examples

### Basic Usage

```python
app.add_middleware(IdempotencyMiddleware)
```

Client usage:
```bash
curl -X POST /api/payments \
  -H "Idempotency-Key: payment-123" \
  -d '{"amount": 100}'
```

### Require Idempotency Key

```python
config = IdempotencyConfig(require_key=True)
app.add_middleware(IdempotencyMiddleware, config=config)
```

### Custom TTL

```python
config = IdempotencyConfig(ttl_seconds=3600)  # 1 hour
app.add_middleware(IdempotencyMiddleware, config=config)
```

## Response Headers

| Header | Description |
|--------|-------------|
| `X-Idempotent-Replayed` | `true` if cached response |

## How It Works

1. Client sends request with `Idempotency-Key` header
2. Middleware checks if key exists in store
3. If exists: return cached response
4. If new: execute request, cache response
5. Same key = same response (idempotent)

## Best Practices

1. Use UUIDs for idempotency keys
2. Include request context in key
3. Set appropriate TTL
4. Handle 409 Conflict for concurrent requests
