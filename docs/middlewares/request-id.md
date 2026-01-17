# RequestIDMiddleware

Generates unique request identifiers for distributed tracing and request correlation.

## Installation

```python
from fastMiddleware import RequestIDMiddleware
```

## Quick Start

```python
from fastapi import FastAPI
from fastMiddleware import RequestIDMiddleware

app = FastAPI()

app.add_middleware(RequestIDMiddleware)
```

## Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `header_name` | `str` | `"X-Request-ID"` | Header name for request ID |
| `generator` | `Callable` | UUID4 | ID generator function |
| `trust_incoming` | `bool` | `True` | Trust incoming request IDs |

## Response Header

```http
X-Request-ID: 550e8400-e29b-41d4-a716-446655440000
```

## Examples

### Default Configuration

```python
app.add_middleware(RequestIDMiddleware)

# Generates UUIDv4: X-Request-ID: 550e8400-e29b-41d4-a716-446655440000
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

def custom_generator() -> str:
    """Generate a custom request ID with timestamp prefix."""
    timestamp = int(time.time() * 1000)
    unique = uuid.uuid4().hex[:8]
    return f"{timestamp}-{unique}"

app.add_middleware(
    RequestIDMiddleware,
    generator=custom_generator,
)

# Result: X-Request-ID: 1704067200000-a1b2c3d4
```

### Short IDs

```python
import secrets

def short_id_generator() -> str:
    """Generate short, URL-safe IDs."""
    return secrets.token_urlsafe(12)

app.add_middleware(
    RequestIDMiddleware,
    generator=short_id_generator,
)

# Result: X-Request-ID: Kj8_mX2pQvNt
```

### Don't Trust Incoming IDs

```python
app.add_middleware(
    RequestIDMiddleware,
    trust_incoming=False,  # Always generate new ID
)
```

### Propagate Incoming IDs

```python
app.add_middleware(
    RequestIDMiddleware,
    trust_incoming=True,  # Use incoming ID if present
)
```

When `trust_incoming=True`:
- If request has `X-Request-ID`: Use that ID
- If no incoming ID: Generate new ID

## Accessing Request ID

### In Route Handlers

```python
from fastapi import Request

@app.get("/")
async def root(request: Request):
    request_id = request.state.request_id
    return {"request_id": request_id}
```

### In Dependencies

```python
from fastapi import Request, Depends

def get_request_id(request: Request) -> str:
    return request.state.request_id

@app.get("/")
async def root(request_id: str = Depends(get_request_id)):
    return {"request_id": request_id}
```

### In Services/Repositories

```python
from fastMiddleware import get_request_id

async def my_service_function():
    request_id = get_request_id()
    logger.info(f"Processing request {request_id}")
```

## Use Cases

### Distributed Tracing

Pass request ID to downstream services:

```python
import httpx

@app.get("/api/data")
async def get_data(request: Request):
    request_id = request.state.request_id
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://other-service/data",
            headers={"X-Request-ID": request_id},
        )
    
    return response.json()
```

### Log Correlation

```python
import logging

@app.get("/api/users")
async def get_users(request: Request):
    request_id = request.state.request_id
    
    logging.info(
        f"Fetching users",
        extra={"request_id": request_id}
    )
    
    users = await db.get_users()
    
    logging.info(
        f"Found {len(users)} users",
        extra={"request_id": request_id}
    )
    
    return users
```

### Error Tracking

```python
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", "unknown")
    
    # Log with request ID
    logging.error(
        f"Unhandled exception: {exc}",
        extra={"request_id": request_id},
        exc_info=True,
    )
    
    # Return request ID to client for support
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "request_id": request_id,
        },
    )
```

### Support Tickets

```python
@app.get("/support/ticket")
async def create_ticket(request: Request, issue: str):
    request_id = request.state.request_id
    
    return {
        "message": f"Ticket created. Reference: {request_id}",
        "request_id": request_id,
    }
```

## Integration with Other Middlewares

### With Logging

```python
from fastMiddleware import RequestIDMiddleware, LoggingMiddleware

app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestIDMiddleware)

# Logs include request ID automatically
```

### With Request Context

```python
from fastMiddleware import RequestIDMiddleware, RequestContextMiddleware

app.add_middleware(RequestContextMiddleware)
app.add_middleware(RequestIDMiddleware)

# Request ID available via get_request_id()
```

## Best Practices

1. **Always include in responses** - Helps clients report issues
2. **Propagate to downstream services** - Enables distributed tracing
3. **Include in all logs** - Makes log correlation possible
4. **Use in error responses** - Customers can reference for support
5. **Consider ID format** - UUID for uniqueness, shorter for readability

## Security Considerations

- Request IDs can reveal request volume patterns
- Don't use sequential IDs (reveals total request count)
- Consider using random IDs for public APIs
- Trust incoming IDs only from trusted sources

## Related Middlewares

- [RequestContextMiddleware](./request-context.md) - Access request ID anywhere
- [LoggingMiddleware](./logging.md) - Log with request ID
- [ErrorHandlerMiddleware](./error-handler.md) - Include ID in errors
