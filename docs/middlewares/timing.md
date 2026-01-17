# TimingMiddleware

Adds request processing time to response headers for performance monitoring.

## Installation

```python
from src import TimingMiddleware
```

## Quick Start

```python
from fastapi import FastAPI
from src import TimingMiddleware

app = FastAPI()

app.add_middleware(TimingMiddleware)
```

## Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `header_name` | `str` | `"X-Process-Time"` | Response header name |
| `include_unit` | `bool` | `True` | Include "ms" suffix |
| `precision` | `int` | `2` | Decimal precision |

## Response Header

```http
HTTP/1.1 200 OK
X-Process-Time: 12.34ms
```

## Examples

### Default Configuration

```python
app.add_middleware(TimingMiddleware)
```

Response: `X-Process-Time: 12.34ms`

### Custom Header Name

```python
app.add_middleware(
    TimingMiddleware,
    header_name="X-Response-Time",
)
```

Response: `X-Response-Time: 12.34ms`

### Without Unit Suffix

```python
app.add_middleware(
    TimingMiddleware,
    include_unit=False,
)
```

Response: `X-Process-Time: 12.34`

### Higher Precision

```python
app.add_middleware(
    TimingMiddleware,
    precision=4,
)
```

Response: `X-Process-Time: 12.3456ms`

### Server-Timing Header

For browser DevTools compatibility:

```python
app.add_middleware(
    TimingMiddleware,
    header_name="Server-Timing",
    include_unit=False,
)
```

Response: `Server-Timing: total;dur=12.34`

## Use Cases

### Performance Monitoring

Track response times for performance analysis:

```python
# Client-side JavaScript
const response = await fetch('/api/data');
const processTime = response.headers.get('X-Process-Time');
console.log(`API took ${processTime}`);
```

### SLA Monitoring

Check if response times meet SLA:

```python
import httpx

async def check_sla():
    response = await httpx.get("https://api.example.com/health")
    time_str = response.headers.get("X-Process-Time", "0ms")
    time_ms = float(time_str.replace("ms", ""))
    
    if time_ms > 200:
        alert("Response time exceeds SLA!")
```

### Load Testing Analysis

Collect timing data during load tests:

```bash
# Using curl
curl -i https://api.example.com/data 2>&1 | grep X-Process-Time

# Using hey (load testing)
hey -n 1000 -c 10 https://api.example.com/data
```

## Middleware Order

Place `TimingMiddleware` early (one of the first added) to measure total request time including other middleware:

```python
# First added = last executed = measures total time
app.add_middleware(TimingMiddleware)  # Add first!

# Other middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(AuthenticationMiddleware)
```

## Combining with Logging

```python
from src import TimingMiddleware, LoggingMiddleware

# Timing captures total time
app.add_middleware(TimingMiddleware)

# Logging also shows time in logs
app.add_middleware(LoggingMiddleware)
```

Log output includes timing:
```
← ✓ GET /api/users [200] 12.34ms
```

## Related

- [LoggingMiddleware](logging.md) - Request logging
- [MetricsMiddleware](metrics.md) - Prometheus metrics

