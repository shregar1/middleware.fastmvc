# RequestContextMiddleware

Provides async-safe context variables accessible from anywhere in your application code.

## Installation

```python
from fastmiddleware import (
    RequestContextMiddleware,
    get_request_id,
    get_request_context,
)

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import RequestContextMiddleware, get_request_id

app = FastAPI()

app.add_middleware(RequestContextMiddleware)

# Access request ID anywhere
async def my_service():
    request_id = get_request_id()
    print(f"Processing request {request_id}")

```

## Helper Functions

| Function | Returns | Description |
| ---------- | --------- | ------------- |
| `get_request_id()` | `str \| None` | Current request ID |
| `get_request_context()` | `dict` | Full request context |

## Context Data

| Key | Type | Description |
| ----- | ------ | ------------- |
| `request_id` | `str` | Unique request identifier |
| `start_time` | `datetime` | Request start timestamp |
| `client_ip` | `str` | Client IP address |
| `method` | `str` | HTTP method |
| `path` | `str` | Request path |

## Examples

### Basic Usage

```python
from fastmiddleware import RequestContextMiddleware, get_request_id, get_request_context

app.add_middleware(RequestContextMiddleware)

@app.get("/")
async def root():
    request_id = get_request_id()
    ctx = get_request_context()

    return {
        "request_id": request_id,
        "path": ctx["path"],
        "method": ctx["method"],
    }

```

### In Service Layer

```python
from fastmiddleware import get_request_id, get_request_context

class UserService:
    async def get_users(self):
        request_id = get_request_id()
        ctx = get_request_context()

        # Log with context
        logger.info(
            f"Fetching users",
            extra={
                "request_id": request_id,
                "client_ip": ctx["client_ip"],
            }
        )

        return await self.db.get_users()

```

### In Repository Layer

```python
from fastmiddleware import get_request_id

class UserRepository:
    async def get_by_id(self, user_id: int):
        request_id = get_request_id()

        try:
            user = await self.db.fetchone(
                "SELECT * FROM users WHERE id = $1",
                user_id
            )
            return user
        except Exception as e:
            logger.error(
                f"Database error in request {request_id}: {e}"
            )
            raise

```

### In Background Tasks

```python
from fastmiddleware import get_request_id

@app.post("/process")
async def process_data(background_tasks: BackgroundTasks):
    request_id = get_request_id()

    # Pass request ID to background task
    background_tasks.add_task(
        process_in_background,
        request_id=request_id,
    )

    return {"status": "processing"}

async def process_in_background(request_id: str):
    # Note: get_request_id() won't work here
    # Use the passed request_id instead
    logger.info(f"Background processing for {request_id}")

```

### Structured Logging

```python
import logging
import json

class ContextualFormatter(logging.Formatter):
    def format(self, record):
        from fastmiddleware import get_request_context

        ctx = get_request_context() or {}

        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "request_id": ctx.get("request_id"),
            "path": ctx.get("path"),
            "client_ip": ctx.get("client_ip"),
        }

        return json.dumps(log_data)

```

### Custom Context Data

```python
from contextvars import ContextVar

# Create custom context variable
user_context: ContextVar[dict] = ContextVar("user_context", default={})

class EnhancedContextMiddleware(RequestContextMiddleware):
    async def dispatch(self, request, call_next):
        # Set standard context
        response = await super().dispatch(request, call_next)

        # Add custom data
        if hasattr(request.state, "auth"):
            user_context.set({
                "user_id": request.state.auth.get("user_id"),
                "role": request.state.auth.get("role"),
            })

        return response

def get_user_context() -> dict:
    return user_context.get()

```

### Database Query Logging

```python
from fastmiddleware import get_request_id

class TracedDatabase:
    async def execute(self, query: str, *args):
        request_id = get_request_id()
        start = time.time()

        try:
            result = await self.db.execute(query, *args)
            duration = time.time() - start

            logger.debug(
                f"Query executed in {duration:.3f}s",
                extra={
                    "request_id": request_id,
                    "query": query[:100],
                    "duration": duration,
                }
            )

            return result
        except Exception as e:
            logger.error(
                f"Query failed for request {request_id}: {e}",
                extra={"query": query[:100]}
            )
            raise

```

## Thread Safety

Context variables are async-safe and work correctly with:

- ✅ async/await code

- ✅ FastAPI dependencies

- ✅ Starlette middleware

- ✅ Multiple concurrent requests

- ⚠️ Background tasks (context doesn't propagate automatically)

- ⚠️ Thread pools (use `contextvars.copy_context()`)

### Thread Pool Usage

```python
import asyncio
from contextvars import copy_context

async def run_in_thread(func, *args):
    loop = asyncio.get_event_loop()
    ctx = copy_context()
    return await loop.run_in_executor(None, ctx.run, func, *args)

```

## Middleware Order

Place RequestContextMiddleware after RequestIDMiddleware:

```python

# Order matters!
app.add_middleware(RequestContextMiddleware)  # Add first (runs last)
app.add_middleware(RequestIDMiddleware)        # Add second (runs first)

```

This ensures request ID is available when context is created.

## Best Practices

1. **Don't overuse** - Pass data explicitly when practical
2. **Handle missing context** - Always check for None
3. **Don't mutate context** - Treat as read-only
4. **Copy for background tasks** - Context doesn't propagate automatically
5. **Use for cross-cutting concerns** - Logging, tracing, not business logic

## Related Middlewares

- [RequestIDMiddleware](./request-id.md) - Generates request IDs
- [LoggingMiddleware](./logging.md) - Logs with context
- [AuthenticationMiddleware](./authentication.md) - Adds auth to state
