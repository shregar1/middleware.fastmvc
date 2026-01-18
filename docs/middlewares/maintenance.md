# MaintenanceMiddleware

Enable maintenance mode with 503 responses, bypass options, and customizable maintenance pages.

## Installation

```python
from fastmiddleware import MaintenanceMiddleware, MaintenanceConfig

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import MaintenanceMiddleware

app = FastAPI()

config = MaintenanceConfig(enabled=False)
middleware = MaintenanceMiddleware(app, config=config)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `enabled` | `bool` | `False` | Enable maintenance |
| `message` | `str` | Default message | Maintenance message |
| `retry_after` | `int` | `300` | Retry-After seconds |
| `allowed_paths` | `set` | Health paths | Bypassed paths |
| `allowed_ips` | `set` | `set()` | Bypassed IPs |
| `bypass_token` | `str` | `None` | Bypass token |
| `use_html` | `bool` | `False` | Return HTML page |

## Examples

### Basic Usage

```python
config = MaintenanceConfig(
    enabled=True,
    message="We're upgrading!",
    retry_after=1800,
)
app.add_middleware(MaintenanceMiddleware, config=config)

```

### Dynamic Toggle

```python
middleware = MaintenanceMiddleware(app, config=config)

# Enable at runtime
middleware.enable(message="Deploying", retry_after=300)

# Disable
middleware.disable()

# Check status
if middleware.is_enabled():
    print("Maintenance mode active")

```

### Bypass Options

```python
config = MaintenanceConfig(
    enabled=True,
    allowed_paths={"/health", "/status"},
    allowed_ips={"10.0.0.1"},
    bypass_token="secret-admin-token",
)

```

Bypass header:

```http
X-Maintenance-Bypass: secret-admin-token

```

### HTML Page

```python
config = MaintenanceConfig(
    enabled=True,
    use_html=True,
    message="We're upgrading our systems.",
)

```

## Response

### JSON (default)

```json
{
    "error": true,
    "message": "Service temporarily unavailable for maintenance",
    "maintenance": true,
    "retry_after": 300
}

```

### Headers

```http
HTTP/1.1 503 Service Unavailable
Retry-After: 300
X-Maintenance-Mode: true

```

## Best Practices

1. Always exclude health endpoints
2. Use bypass tokens for admin access
3. Set appropriate retry_after times
4. Monitor maintenance mode status
