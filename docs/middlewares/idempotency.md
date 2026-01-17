# IdempotencyMiddleware

Provides idempotency key support for safe request retries, preventing duplicate operations.

## Installation

```python
from src import IdempotencyMiddleware, IdempotencyConfig
```

## Quick Start

```python
from fastapi import FastAPI
from src import IdempotencyMiddleware

app = FastAPI()

app.add_middleware(IdempotencyMiddleware)
```

## Configuration

### IdempotencyConfig

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `header_name` | `str` | `"Idempotency-Key"` | Header name for key |
| `ttl_seconds` | `int` | `86400` | Cache TTL (24 hours) |
| `require_key` | `bool` | `False` | Require key for POST/PUT/PATCH |
| `required_methods` | `set[str]` | POST/PUT/PATCH | Methods to apply idempotency |

## How It Works

1. Client sends request with `Idempotency-Key` header
2. First request: Execute and cache response
3. Repeat request with same key: Return cached response
4. Different key: Execute as new request

```
Request 1: POST /orders + Idempotency-Key: abc123
→ Execute, create order, cache response

Request 2: POST /orders + Idempotency-Key: abc123
→ Return cached response (no duplicate order)
```

## Response Headers

| Header | Value | Description |
|--------|-------|-------------|
| `X-Idempotent-Replayed` | `true` | Response was cached |

## Examples

### Basic Configuration

```python
app.add_middleware(IdempotencyMiddleware)
```

### Require Idempotency Keys

```python
from src import IdempotencyMiddleware, IdempotencyConfig

config = IdempotencyConfig(
    require_key=True,  # Error if POST/PUT/PATCH without key
)

app.add_middleware(IdempotencyMiddleware, config=config)
```

### Custom Header Name

```python
config = IdempotencyConfig(
    header_name="X-Idempotency-Key",
)
```

### Custom TTL

```python
config = IdempotencyConfig(
    ttl_seconds=3600,  # 1 hour
)
```

### Custom Methods

```python
config = IdempotencyConfig(
    required_methods={"POST"},  # Only POST requests
)
```

## Client Usage

### JavaScript

```javascript
// Generate unique key per operation
const idempotencyKey = `order-${Date.now()}-${Math.random().toString(36).slice(2)}`;

const response = await fetch('/api/orders', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Idempotency-Key': idempotencyKey,
    },
    body: JSON.stringify({ product_id: 123, quantity: 2 }),
});

// Check if this was a replay
if (response.headers.get('X-Idempotent-Replayed') === 'true') {
    console.log('This was a cached response');
}
```

### Python

```python
import httpx
import uuid

async def create_order(order_data: dict) -> dict:
    idempotency_key = str(uuid.uuid4())
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.example.com/orders",
            json=order_data,
            headers={"Idempotency-Key": idempotency_key},
        )
    
    return response.json()
```

### cURL

```bash
curl -X POST https://api.example.com/orders \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: unique-key-123" \
  -d '{"product_id": 123}'

# Retry with same key - safe!
curl -X POST https://api.example.com/orders \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: unique-key-123" \
  -d '{"product_id": 123}'
```

## Custom Storage Backend

```python
from src import IdempotencyStore

class RedisIdempotencyStore(IdempotencyStore):
    """Redis-backed idempotency store."""
    
    def __init__(self, redis_client):
        self.redis = redis_client
    
    async def get(self, key: str) -> dict | None:
        data = await self.redis.get(f"idempotency:{key}")
        return json.loads(data) if data else None
    
    async def set(
        self,
        key: str,
        response_data: dict,
        ttl: int,
    ) -> None:
        await self.redis.setex(
            f"idempotency:{key}",
            ttl,
            json.dumps(response_data),
        )
    
    async def delete(self, key: str) -> None:
        await self.redis.delete(f"idempotency:{key}")

# Usage
store = RedisIdempotencyStore(redis_client)
app.add_middleware(IdempotencyMiddleware, store=store)
```

## Key Generation Best Practices

### Client-Generated Keys

```javascript
// Good: UUID
const key = crypto.randomUUID();

// Good: Operation-specific
const key = `order-${userId}-${cartId}-${timestamp}`;

// Bad: Predictable
const key = `order-1`;  // Can be guessed
```

### Server Validation

```python
import uuid

@app.post("/orders")
async def create_order(request: Request, order: OrderCreate):
    key = request.headers.get("Idempotency-Key")
    
    # Validate key format
    try:
        uuid.UUID(key)
    except ValueError:
        raise HTTPException(400, "Invalid Idempotency-Key format")
```

## Error Handling

### Missing Key (when required)

```http
HTTP/1.1 400 Bad Request

{
    "detail": "Idempotency-Key header is required"
}
```

### Conflict (concurrent requests)

```http
HTTP/1.1 409 Conflict

{
    "detail": "A request with this Idempotency-Key is already in progress"
}
```

## Use Cases

### Payment Processing

```javascript
// Prevent duplicate payments
const paymentKey = `payment-${orderId}-${amount}`;

await fetch('/api/payments', {
    method: 'POST',
    headers: { 'Idempotency-Key': paymentKey },
    body: JSON.stringify({ order_id: orderId, amount }),
});
```

### Order Creation

```javascript
// Retry-safe order creation
const orderKey = `order-${cartId}-${timestamp}`;

await fetch('/api/orders', {
    method: 'POST',
    headers: { 'Idempotency-Key': orderKey },
    body: JSON.stringify(cart),
});
```

### Resource Updates

```javascript
// Safe resource updates
const updateKey = `update-${resourceId}-${version}`;

await fetch(`/api/resources/${resourceId}`, {
    method: 'PUT',
    headers: { 'Idempotency-Key': updateKey },
    body: JSON.stringify(newData),
});
```

## Best Practices

1. **Always use for payments** - Critical for financial operations
2. **Use UUIDs** - Prevent key collisions
3. **Include operation context** - Makes debugging easier
4. **Set appropriate TTL** - Balance between safety and storage
5. **Handle 409 conflicts** - Retry after waiting

## Related

- [RateLimitMiddleware](rate-limit.md) - Rate limiting
- [ErrorHandlerMiddleware](error-handler.md) - Error handling

