# FastMVC Middleware API Reference

This document provides detailed API documentation for all middleware components.

## Table of Contents

- [Base Class](#base-class)
- [Security Middlewares](#security-middlewares)
- [Observability Middlewares](#observability-middlewares)
- [Resilience Middlewares](#resilience-middlewares)
- [Performance Middlewares](#performance-middlewares)
- [Operations Middlewares](#operations-middlewares)
- [Helper Functions](#helper-functions)

---

## Base Class

### `FastMVCMiddleware`

Base class for all FastMVC middlewares.

```python
from src import FastMVCMiddleware

class FastMVCMiddleware(BaseHTTPMiddleware):
    """Base middleware class with common functionality."""
    
    def __init__(
        self,
        app,
        exclude_paths: Set[str] | None = None,
        exclude_methods: Set[str] | None = None,
    ) -> None:
        """Initialize the middleware.
        
        Args:
            app: The ASGI application to wrap.
            exclude_paths: Set of paths to skip middleware processing.
            exclude_methods: Set of HTTP methods to skip.
        """
```

**Methods:**

| Method | Description |
|--------|-------------|
| `dispatch(request, call_next)` | Abstract method to process requests |
| `should_skip(request)` | Check if request should skip processing |
| `get_client_ip(request)` | Get client IP, respecting X-Forwarded-For |

**Example - Creating Custom Middleware:**

```python
class MyMiddleware(FastMVCMiddleware):
    async def dispatch(self, request, call_next):
        if self.should_skip(request):
            return await call_next(request)
        
        # Your logic here
        response = await call_next(request)
        return response
```

---

## Security Middlewares

### `SecurityHeadersMiddleware`

Adds security headers to all responses.

```python
from src import SecurityHeadersMiddleware, SecurityHeadersConfig
```

**Class: `SecurityHeadersConfig`**

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `enable_hsts` | `bool` | `False` | Enable HSTS header |
| `hsts_max_age` | `int` | `31536000` | HSTS max-age in seconds |
| `hsts_preload` | `bool` | `False` | Add preload directive |
| `hsts_include_subdomains` | `bool` | `True` | Include subdomains |
| `content_security_policy` | `str \| None` | `None` | CSP header value |
| `x_frame_options` | `str` | `"DENY"` | X-Frame-Options value |
| `x_content_type_options` | `str` | `"nosniff"` | X-Content-Type-Options |
| `referrer_policy` | `str` | `"strict-origin-when-cross-origin"` | Referrer-Policy |
| `permissions_policy` | `str \| None` | `None` | Permissions-Policy |
| `cross_origin_opener_policy` | `str` | `"same-origin"` | COOP value |
| `cross_origin_resource_policy` | `str` | `"same-origin"` | CORP value |

**Class: `SecurityHeadersMiddleware`**

```python
SecurityHeadersMiddleware(
    app,
    config: SecurityHeadersConfig | None = None,
    enable_hsts: bool | None = None,
    content_security_policy: str | None = None,
    x_frame_options: str | None = None,
    exclude_paths: Set[str] | None = None,
    exclude_methods: Set[str] | None = None,
)
```

---

### `TrustedHostMiddleware`

Validates the Host header against allowed hosts.

```python
from src import TrustedHostMiddleware, TrustedHostConfig
```

**Class: `TrustedHostConfig`**

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `allowed_hosts` | `Sequence[str]` | `["*"]` | Allowed host patterns |
| `www_redirect` | `bool` | `False` | Redirect www to non-www |
| `redirect_to_primary` | `bool` | `False` | Redirect to primary host |
| `primary_host` | `str \| None` | `None` | Primary host for redirects |

**Host Patterns:**
- `"example.com"` - Exact match
- `"*.example.com"` - Wildcard subdomain
- `"*"` - Allow any host (development only)

---

### `CORSMiddleware`

Cross-Origin Resource Sharing support.

```python
from src import CORSMiddleware
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `allow_origins` | `list[str]` | `[]` | Allowed origins |
| `allow_methods` | `list[str]` | `["GET", "POST", ...]` | Allowed HTTP methods |
| `allow_headers` | `list[str]` | `["*"]` | Allowed headers |
| `allow_credentials` | `bool` | `True` | Allow cookies/auth |
| `expose_headers` | `list[str]` | `[]` | Headers to expose |
| `max_age` | `int` | `600` | Preflight cache time |

---

### `AuthenticationMiddleware`

Pluggable authentication middleware.

```python
from src import (
    AuthenticationMiddleware,
    AuthConfig,
    JWTAuthBackend,
    APIKeyAuthBackend,
)
```

**Class: `AuthConfig`**

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `exclude_paths` | `Set[str]` | Health/docs paths | Paths without auth |
| `exclude_methods` | `Set[str]` | `{"OPTIONS"}` | Methods without auth |
| `header_name` | `str` | `"Authorization"` | Auth header name |
| `header_scheme` | `str` | `"Bearer"` | Auth scheme |
| `error_message` | `str` | `"Authentication required"` | Error message |
| `error_status_code` | `int` | `401` | Error status code |

**Class: `JWTAuthBackend`**

```python
JWTAuthBackend(
    secret: str,
    algorithm: str = "HS256",
    verify_exp: bool = True,
    audience: str | None = None,
    issuer: str | None = None,
)
```

| Method | Description |
|--------|-------------|
| `authenticate(token)` | Returns decoded payload or None |

**Class: `APIKeyAuthBackend`**

```python
APIKeyAuthBackend(
    valid_keys: Set[str] | None = None,
    validator: Callable[[str], Awaitable[dict | None]] | None = None,
    header_name: str = "X-API-Key",
)
```

---

## Observability Middlewares

### `LoggingMiddleware`

Request/response logging.

```python
from src import LoggingMiddleware
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `log_level` | `int` | `logging.INFO` | Log level |
| `log_request_body` | `bool` | `False` | Log request bodies |
| `log_response_body` | `bool` | `False` | Log response bodies |
| `log_request_headers` | `bool` | `False` | Log request headers |
| `log_response_headers` | `bool` | `False` | Log response headers |
| `custom_logger` | `Logger \| None` | `None` | Custom logger instance |
| `exclude_paths` | `Set[str]` | Health/metrics | Paths to skip |

---

### `TimingMiddleware`

Adds processing time header.

```python
from src import TimingMiddleware
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `header_name` | `str` | `"X-Process-Time"` | Response header name |
| `include_unit` | `bool` | `True` | Include "ms" suffix |
| `precision` | `int` | `2` | Decimal precision |

---

### `RequestIDMiddleware`

Generates/propagates request IDs.

```python
from src import RequestIDMiddleware
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `header_name` | `str` | `"X-Request-ID"` | Header name |
| `generator` | `Callable` | UUID4 | ID generator |
| `trust_incoming` | `bool` | `True` | Trust incoming IDs |

**Request State:**
- `request.state.request_id` - The request ID

---

### `RequestContextMiddleware`

Async-safe request context.

```python
from src import (
    RequestContextMiddleware,
    get_request_id,
    get_request_context,
)
```

**Helper Functions:**

| Function | Returns | Description |
|----------|---------|-------------|
| `get_request_id()` | `str \| None` | Current request ID |
| `get_request_context()` | `dict` | Full context dict |

**Context Keys:**
- `request_id` - Request identifier
- `start_time` - Request start (datetime)
- `client_ip` - Client IP address
- `method` - HTTP method
- `path` - Request path

---

### `MetricsMiddleware`

Prometheus metrics collection.

```python
from src import MetricsMiddleware, MetricsConfig, MetricsCollector
```

**Class: `MetricsConfig`**

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `metrics_path` | `str` | `"/metrics"` | Metrics endpoint path |
| `histogram_buckets` | `tuple` | `(0.01, ...)` | Latency buckets |
| `enable_latency_histogram` | `bool` | `True` | Track latency |
| `enable_request_count` | `bool` | `True` | Count requests |
| `enable_response_size` | `bool` | `True` | Track response size |
| `path_patterns` | `dict` | `{}` | Path normalization |

**Class: `MetricsCollector`**

| Method | Description |
|--------|-------------|
| `record_request(method, path, status, latency, size)` | Record a request |
| `get_metrics()` | Get Prometheus format |
| `get_json_metrics()` | Get JSON format |

---

## Resilience Middlewares

### `RateLimitMiddleware`

Rate limiting with sliding window.

```python
from src import (
    RateLimitMiddleware,
    RateLimitConfig,
    RateLimitStore,
    InMemoryRateLimitStore,
)
```

**Class: `RateLimitConfig`**

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `requests_per_minute` | `int` | `60` | Requests per minute |
| `requests_per_hour` | `int \| None` | `None` | Requests per hour |
| `burst_limit` | `int \| None` | `None` | Burst limit |
| `key_func` | `Callable` | IP-based | Key extraction |
| `error_message` | `str` | `"Rate limit exceeded"` | Error message |

**Abstract Class: `RateLimitStore`**

| Method | Description |
|--------|-------------|
| `check_rate_limit(key, limit, window)` | Check if rate limited |
| `record_request(key)` | Record a request |
| `get_remaining(key, limit, window)` | Get remaining requests |

---

### `ErrorHandlerMiddleware`

Centralized error handling.

```python
from src import ErrorHandlerMiddleware, ErrorConfig
```

**Class: `ErrorConfig`**

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `include_traceback` | `bool` | `False` | Include stack trace |
| `include_exception_type` | `bool` | `False` | Include exception class |
| `log_exceptions` | `bool` | `True` | Log exceptions |
| `default_message` | `str` | `"An internal error occurred"` | Default message |
| `status_code` | `int` | `500` | Default status code |
| `error_handlers` | `dict` | `{}` | Custom exception handlers |

**Custom Handlers:**

```python
config = ErrorConfig()
config.error_handlers[ValueError] = (400, "Invalid value")
config.error_handlers[PermissionError] = (403, "Forbidden")
```

---

### `IdempotencyMiddleware`

Idempotency key support.

```python
from src import (
    IdempotencyMiddleware,
    IdempotencyConfig,
    IdempotencyStore,
    InMemoryIdempotencyStore,
)
```

**Class: `IdempotencyConfig`**

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `header_name` | `str` | `"Idempotency-Key"` | Header name |
| `ttl_seconds` | `int` | `86400` | Cache TTL |
| `require_key` | `bool` | `False` | Require key |
| `required_methods` | `Set[str]` | POST/PUT/PATCH | Methods to apply |

**Response Headers:**
- `X-Idempotent-Replayed: true` - When returning cached response

---

## Performance Middlewares

### `CompressionMiddleware`

GZip response compression.

```python
from src import CompressionMiddleware, CompressionConfig
```

**Class: `CompressionConfig`**

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `minimum_size` | `int` | `500` | Minimum bytes |
| `compression_level` | `int` | `6` | GZip level (1-9) |
| `compressible_types` | `tuple` | JSON/HTML/etc | MIME types |

---

### `CacheMiddleware`

HTTP caching with ETags.

```python
from src import CacheMiddleware, CacheConfig, InMemoryCacheStore
```

**Class: `CacheConfig`**

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `default_max_age` | `int` | `0` | Default cache time |
| `enable_etag` | `bool` | `True` | Generate ETags |
| `private` | `bool` | `False` | Private cache |
| `no_store` | `bool` | `False` | No caching |
| `vary_headers` | `tuple` | Accept headers | Vary headers |
| `path_rules` | `dict` | `{}` | Path-specific rules |
| `cacheable_methods` | `Set[str]` | GET/HEAD | Cacheable methods |
| `cacheable_status_codes` | `Set[int]` | 200/301/etc | Cacheable codes |

**Path Rules:**

```python
config = CacheConfig(
    path_rules={
        "/static": {"max_age": 86400, "public": True},
        "/api": {"no_store": True},
    }
)
```

---

## Operations Middlewares

### `HealthCheckMiddleware`

Health check endpoints.

```python
from src import HealthCheckMiddleware, HealthConfig
```

**Class: `HealthConfig`**

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `health_path` | `str` | `"/health"` | Health endpoint |
| `ready_path` | `str` | `"/ready"` | Readiness endpoint |
| `live_path` | `str` | `"/live"` | Liveness endpoint |
| `version` | `str \| None` | `None` | Service version |
| `service_name` | `str \| None` | `None` | Service name |
| `include_details` | `bool` | `True` | Include details |
| `custom_checks` | `dict` | `{}` | Custom health checks |

**Custom Checks:**

```python
async def check_database():
    return await db.is_connected()

config = HealthConfig(
    custom_checks={"database": check_database}
)
```

**Endpoints:**

| Endpoint | Success | Failure | Description |
|----------|---------|---------|-------------|
| `/health` | 200 | 503 | Full health status |
| `/ready` | 200 | 503 | Readiness status |
| `/live` | 200 | - | Always returns 200 |

---

### `MaintenanceMiddleware`

Maintenance mode control.

```python
from src import MaintenanceMiddleware, MaintenanceConfig
```

**Class: `MaintenanceConfig`**

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `enabled` | `bool` | `False` | Enable maintenance |
| `message` | `str` | Default message | User-facing message |
| `retry_after` | `int` | `300` | Retry-After seconds |
| `allowed_paths` | `Set[str]` | `/health` etc | Bypassed paths |
| `allowed_ips` | `Set[str]` | `set()` | Bypassed IPs |
| `bypass_token` | `str \| None` | `None` | Bypass token |
| `bypass_header` | `str` | `"X-Maintenance-Bypass"` | Bypass header |
| `use_html` | `bool` | `False` | Return HTML |
| `html_template` | `str \| None` | `None` | Custom template |

**Dynamic Control:**

```python
middleware = MaintenanceMiddleware(app, config=config)

# Enable/disable at runtime
middleware.enable(message="Deploying", retry_after=600)
middleware.disable()
middleware.is_enabled()
```

---

## Helper Functions

### Request Context Helpers

```python
from src import get_request_id, get_request_context
```

| Function | Returns | Description |
|----------|---------|-------------|
| `get_request_id()` | `str \| None` | Current request ID |
| `get_request_context()` | `dict` | Full request context |

**Usage:**

```python
async def my_service():
    request_id = get_request_id()
    ctx = get_request_context()
    
    logger.info(f"Processing {request_id}", extra=ctx)
```

---

## Version Information

```python
from src import __version__, __author__, __license__

print(__version__)  # "0.1.0"
print(__author__)   # "Shiv"
print(__license__)  # "MIT"
```

