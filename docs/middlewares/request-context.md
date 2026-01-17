# RequestContextMiddleware

Provides async-safe context variables accessible from anywhere in your code without passing request objects.

## Installation

```python
from src import (
    RequestContextMiddleware,
    get_request_id,
    get_request_context,
)
```

## Quick Start

```python
from fastapi import FastAPI
from src import RequestContextMiddleware, get_request_id

app = FastAPI()

app.add_middleware(RequestContextMiddleware)

@app.get("/")
async def root():
    request_id = get_request_id()
    return {"request_id": request_id}
```

## Helper Functions

| Function | Returns | Description |
|----------|---------|-------------|
| `get_request_id()` | `str \| None` | Current request ID |
| `get_request_context()` | `dict` | Full context dictionary |

## Context Data

| Key | Type | Description |
|-----|------|-------------|
| `request_id` | `str` | Unique request identifier |
| `start_time` | `datetime` | Request start time |
| `client_ip` | `str` | Client IP address |
| `method` | `str` | HTTP method |
| `path` | `str` | Request path |

## Examples

### Accessing Context in Services

```python
from src import get_request_id, get_request_context

class OrderService:
    async def create_order(self, data: dict):
        request_id = get_request_id()
        ctx = get_request_context()
        
        self.logger.info(
            f"Creating order for client {ctx['client_ip']}",
            extra={"request_id": request_id}
        )
        
        order = await self.db.orders.create(data)
        return order
```

### Logging with Context

```python
import logging
from src import get_request_id, get_request_context

class ContextLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
    
    def info(self, message: str):
        request_id = get_request_id() or "-"
        ctx = get_request_context()
        
        self.logger.info(
            message,
            extra={
                "request_id": request_id,
                "path": ctx.get("path", "-"),
                "client_ip": ctx.get("client_ip", "-"),
            }
        )

# Usage
logger = ContextLogger("app")

async def process_data():
    logger.info("Processing data")  # Includes request context automatically
```

### Database Query Tagging

```python
from src import get_request_id

async def query_with_context(query: str):
    request_id = get_request_id()
    
    # Add request ID as comment for query tracing
    tagged_query = f"/* request_id={request_id} */ {query}"
    
    return await db.execute(tagged_query)
```

### External API Calls

```python
import httpx
from src import get_request_id

async def call_external_api(endpoint: str):
    request_id = get_request_id()
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            endpoint,
            headers={"X-Request-ID": request_id}
        )
    
    return response.json()
```

### Audit Logging

```python
from src import get_request_context

async def audit_log(action: str, resource: str):
    ctx = get_request_context()
    
    await db.audit_logs.insert({
        "action": action,
        "resource": resource,
        "request_id": ctx.get("request_id"),
        "client_ip": ctx.get("client_ip"),
        "path": ctx.get("path"),
        "method": ctx.get("method"),
        "timestamp": ctx.get("start_time"),
    })
```

## Thread Safety

The context uses Python's `contextvars` module, which is:
- ✅ Safe for async code
- ✅ Isolated between requests
- ✅ Works with asyncio tasks

```python
import asyncio
from src import get_request_id

async def parallel_task():
    # Each task sees its own request context
    request_id = get_request_id()
    print(f"Task sees request ID: {request_id}")

@app.get("/parallel")
async def parallel_endpoint():
    # All tasks see the same request ID
    await asyncio.gather(
        parallel_task(),
        parallel_task(),
        parallel_task(),
    )
    return {"ok": True}
```

## Middleware Order

Add `RequestContextMiddleware` before middleware that needs context access:

```python
app.add_middleware(LoggingMiddleware)  # Can use get_request_id()
app.add_middleware(RequestContextMiddleware)  # Sets up context
app.add_middleware(RequestIDMiddleware)  # Generates request ID
```

## Custom Context Data

Extend the context with custom data:

```python
from contextvars import ContextVar

# Create custom context variable
user_context: ContextVar[dict] = ContextVar("user", default={})

@app.middleware("http")
async def set_user_context(request, call_next):
    # Set custom context
    if hasattr(request.state, "auth"):
        user_context.set(request.state.auth)
    
    response = await call_next(request)
    return response

# Access anywhere
def get_current_user() -> dict:
    return user_context.get({})
```

## Best Practices

1. **Use for cross-cutting concerns** - Logging, tracing, auditing
2. **Keep context read-only** - Don't modify context data
3. **Handle None values** - Context may be empty outside requests
4. **Don't overuse** - Pass data explicitly when appropriate

## Related

- [RequestIDMiddleware](request-id.md) - Request ID generation
- [LoggingMiddleware](logging.md) - Request logging

