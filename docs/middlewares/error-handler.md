# ErrorHandlerMiddleware

Catches exceptions and returns consistent, structured error responses.

## Installation

```python
from src import ErrorHandlerMiddleware, ErrorConfig
```

## Quick Start

```python
from fastapi import FastAPI
from src import ErrorHandlerMiddleware

app = FastAPI()

app.add_middleware(ErrorHandlerMiddleware)
```

## Configuration

### ErrorConfig

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `include_traceback` | `bool` | `False` | Include stack trace |
| `include_exception_type` | `bool` | `False` | Include exception class |
| `log_exceptions` | `bool` | `True` | Log exceptions |
| `default_message` | `str` | `"An internal error occurred"` | Default error message |
| `status_code` | `int` | `500` | Default status code |
| `error_handlers` | `dict` | `{}` | Custom exception handlers |

## Response Format

### Default (Production)

```json
{
    "error": true,
    "message": "An internal error occurred",
    "request_id": "abc-123"
}
```

### With Traceback (Development)

```json
{
    "error": true,
    "message": "An internal error occurred",
    "type": "ValueError",
    "detail": "invalid literal for int() with base 10: 'abc'",
    "request_id": "abc-123",
    "traceback": [
        "Traceback (most recent call last):",
        "  File \"app.py\", line 10, in handler",
        "    int('abc')",
        "ValueError: invalid literal for int() with base 10: 'abc'"
    ]
}
```

## Examples

### Development Mode

```python
app.add_middleware(
    ErrorHandlerMiddleware,
    include_traceback=True,
    include_exception_type=True,
)
```

### Production Mode

```python
app.add_middleware(
    ErrorHandlerMiddleware,
    include_traceback=False,
    include_exception_type=False,
    log_exceptions=True,
)
```

### Custom Error Handlers

```python
from src import ErrorHandlerMiddleware, ErrorConfig

config = ErrorConfig()

# Map exception types to (status_code, message)
config.error_handlers[ValueError] = (400, "Invalid value provided")
config.error_handlers[PermissionError] = (403, "Permission denied")
config.error_handlers[FileNotFoundError] = (404, "Resource not found")
config.error_handlers[TimeoutError] = (504, "Request timed out")

app.add_middleware(ErrorHandlerMiddleware, config=config)
```

### Custom Default Message

```python
app.add_middleware(
    ErrorHandlerMiddleware,
    default_message="Something went wrong. Please try again later.",
)
```

## Custom Exception Classes

```python
class BusinessError(Exception):
    """Base class for business errors."""
    status_code = 400
    message = "A business error occurred"

class OrderNotFoundError(BusinessError):
    status_code = 404
    message = "Order not found"

class InsufficientFundsError(BusinessError):
    status_code = 402
    message = "Insufficient funds"

# Register handlers
config = ErrorConfig()
config.error_handlers[OrderNotFoundError] = (404, "Order not found")
config.error_handlers[InsufficientFundsError] = (402, "Insufficient funds")
```

## Integration with Request ID

```python
from src import ErrorHandlerMiddleware, RequestIDMiddleware

# Error responses include request ID
app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(RequestIDMiddleware)
```

Response:
```json
{
    "error": true,
    "message": "An internal error occurred",
    "request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

## Logging

With `log_exceptions=True`, exceptions are logged:

```python
import logging

logging.basicConfig(level=logging.ERROR)

app.add_middleware(
    ErrorHandlerMiddleware,
    log_exceptions=True,
)
```

Log output:
```
ERROR:fastmvc:Unhandled exception in request abc-123
Traceback (most recent call last):
  ...
ValueError: invalid input
```

## Exception Filtering

Exclude certain paths from error handling:

```python
app.add_middleware(
    ErrorHandlerMiddleware,
    exclude_paths={"/webhooks"},  # Let webhook errors propagate
)
```

## HTTP Exceptions

FastAPI's `HTTPException` is not caught by default (passed through):

```python
from fastapi import HTTPException

@app.get("/item/{id}")
async def get_item(id: int):
    if id < 0:
        raise HTTPException(status_code=400, detail="Invalid ID")
    # This is NOT caught by ErrorHandlerMiddleware
```

To catch all exceptions:

```python
# Custom handler for HTTPException
config.error_handlers[HTTPException] = None  # Let it pass through

# Or handle it:
def handle_http_exception(exc: HTTPException):
    return (exc.status_code, exc.detail)
```

## Best Practices

### Development

- Include tracebacks for debugging
- Include exception types
- Log all exceptions

```python
app.add_middleware(
    ErrorHandlerMiddleware,
    include_traceback=True,
    include_exception_type=True,
    log_exceptions=True,
)
```

### Production

- Hide tracebacks (security)
- Hide exception types (security)
- Log exceptions for monitoring
- Use generic error messages

```python
app.add_middleware(
    ErrorHandlerMiddleware,
    include_traceback=False,
    include_exception_type=False,
    log_exceptions=True,
    default_message="An error occurred. Please try again.",
)
```

## Security Considerations

⚠️ **Never expose in production:**
- Stack traces
- Internal exception types
- Database error messages
- File paths
- Internal IDs

## Middleware Order

Place early to catch exceptions from all middleware:

```python
app.add_middleware(ErrorHandlerMiddleware)  # Add early (catches all)
app.add_middleware(LoggingMiddleware)
app.add_middleware(AuthenticationMiddleware)
```

## Related

- [RequestIDMiddleware](request-id.md) - Include request IDs in errors
- [LoggingMiddleware](logging.md) - Request logging

