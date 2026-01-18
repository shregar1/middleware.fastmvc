# TimingMiddleware

Adds request processing time to response headers for performance monitoring and debugging.

## Installation

```python
from fastmiddleware import TimingMiddleware

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import TimingMiddleware

app = FastAPI()

app.add_middleware(TimingMiddleware)

```

## Configuration

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `header_name` | `str` | `"X-Process-Time"` | Response header name |
| `include_unit` | `bool` | `True` | Include "ms" suffix |
| `precision` | `int` | `2` | Decimal precision |

## Response Header

Default format:

```http
X-Process-Time: 12.34ms

```

## Examples

### Default Configuration

```python
app.add_middleware(TimingMiddleware)

# Response header: X-Process-Time: 12.34ms

```

### Custom Header Name

```python
app.add_middleware(
    TimingMiddleware,
    header_name="X-Response-Time",
)

# Response header: X-Response-Time: 12.34ms

```

### Without Unit

```python
app.add_middleware(
    TimingMiddleware,
    include_unit=False,
)

# Response header: X-Process-Time: 12.34

```

### Higher Precision

```python
app.add_middleware(
    TimingMiddleware,
    precision=4,
)

# Response header: X-Process-Time: 12.3456ms

```

### Server-Timing Header

For browser DevTools compatibility:

```python
app.add_middleware(
    TimingMiddleware,
    header_name="Server-Timing",
    include_unit=False,
)

# Response header: Server-Timing: 12.34

```

## Use Cases

### Performance Monitoring

```python

# In your monitoring system
response = requests.get("https://api.example.com/data")
process_time = float(response.headers["X-Process-Time"].rstrip("ms"))

if process_time > 1000:  # Over 1 second
    alert("Slow response detected")

```

### Load Balancer Health Checks

Some load balancers can use response time for routing:

```nginx

# nginx upstream health check
upstream backend {
    server backend1:8000 max_fails=3 fail_timeout=30s;
    server backend2:8000 max_fails=3 fail_timeout=30s;
}

```

### Client-Side Performance Tracking

```javascript
// Browser JavaScript
fetch('/api/data')
    .then(response => {
        const processTime = response.headers.get('X-Process-Time');
        console.log(`Server processing time: ${processTime}`);
        analytics.track('api_latency', { time: processTime });
        return response.json();
    });

```

## What's Measured

The timing includes:

- ✅ Route handler execution

- ✅ Dependency injection

- ✅ Response serialization

- ❌ Network latency (client to server)

- ❌ TLS handshake

- ❌ Reverse proxy overhead

## Placement in Middleware Stack

For accurate timing, place TimingMiddleware early (it's executed late due to middleware order):

```python

# First added = last executed

# Last added = first executed

# Add early in the list
app.add_middleware(TimingMiddleware)  # Add first
app.add_middleware(LoggingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(AuthenticationMiddleware)
app.add_middleware(CORSMiddleware)  # Add last

```

This ensures timing measures the entire request lifecycle.

## Path Exclusion

Exclude paths from timing:

```python
app.add_middleware(
    TimingMiddleware,
    exclude_paths={"/health", "/metrics"},
)

```

## Combining with Logging

```python
from fastmiddleware import TimingMiddleware, LoggingMiddleware

# TimingMiddleware will add the header

# LoggingMiddleware will log it
app.add_middleware(LoggingMiddleware, log_response_headers=True)
app.add_middleware(TimingMiddleware)

```

Log output:

```text
← ✓ GET /api/users [200] 12.34ms
  Headers: {"x-process-time": "12.34ms", ...}

```

## Best Practices

1. **Keep it enabled in production** - Minimal overhead, valuable data
2. **Use consistent header names** - Easier to parse in monitoring
3. **Track percentiles, not averages** - P95, P99 are more meaningful
4. **Correlate with other metrics** - CPU, memory, database time
5. **Set SLOs based on timing data** - Define acceptable latencies

## Performance Impact

- Overhead: ~0.01ms per request
- Memory: Negligible
- Safe for high-traffic production use

## Related Middlewares

- [LoggingMiddleware](./logging.md) - Log timing data
- [MetricsMiddleware](./metrics.md) - Collect timing metrics
- [RequestIDMiddleware](./request-id.md) - Correlate timing with requests
