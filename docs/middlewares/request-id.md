# RequestIDMiddleware

Generates unique request identifiers for distributed tracing and request correlation.

## Installation

```python
from src import RequestIDMiddleware
```

## Quick Start

```python
from fastapi import FastAPI
from src import RequestIDMiddleware

app = FastAPI()

app.add_middleware(RequestIDMiddleware)
```

## Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `header_name` | `str` | `"X-Request-ID"` | Request ID header name |
| `generator` | `Callable` | UUID4 | ID generator function |
| `trust_incoming` | `bool` | `True` | Trust incoming request IDs |

## Response Header

```http
HTTP/1.1 200 OK
X-Request-ID: 550e8400-e29b-41d4-a716-446655440000
```

## Examples

### Default Configuration

```python
app.add_middleware(RequestIDMiddleware)
```

### Custom Header Name

```python
app.add_middleware(
    RequestIDMiddleware,
    header_name="X-Correlation-ID",
)
```

### Custom ID Generator

```python
import uuid
import time

def short_id():
    """Generate a short request ID."""
    return f"{int(time.time())}-{uuid.uuid4().hex[:8]}"

app.add_middleware(
    RequestIDMiddleware,
    generator=short_id,
)
```

Response: `X-Request-ID: 1704067200-a1b2c3d4`

### Don't Trust Incoming IDs

```python
# Always generate new IDs, ignore incoming headers
app.add_middleware(
    RequestIDMiddleware,
    trust_incoming=False,
)
```

## Accessing Request ID

### In Route Handlers

```python
from fastapi import Request

@app.get("/")
async def root(request: Request):
    request_id = request.state.request_id
    return {"request_id": request_id}
```

### In Services

```python
from src import get_request_id

async def process_order(order_id: str):
    request_id = get_request_id()
    logger.info(f"Processing order {order_id}", extra={"request_id": request_id})
```

## Distributed Tracing

### Propagating IDs Across Services

```python
import httpx

async def call_downstream_service():
    request_id = get_request_id()
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://downstream-service.example.com/api",
            headers={"X-Request-ID": request_id}
        )
    
    return response.json()
```

### Trusting Incoming IDs

When `trust_incoming=True` (default), the middleware uses existing request IDs:

```http
# Incoming request
GET /api/data HTTP/1.1
X-Request-ID: upstream-request-id-123

# Response (same ID preserved)
HTTP/1.1 200 OK
X-Request-ID: upstream-request-id-123
```

## Logging Integration

### Include Request ID in Logs

```python
import logging

class RequestIDFilter(logging.Filter):
    def filter(self, record):
        from src import get_request_id
        record.request_id = get_request_id() or "-"
        return True

# Configure logger
logger = logging.getLogger("app")
logger.addFilter(RequestIDFilter())

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    "[%(request_id)s] %(levelname)s - %(message)s"
))
logger.addHandler(handler)
```

Output:
```
[550e8400-e29b-41d4-a716-446655440000] INFO - Processing request
[550e8400-e29b-41d4-a716-446655440000] INFO - Fetching user data
[550e8400-e29b-41d4-a716-446655440000] INFO - Request completed
```

## Error Tracking

Include request ID in error responses for debugging:

```python
from src import ErrorHandlerMiddleware, RequestIDMiddleware

app.add_middleware(ErrorHandlerMiddleware, include_request_id=True)
app.add_middleware(RequestIDMiddleware)
```

Error response:
```json
{
    "error": true,
    "message": "Internal server error",
    "request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

## Best Practices

1. **Always use request IDs** - Essential for debugging
2. **Include in all logs** - Makes correlation easy
3. **Propagate to downstream services** - Enables distributed tracing
4. **Include in error responses** - Helps support debugging
5. **Trust incoming IDs** - Unless you have security concerns

## Middleware Order

Add `RequestIDMiddleware` early so other middleware can access the ID:

```python
app.add_middleware(LoggingMiddleware)  # Uses request ID
app.add_middleware(RequestIDMiddleware)  # Generates ID
```

## Related

- [RequestContextMiddleware](request-context.md) - Full request context
- [LoggingMiddleware](logging.md) - Request logging

