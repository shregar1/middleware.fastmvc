# ErrorHandlerMiddleware

Centralized error handling with consistent error response formatting, exception mapping, and optional traceback inclusion.

## Installation

```python
from fastmiddleware import ErrorHandlerMiddleware, ErrorConfig

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import ErrorHandlerMiddleware

app = FastAPI()

app.add_middleware(ErrorHandlerMiddleware)

```

## Configuration

### ErrorConfig

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `include_traceback` | `bool` | `False` | Include stack trace |
| `include_exception_type` | `bool` | `False` | Include exception class |
| `log_exceptions` | `bool` | `True` | Log exceptions |
| `default_message` | `str` | `"An internal error occurred"` | Default message |
| `status_code` | `int` | `500` | Default status code |
| `error_handlers` | `dict` | `{}` | Custom exception handlers |

## Response Format

```json
{
    "error": true,
    "message": "An internal error occurred",
    "status_code": 500,
    "request_id": "abc-123-def"
}

```

### With Exception Type

```json
{
    "error": true,
    "message": "An internal error occurred",
    "status_code": 500,
    "type": "ValueError",
    "request_id": "abc-123-def"
}

```

### With Traceback (Development)

```json
{
    "error": true,
    "message": "invalid literal for int()",
    "status_code": 500,
    "type": "ValueError",
    "detail": "invalid literal for int() with base 10: 'abc'",
    "traceback": [
        "Traceback (most recent call last):",
        "  File \"app.py\", line 42, in handler",
        "    value = int(input)",
        "ValueError: invalid literal for int()"
    ]
}

```

## Examples

### Production Configuration

```python
app.add_middleware(
    ErrorHandlerMiddleware,
    include_traceback=False,
    include_exception_type=False,
    log_exceptions=True,
)

```

### Development Configuration

```python
app.add_middleware(
    ErrorHandlerMiddleware,
    include_traceback=True,
    include_exception_type=True,
    log_exceptions=True,
)

```

### Custom Error Message

```python
app.add_middleware(
    ErrorHandlerMiddleware,
    default_message="Something went wrong. Please try again.",
)

```

### Custom Exception Handlers

```python
from fastmiddleware import ErrorConfig

config = ErrorConfig()
config.error_handlers[ValueError] = (400, "Invalid value provided")
config.error_handlers[PermissionError] = (403, "Permission denied")
config.error_handlers[FileNotFoundError] = (404, "Resource not found")
config.error_handlers[TimeoutError] = (504, "Request timed out")

app.add_middleware(ErrorHandlerMiddleware, config=config)

```

### Handler with Custom Response

```python
from fastmiddleware import ErrorConfig

def handle_validation_error(exc: ValueError) -> tuple[int, str, dict]:
    """Custom handler returning (status, message, extra_data)."""
    return 400, str(exc), {"validation_error": True}

config = ErrorConfig()
config.error_handlers[ValueError] = handle_validation_error

app.add_middleware(ErrorHandlerMiddleware, config=config)

```

## Exception Mapping

Map exceptions to HTTP status codes:

| Exception | Status | Message |
| ----------- | -------- | --------- |
| `ValueError` | 400 | Bad Request |
| `PermissionError` | 403 | Forbidden |
| `FileNotFoundError` | 404 | Not Found |
| `NotImplementedError` | 501 | Not Implemented |
| `TimeoutError` | 504 | Gateway Timeout |
| Other | 500 | Internal Server Error |

## Logging

When `log_exceptions=True`:

```python
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR)

# Exceptions are logged with:

# - Exception type

# - Message

# - Traceback

# - Request ID (if available)

```

## Integration with Request ID

```python
from fastmiddleware import ErrorHandlerMiddleware, RequestIDMiddleware

# Request ID is included in error responses
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

## Custom Error Responses

### JSON API Format

```python
class JSONAPIErrorMiddleware(ErrorHandlerMiddleware):
    async def format_error(self, request, exc, status_code, message):
        return {
            "errors": [{
                "status": str(status_code),
                "title": type(exc).__name__,
                "detail": message,
            }]
        }

```

### Problem Details (RFC 7807)

```python
class ProblemDetailsMiddleware(ErrorHandlerMiddleware):
    async def format_error(self, request, exc, status_code, message):
        return {
            "type": f"https://api.example.com/errors/{status_code}",
            "title": HTTP_STATUS_PHRASES.get(status_code, "Error"),
            "status": status_code,
            "detail": message,
            "instance": str(request.url),
        }

```

## Middleware Order

Place ErrorHandlerMiddleware early to catch all exceptions:

```python
app.add_middleware(ErrorHandlerMiddleware)  # Add early
app.add_middleware(LoggingMiddleware)
app.add_middleware(AuthenticationMiddleware)
app.add_middleware(RateLimitMiddleware)

```

## Path Exclusion

Exclude paths from error handling:

```python
app.add_middleware(
    ErrorHandlerMiddleware,
    exclude_paths={"/health"},
)

```

## Best Practices

1. **Never expose tracebacks in production** - Security risk
2. **Log all exceptions** - For debugging and monitoring
3. **Include request ID** - For support and debugging
4. **Use custom handlers** - Map domain exceptions
5. **Return consistent format** - Easier for clients

## Security Considerations

- Tracebacks can expose:
  - File paths
  - Database queries
  - Internal variable values
  - Configuration details

- Always disable in production

- Sanitize error messages

## Related Middlewares

- [RequestIDMiddleware](./request-id.md) - Add request ID to errors
- [LoggingMiddleware](./logging.md) - Log error details
