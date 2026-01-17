# MetricsMiddleware

Collects request metrics and exposes a Prometheus-compatible `/metrics` endpoint.

## Installation

```python
from src import MetricsMiddleware, MetricsConfig
```

## Quick Start

```python
from fastapi import FastAPI
from src import MetricsMiddleware

app = FastAPI()

app.add_middleware(MetricsMiddleware)
```

## Configuration

### MetricsConfig

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `metrics_path` | `str` | `"/metrics"` | Metrics endpoint path |
| `histogram_buckets` | `tuple` | `(0.01, ...)` | Latency histogram buckets |
| `enable_latency_histogram` | `bool` | `True` | Track request latency |
| `enable_request_count` | `bool` | `True` | Count requests |
| `enable_response_size` | `bool` | `True` | Track response sizes |
| `path_patterns` | `dict` | `{}` | Path normalization patterns |

## Metrics Collected

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `fastmvc_http_requests_total` | Counter | method, path, status | Total HTTP requests |
| `fastmvc_http_request_duration_seconds` | Histogram | method, path | Request latency |
| `fastmvc_http_response_size_bytes` | Summary | method, path | Response size |
| `fastmvc_http_errors_total` | Counter | method, path | 5xx errors count |
| `fastmvc_uptime_seconds` | Gauge | - | Service uptime |

## Examples

### Basic Configuration

```python
app.add_middleware(MetricsMiddleware)

# Access metrics at GET /metrics
```

### Custom Metrics Path

```python
from src import MetricsMiddleware, MetricsConfig

config = MetricsConfig(
    metrics_path="/prometheus",
)

app.add_middleware(MetricsMiddleware, config=config)
```

### Path Normalization

Prevent high-cardinality labels from dynamic paths:

```python
config = MetricsConfig(
    path_patterns={
        r"/users/\d+": "/users/{id}",
        r"/orders/[a-f0-9-]+": "/orders/{uuid}",
        r"/products/[\w-]+": "/products/{slug}",
    },
)

app.add_middleware(MetricsMiddleware, config=config)
```

Before: `/users/123`, `/users/456`, `/users/789`
After: All grouped under `/users/{id}`

### Custom Histogram Buckets

```python
config = MetricsConfig(
    histogram_buckets=(
        0.005,  # 5ms
        0.01,   # 10ms
        0.025,  # 25ms
        0.05,   # 50ms
        0.1,    # 100ms
        0.25,   # 250ms
        0.5,    # 500ms
        1.0,    # 1s
        2.5,    # 2.5s
        5.0,    # 5s
        10.0,   # 10s
    ),
)
```

### Exclude Paths

```python
app.add_middleware(
    MetricsMiddleware,
    exclude_paths={"/health", "/ready", "/live"},
)
```

## Prometheus Format

```
# HELP fastmvc_http_requests_total Total HTTP requests
# TYPE fastmvc_http_requests_total counter
fastmvc_http_requests_total{method="GET",path="/api/users",status="200"} 1234
fastmvc_http_requests_total{method="POST",path="/api/users",status="201"} 56

# HELP fastmvc_http_request_duration_seconds HTTP request latency
# TYPE fastmvc_http_request_duration_seconds histogram
fastmvc_http_request_duration_seconds_bucket{method="GET",path="/api/users",le="0.01"} 100
fastmvc_http_request_duration_seconds_bucket{method="GET",path="/api/users",le="0.05"} 500
fastmvc_http_request_duration_seconds_bucket{method="GET",path="/api/users",le="0.1"} 800
fastmvc_http_request_duration_seconds_bucket{method="GET",path="/api/users",le="+Inf"} 1234
fastmvc_http_request_duration_seconds_sum{method="GET",path="/api/users"} 123.45
fastmvc_http_request_duration_seconds_count{method="GET",path="/api/users"} 1234

# HELP fastmvc_uptime_seconds Service uptime
# TYPE fastmvc_uptime_seconds gauge
fastmvc_uptime_seconds 3600.5
```

## Prometheus Configuration

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'my-api'
    static_configs:
      - targets: ['my-api:8000']
    metrics_path: /metrics
    scrape_interval: 15s
```

## Grafana Dashboards

### Request Rate

```promql
rate(fastmvc_http_requests_total[5m])
```

### Error Rate

```promql
rate(fastmvc_http_requests_total{status=~"5.."}[5m])
/ rate(fastmvc_http_requests_total[5m])
```

### Latency (P50, P95, P99)

```promql
# P50
histogram_quantile(0.5, rate(fastmvc_http_request_duration_seconds_bucket[5m]))

# P95
histogram_quantile(0.95, rate(fastmvc_http_request_duration_seconds_bucket[5m]))

# P99
histogram_quantile(0.99, rate(fastmvc_http_request_duration_seconds_bucket[5m]))
```

### Requests per Path

```promql
sum by (path) (rate(fastmvc_http_requests_total[5m]))
```

### Error Rate by Status

```promql
sum by (status) (rate(fastmvc_http_requests_total{status=~"[45].."}[5m]))
```

## Alerting Examples

### High Error Rate

```yaml
# alerts.yml
groups:
  - name: api-alerts
    rules:
      - alert: HighErrorRate
        expr: |
          rate(fastmvc_http_requests_total{status=~"5.."}[5m])
          / rate(fastmvc_http_requests_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: High error rate (> 5%)
```

### Slow Responses

```yaml
      - alert: SlowResponses
        expr: |
          histogram_quantile(0.95, rate(fastmvc_http_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: 95th percentile latency > 1s
```

## JSON Metrics

For non-Prometheus systems, get JSON format:

```python
from src import MetricsCollector

collector = MetricsCollector(config)
json_metrics = collector.get_json_metrics()

# Returns:
{
    "total_requests": 1234,
    "total_errors": 5,
    "uptime_seconds": 3600.5,
    "requests_by_path": {...},
    "latency_percentiles": {...},
}
```

## Best Practices

1. **Normalize paths** - Prevent high-cardinality labels
2. **Exclude health checks** - Don't pollute metrics
3. **Set appropriate buckets** - Match your SLA targets
4. **Monitor the metrics endpoint** - Ensure it doesn't get rate limited
5. **Use alerting** - React to issues proactively

## Related

- [HealthCheckMiddleware](health.md) - Health endpoints
- [TimingMiddleware](timing.md) - Response timing

