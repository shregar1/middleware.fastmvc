# LoggingMiddleware

Structured request/response logging with configurable verbosity levels.

## Installation

```python
from src import LoggingMiddleware
```

## Quick Start

```python
from fastapi import FastAPI
from src import LoggingMiddleware

app = FastAPI()

app.add_middleware(LoggingMiddleware)
```

## Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `log_level` | `int` | `logging.INFO` | Log level |
| `log_request_body` | `bool` | `False` | Log request bodies |
| `log_response_body` | `bool` | `False` | Log response bodies |
| `log_request_headers` | `bool` | `False` | Log request headers |
| `log_response_headers` | `bool` | `False` | Log response headers |
| `custom_logger` | `Logger \| None` | `None` | Custom logger instance |
| `exclude_paths` | `set[str]` | Health/metrics | Paths to skip |

## Examples

### Basic Logging

```python
app.add_middleware(LoggingMiddleware)
```

Output:
```
→ GET /api/users
← ✓ GET /api/users [200] 12.34ms
```

### Verbose Logging (Development)

```python
import logging

app.add_middleware(
    LoggingMiddleware,
    log_level=logging.DEBUG,
    log_request_headers=True,
    log_response_headers=True,
    log_request_body=True,
)
```

Output:
```
→ POST /api/users
  Headers: {'content-type': 'application/json', 'authorization': 'Bearer ***'}
  Body: {"name": "John", "email": "john@example.com"}
← ✓ POST /api/users [201] 45.67ms
  Headers: {'content-type': 'application/json', 'x-request-id': 'abc123'}
```

### Custom Logger

```python
import logging

# Create custom logger
logger = logging.getLogger("api.requests")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))
logger.addHandler(handler)

app.add_middleware(
    LoggingMiddleware,
    custom_logger=logger,
)
```

### Exclude Health Checks

```python
app.add_middleware(
    LoggingMiddleware,
    exclude_paths={
        "/health",
        "/ready",
        "/live",
        "/metrics",
        "/favicon.ico",
    },
)
```

### Production Configuration

```python
import logging

app.add_middleware(
    LoggingMiddleware,
    log_level=logging.INFO,
    log_request_headers=False,
    log_response_headers=False,
    log_request_body=False,
    log_response_body=False,
    exclude_paths={"/health", "/metrics"},
)
```

## Log Format

### Request Log

```
→ {METHOD} {PATH}
```

### Response Log (Success)

```
← ✓ {METHOD} {PATH} [{STATUS}] {TIME}ms
```

### Response Log (Error)

```
← ✗ {METHOD} {PATH} [{STATUS}] {TIME}ms
```

## Structured Logging (JSON)

For JSON logging, use a custom logger with JSON formatter:

```python
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        
        # Add extra fields
        if hasattr(record, "method"):
            log_data["method"] = record.method
        if hasattr(record, "path"):
            log_data["path"] = record.path
        if hasattr(record, "status_code"):
            log_data["status_code"] = record.status_code
        if hasattr(record, "duration_ms"):
            log_data["duration_ms"] = record.duration_ms
        
        return json.dumps(log_data)

logger = logging.getLogger("api")
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)

app.add_middleware(LoggingMiddleware, custom_logger=logger)
```

Output:
```json
{"timestamp": "2024-01-01 12:00:00", "level": "INFO", "message": "GET /api/users", "method": "GET", "path": "/api/users", "status_code": 200, "duration_ms": 12.34}
```

## Integration with Request Context

```python
from src import LoggingMiddleware, RequestContextMiddleware, get_request_id

# Add both middlewares
app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestContextMiddleware)

# Request ID will be included in logs
```

## Log Levels

| Level | When Used |
|-------|-----------|
| `DEBUG` | Verbose details, headers, bodies |
| `INFO` | Normal request/response logs |
| `WARNING` | 4xx client errors |
| `ERROR` | 5xx server errors |

## Best Practices

1. **Exclude noisy paths** - Don't log health checks
2. **Don't log sensitive data** - Mask tokens, passwords
3. **Use structured logging** - JSON for log aggregation
4. **Set appropriate levels** - DEBUG for dev, INFO for prod
5. **Include request IDs** - For request tracing

## Security Considerations

⚠️ **Sensitive Data Warning**

Be careful not to log:
- Authorization tokens
- API keys
- Passwords
- Personal information (PII)

```python
# ❌ Don't log headers with tokens
app.add_middleware(LoggingMiddleware, log_request_headers=True)

# ✅ Use header filtering (custom implementation)
```

## Related

- [TimingMiddleware](timing.md) - Response timing
- [RequestIDMiddleware](request-id.md) - Request tracing
- [RequestContextMiddleware](request-context.md) - Request context

