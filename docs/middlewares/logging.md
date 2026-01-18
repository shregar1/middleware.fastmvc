# LoggingMiddleware

Structured request/response logging with configurable verbosity, custom formatters, and sensitive data filtering.

## Installation

```python
from fastmiddleware import LoggingMiddleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import LoggingMiddleware

app = FastAPI()

app.add_middleware(LoggingMiddleware)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `log_level` | `int` | `logging.INFO` | Logging level |
| `log_request_body` | `bool` | `False` | Log request bodies |
| `log_response_body` | `bool` | `False` | Log response bodies |
| `log_request_headers` | `bool` | `False` | Log request headers |
| `log_response_headers` | `bool` | `False` | Log response headers |
| `exclude_paths` | `set[str]` | Health/metrics paths | Paths to skip |
| `custom_logger` | `Logger \| None` | `None` | Custom logger instance |
| `sensitive_headers` | `set[str]` | Auth headers | Headers to mask |

## Log Output

### Default Format

```text
→ GET /api/users
← ✓ GET /api/users [200] 12.34ms

```

### With Headers

```text
→ GET /api/users
  Headers: {"accept": "application/json", "authorization": "[REDACTED]"}
← ✓ GET /api/users [200] 12.34ms
  Headers: {"content-type": "application/json", "x-request-id": "abc-123"}

```

### Error Response

```text
→ POST /api/users
← ✗ POST /api/users [400] 5.67ms

```

## Examples

### Basic Logging

```python
import logging

logging.basicConfig(level=logging.INFO)

app.add_middleware(LoggingMiddleware)

```

### Verbose Logging (Development)

```python
app.add_middleware(
    LoggingMiddleware,
    log_level=logging.DEBUG,
    log_request_headers=True,
    log_response_headers=True,
    log_request_body=True,
    log_response_body=True,
)

```

### Production Logging

```python
app.add_middleware(
    LoggingMiddleware,
    log_level=logging.INFO,
    log_request_headers=False,
    log_response_headers=False,
    exclude_paths={"/health", "/ready", "/live", "/metrics"},
)

```

### Custom Logger

```python
import logging

# Create custom logger
api_logger = logging.getLogger("api.requests")
api_logger.setLevel(logging.INFO)

# Add file handler
handler = logging.FileHandler("api_requests.log")
handler.setFormatter(logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
))
api_logger.addHandler(handler)

# Use custom logger
app.add_middleware(
    LoggingMiddleware,
    custom_logger=api_logger,
)

```

### JSON Logging

```python
import json
import logging

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        if hasattr(record, "extra"):
            log_data.update(record.extra)
        return json.dumps(log_data)

# Configure JSON logging
logger = logging.getLogger("api")
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)

app.add_middleware(LoggingMiddleware, custom_logger=logger)

```

### Sensitive Data Filtering

```python
app.add_middleware(
    LoggingMiddleware,
    log_request_headers=True,
    sensitive_headers={
        "authorization",
        "x-api-key",
        "cookie",
        "x-auth-token",
    },
)

```

Output:

```text
→ GET /api/users
  Headers: {"authorization": "[REDACTED]", "x-api-key": "[REDACTED]", "accept": "application/json"}

```

## Log Levels

| Level | Usage |
| ------- | ------- |
| `DEBUG` | Detailed debugging info, request/response bodies |
| `INFO` | Standard request logging |
| `WARNING` | 4xx responses |
| `ERROR` | 5xx responses, exceptions |

## Structured Logging Fields

When using a structured logger, these fields are available:

| Field | Description |
| ------- | ------------- |
| `method` | HTTP method |
| `path` | Request path |
| `status_code` | Response status |
| `duration_ms` | Request duration |
| `client_ip` | Client IP address |
| `request_id` | Request ID (if available) |
| `user_agent` | User-Agent header |

## Path Exclusion

Exclude noisy endpoints:

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

## Integration with Request ID

Combine with RequestIDMiddleware for traceability:

```python
from fastmiddleware import LoggingMiddleware, RequestIDMiddleware

app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestIDMiddleware)

# Logs will include request ID

# → GET /api/users [req-id: abc-123-def]

# ← ✓ GET /api/users [200] 12.34ms [req-id: abc-123-def]

```

## Best Practices

1. **Don't log sensitive data** - Filter auth tokens, passwords
2. **Exclude health checks** - Avoid log spam from probes
3. **Use structured logging** - Easier to parse and analyze
4. **Set appropriate levels** - DEBUG in dev, INFO in prod
5. **Log request IDs** - Enable request tracing

## Performance Considerations

- Body logging adds overhead - disable in production
- High-volume APIs may generate significant log data
- Consider async logging for high throughput
- Use log sampling for extremely high-traffic endpoints

## Related Middlewares

- [RequestIDMiddleware](./request-id.md) - Add request IDs to logs
- [TimingMiddleware](./timing.md) - Request timing
- [MetricsMiddleware](./metrics.md) - Request metrics
