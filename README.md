# FastMVC Middleware

[![PyPI version](https://badge.fury.io/py/fastmvc-middleware.svg)](https://badge.fury.io/py/fastmvc-middleware)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/hyyre/fastmvc-middleware/actions/workflows/ci.yml/badge.svg)](https://github.com/hyyre/fastmvc-middleware/actions)
[![Coverage](https://img.shields.io/badge/coverage-82%25-green.svg)](https://github.com/hyyre/fastmvc-middleware)

**Production-ready middleware collection for FastAPI/Starlette applications.**

A comprehensive set of 16 battle-tested, configurable middleware components for building robust APIs with security, observability, rate limiting, caching, and authentication built-in.

## ✨ Features

| Category | Middlewares |
|----------|-------------|
| 🔒 **Security** | Security Headers, Trusted Host, CORS, Authentication |
| 📊 **Observability** | Logging, Timing, Request ID, Request Context, Metrics |
| 🛡️ **Resilience** | Rate Limiting, Error Handling, Idempotency |
| ⚡ **Performance** | Compression, Caching |
| 🔧 **Operations** | Health Checks, Maintenance Mode |

## 📦 Installation

```bash
pip install fastmvc-middleware
```

With JWT authentication support:
```bash
pip install fastmvc-middleware[jwt]
```

All optional dependencies:
```bash
pip install fastmvc-middleware[all]
```

## 🚀 Quick Start

```python
from fastapi import FastAPI
from src import (
    CORSMiddleware,
    SecurityHeadersMiddleware,
    LoggingMiddleware,
    TimingMiddleware,
    RequestIDMiddleware,
    HealthCheckMiddleware,
    CompressionMiddleware,
)

app = FastAPI()

# Add middleware (order matters - first added = last executed)
app.add_middleware(CompressionMiddleware)
app.add_middleware(TimingMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(SecurityHeadersMiddleware, enable_hsts=True)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(HealthCheckMiddleware, version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}
```

---

## 📚 Middleware Reference

### Table of Contents

**Security & Authentication**
- [SecurityHeadersMiddleware](#securityheadersmiddleware) - XSS, clickjacking protection
- [TrustedHostMiddleware](#trustedhostmiddleware) - Host header validation
- [CORSMiddleware](#corsmiddleware) - Cross-origin resource sharing
- [AuthenticationMiddleware](#authenticationmiddleware) - JWT & API key auth

**Observability**
- [LoggingMiddleware](#loggingmiddleware) - Request/response logging
- [TimingMiddleware](#timingmiddleware) - Processing time tracking
- [RequestIDMiddleware](#requestidmiddleware) - Unique request IDs
- [RequestContextMiddleware](#requestcontextmiddleware) - Async-safe context
- [MetricsMiddleware](#metricsmiddleware) - Prometheus metrics

**Resilience**
- [RateLimitMiddleware](#ratelimitmiddleware) - Rate limiting
- [ErrorHandlerMiddleware](#errorhandlermiddleware) - Error formatting
- [IdempotencyMiddleware](#idempotencymiddleware) - Safe retries

**Performance**
- [CompressionMiddleware](#compressionmiddleware) - GZip compression
- [CacheMiddleware](#cachemiddleware) - HTTP caching & ETags

**Operations**
- [HealthCheckMiddleware](#healthcheckmiddleware) - Health endpoints
- [MaintenanceMiddleware](#maintenancemiddleware) - Maintenance mode

---

## 🔒 Security & Authentication

### SecurityHeadersMiddleware

Adds comprehensive security headers to protect against common web vulnerabilities.

```python
from src import SecurityHeadersMiddleware, SecurityHeadersConfig

# Using individual parameters
app.add_middleware(
    SecurityHeadersMiddleware,
    enable_hsts=True,
    content_security_policy="default-src 'self'",
    x_frame_options="SAMEORIGIN",
)

# Using configuration object
config = SecurityHeadersConfig(
    enable_hsts=True,
    hsts_preload=True,
    hsts_max_age=31536000,
    content_security_policy="default-src 'self'; script-src 'self' 'unsafe-inline'",
)
app.add_middleware(SecurityHeadersMiddleware, config=config)
```

**Headers Added:**
| Header | Default Value | Description |
|--------|---------------|-------------|
| `X-Content-Type-Options` | `nosniff` | Prevents MIME type sniffing |
| `X-Frame-Options` | `DENY` | Prevents clickjacking |
| `X-XSS-Protection` | `1; mode=block` | XSS filter (legacy) |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Controls referrer info |
| `Content-Security-Policy` | Configurable | Controls resource loading |
| `Permissions-Policy` | Configurable | Controls browser features |
| `Strict-Transport-Security` | Optional | Forces HTTPS |
| `Cross-Origin-Opener-Policy` | `same-origin` | Isolates browsing context |
| `Cross-Origin-Resource-Policy` | `same-origin` | Controls cross-origin access |

---

### TrustedHostMiddleware

Validates the Host header to prevent host header attacks.

```python
from src import TrustedHostMiddleware

# Specific hosts
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["example.com", "www.example.com"],
)

# Wildcard subdomains
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*.example.com"],
)

# Allow any host (development only!)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],
)
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `allowed_hosts` | `list[str]` | `["*"]` | Allowed host patterns |
| `redirect_to_primary` | `bool` | `False` | Redirect to primary host |
| `primary_host` | `str` | `None` | Primary host for redirects |
| `www_redirect` | `bool` | `False` | Redirect www to non-www |

---

### CORSMiddleware

Cross-origin resource sharing with sensible defaults.

```python
from src import CORSMiddleware

# Production (specific origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com", "https://app.example.com"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    allow_credentials=True,
    max_age=600,
)

# Development (all origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # Required when using "*"
)
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `allow_origins` | `list[str]` | `[]` | Allowed origins |
| `allow_methods` | `list[str]` | `["GET", "POST", ...]` | Allowed HTTP methods |
| `allow_headers` | `list[str]` | `["*"]` | Allowed headers |
| `allow_credentials` | `bool` | `True` | Allow credentials |
| `expose_headers` | `list[str]` | `[]` | Exposed headers |
| `max_age` | `int` | `600` | Preflight cache time |

---

### AuthenticationMiddleware

Pluggable authentication with support for JWT tokens and API keys.

```python
from src import (
    AuthenticationMiddleware,
    AuthConfig,
    JWTAuthBackend,
    APIKeyAuthBackend,
)

# JWT Authentication
jwt_backend = JWTAuthBackend(
    secret="your-secret-key",
    algorithm="HS256",
    verify_exp=True,
)

config = AuthConfig(
    exclude_paths={"/login", "/register", "/health", "/docs", "/openapi.json"},
)

app.add_middleware(
    AuthenticationMiddleware,
    backend=jwt_backend,
    config=config,
)

# Access authenticated user in routes
@app.get("/protected")
async def protected(request: Request):
    user_data = request.state.auth  # Contains decoded JWT payload
    return {"user": user_data}
```

**API Key Authentication:**

```python
# Static keys
backend = APIKeyAuthBackend(valid_keys={"key1", "key2"})

# Dynamic validation
async def validate_api_key(key: str):
    user = await db.get_user_by_api_key(key)
    if user:
        return {"user_id": user.id, "tier": user.tier}
    return None

backend = APIKeyAuthBackend(validator=validate_api_key)
```

**AuthConfig Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `exclude_paths` | `set[str]` | Health/docs paths | Paths without auth |
| `exclude_methods` | `set[str]` | `{"OPTIONS"}` | Methods without auth |
| `header_name` | `str` | `"Authorization"` | Auth header name |
| `header_scheme` | `str` | `"Bearer"` | Auth scheme |
| `error_message` | `str` | `"Authentication required"` | Error message |

---

## 📊 Observability

### LoggingMiddleware

Structured request/response logging with configurable verbosity.

```python
from src import LoggingMiddleware
import logging

app.add_middleware(
    LoggingMiddleware,
    log_level=logging.INFO,
    log_request_headers=True,
    log_response_headers=False,
    exclude_paths={"/health", "/metrics"},
)
```

**Log Output:**
```
→ GET /api/users
← ✓ GET /api/users [200] 12.34ms
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `log_level` | `int` | `INFO` | Logging level |
| `log_request_body` | `bool` | `False` | Log request bodies |
| `log_response_body` | `bool` | `False` | Log response bodies |
| `log_request_headers` | `bool` | `False` | Log request headers |
| `log_response_headers` | `bool` | `False` | Log response headers |
| `exclude_paths` | `set[str]` | Health/metrics | Paths to skip |
| `custom_logger` | `Logger` | `None` | Custom logger |

---

### TimingMiddleware

Adds request processing time to response headers.

```python
from src import TimingMiddleware

app.add_middleware(
    TimingMiddleware,
    header_name="X-Process-Time",
    include_unit=True,
    precision=2,
)
```

**Response Header:** `X-Process-Time: 12.34ms`

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `header_name` | `str` | `"X-Process-Time"` | Header name |
| `include_unit` | `bool` | `True` | Include "ms" suffix |
| `precision` | `int` | `2` | Decimal places |

---

### RequestIDMiddleware

Generates unique request identifiers for distributed tracing.

```python
from src import RequestIDMiddleware

app.add_middleware(
    RequestIDMiddleware,
    header_name="X-Request-ID",
    trust_incoming=True,  # Reuse IDs from upstream services
)

# Access in routes
@app.get("/")
async def root(request: Request):
    request_id = request.state.request_id
    return {"request_id": request_id}
```

**Response Header:** `X-Request-ID: 550e8400-e29b-41d4-a716-446655440000`

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `header_name` | `str` | `"X-Request-ID"` | Header name |
| `generator` | `Callable` | UUID4 | ID generator function |
| `trust_incoming` | `bool` | `True` | Trust incoming IDs |

---

### RequestContextMiddleware

Provides async-safe context variables accessible from anywhere in your code.

```python
from src import (
    RequestContextMiddleware,
    get_request_id,
    get_request_context,
)

app.add_middleware(RequestContextMiddleware)

# Access context from anywhere in async code
async def my_service_function():
    request_id = get_request_id()
    ctx = get_request_context()
    
    logger.info(
        f"Processing request {request_id}",
        extra={
            "client_ip": ctx["client_ip"],
            "path": ctx["path"],
        }
    )
```

**Context Data Available:**
| Key | Type | Description |
|-----|------|-------------|
| `request_id` | `str` | Unique request identifier |
| `start_time` | `datetime` | Request start time |
| `client_ip` | `str` | Client IP address |
| `method` | `str` | HTTP method |
| `path` | `str` | Request path |

---

### MetricsMiddleware

Collects request metrics and exposes a Prometheus-compatible endpoint.

```python
from src import MetricsMiddleware, MetricsConfig

# Basic usage
app.add_middleware(MetricsMiddleware)

# Custom configuration
config = MetricsConfig(
    metrics_path="/prometheus",
    histogram_buckets=(0.01, 0.05, 0.1, 0.5, 1.0, 5.0),
    path_patterns={
        r"/users/\d+": "/users/{id}",
        r"/orders/[a-f0-9-]+": "/orders/{uuid}",
    },
)
app.add_middleware(MetricsMiddleware, config=config)
```

**Metrics Collected:**
| Metric | Type | Description |
|--------|------|-------------|
| `fastmvc_http_requests_total` | Counter | Total requests by method/path/status |
| `fastmvc_http_request_duration_seconds` | Histogram | Request latency distribution |
| `fastmvc_http_response_size_bytes` | Summary | Response size |
| `fastmvc_http_errors_total` | Counter | 5xx error count |
| `fastmvc_uptime_seconds` | Gauge | Service uptime |

**Prometheus Configuration:**
```yaml
scrape_configs:
  - job_name: 'fastmvc-app'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: /metrics
```

---

## 🛡️ Resilience

### RateLimitMiddleware

Protects your API from abuse with configurable rate limiting.

```python
from src import RateLimitMiddleware, RateLimitConfig

# Basic usage - 60 requests per minute
app.add_middleware(RateLimitMiddleware)

# Custom limits
config = RateLimitConfig(
    requests_per_minute=100,
    requests_per_hour=1000,
    burst_limit=20,
)
app.add_middleware(RateLimitMiddleware, config=config)

# Custom key function (rate limit by user ID)
def get_user_key(request):
    user_id = getattr(request.state, "user_id", None)
    if user_id:
        return f"user:{user_id}"
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"

config = RateLimitConfig(key_func=get_user_key)
app.add_middleware(RateLimitMiddleware, config=config)
```

**Response Headers:**
| Header | Description |
|--------|-------------|
| `X-RateLimit-Limit` | Maximum requests allowed |
| `X-RateLimit-Remaining` | Remaining requests in window |
| `X-RateLimit-Reset` | Unix timestamp when limit resets |
| `Retry-After` | Seconds until allowed (when limited) |

**Custom Storage Backend:**
```python
from src import RateLimitStore

class RedisRateLimitStore(RateLimitStore):
    def __init__(self, redis_client):
        self.redis = redis_client
    
    async def check_rate_limit(self, key, limit, window):
        # Implement Redis-based rate limiting
        ...

app.add_middleware(
    RateLimitMiddleware,
    store=RedisRateLimitStore(redis),
)
```

---

### ErrorHandlerMiddleware

Catches exceptions and returns consistent error responses.

```python
from src import ErrorHandlerMiddleware, ErrorConfig

# Development mode (include traceback)
app.add_middleware(
    ErrorHandlerMiddleware,
    include_traceback=True,
    include_exception_type=True,
)

# Production mode
app.add_middleware(
    ErrorHandlerMiddleware,
    include_traceback=False,
    log_exceptions=True,
)

# Custom error handlers
config = ErrorConfig()
config.error_handlers[ValueError] = (400, "Invalid value provided")
config.error_handlers[PermissionError] = (403, "Permission denied")
config.error_handlers[FileNotFoundError] = (404, "Resource not found")

app.add_middleware(ErrorHandlerMiddleware, config=config)
```

**Response Format:**
```json
{
    "error": true,
    "message": "An internal error occurred",
    "status_code": 500,
    "request_id": "abc-123",
    "type": "ValueError",
    "detail": "invalid literal for int()",
    "traceback": ["..."]
}
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `include_traceback` | `bool` | `False` | Include stack trace |
| `include_exception_type` | `bool` | `False` | Include exception class |
| `log_exceptions` | `bool` | `True` | Log exceptions |
| `default_message` | `str` | `"An internal error occurred"` | Default error message |

---

### IdempotencyMiddleware

Provides idempotency key support for safe request retries.

```python
from src import IdempotencyMiddleware, IdempotencyConfig

# Basic usage
app.add_middleware(IdempotencyMiddleware)

# Custom configuration
config = IdempotencyConfig(
    header_name="X-Idempotency-Key",
    ttl_seconds=86400,  # 24 hours
    require_key=True,  # Require key for POST/PUT/PATCH
)
app.add_middleware(IdempotencyMiddleware, config=config)
```

**Client Usage:**
```bash
# First request
curl -X POST /api/payments \
  -H "Idempotency-Key: payment-123" \
  -d '{"amount": 100}'

# Retry with same key returns cached response
curl -X POST /api/payments \
  -H "Idempotency-Key: payment-123" \
  -d '{"amount": 100}'
```

**Response Headers:**
| Header | Description |
|--------|-------------|
| `X-Idempotent-Replayed` | `true` if response was cached |

**Custom Storage Backend:**
```python
from src import IdempotencyStore

class RedisIdempotencyStore(IdempotencyStore):
    async def get(self, key):
        data = await self.redis.get(f"idempotency:{key}")
        return json.loads(data) if data else None
    
    async def set(self, key, response_data, ttl):
        await self.redis.setex(f"idempotency:{key}", ttl, json.dumps(response_data))
    
    async def delete(self, key):
        await self.redis.delete(f"idempotency:{key}")
```

---

## ⚡ Performance

### CompressionMiddleware

GZip compression for HTTP responses.

```python
from src import CompressionMiddleware, CompressionConfig

# Basic usage
app.add_middleware(CompressionMiddleware)

# Custom configuration
config = CompressionConfig(
    minimum_size=500,      # Minimum bytes to compress
    compression_level=6,   # 1-9 (9 = best compression)
    compressible_types=(
        "application/json",
        "text/html",
        "text/css",
        "application/javascript",
    ),
)
app.add_middleware(CompressionMiddleware, config=config)
```

**Response Headers (when compressed):**
| Header | Value |
|--------|-------|
| `Content-Encoding` | `gzip` |
| `Vary` | `Accept-Encoding` |

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `minimum_size` | `int` | `500` | Min bytes to compress |
| `compression_level` | `int` | `6` | GZip level (1-9) |
| `compressible_types` | `tuple` | Common types | MIME types to compress |

---

### CacheMiddleware

HTTP caching with ETag generation and conditional requests.

```python
from src import CacheMiddleware, CacheConfig

# Basic usage with ETags
app.add_middleware(CacheMiddleware)

# Custom configuration
config = CacheConfig(
    default_max_age=3600,  # 1 hour
    enable_etag=True,
    private=False,  # Use public cache
    path_rules={
        "/api/static": {"max_age": 86400, "public": True},
        "/api/user": {"max_age": 0, "private": True, "no_store": True},
    },
)
app.add_middleware(CacheMiddleware, config=config)
```

**Response Headers:**
| Header | Example |
|--------|---------|
| `Cache-Control` | `public, max-age=3600` |
| `ETag` | `"abc123..."` |
| `Vary` | `Accept, Accept-Encoding` |

**Conditional Requests:**
Clients can send `If-None-Match` header with ETag to receive 304 Not Modified:

```bash
# First request
curl -i /api/data
# Returns: ETag: "abc123"

# Conditional request
curl -i -H "If-None-Match: \"abc123\"" /api/data
# Returns: 304 Not Modified (if unchanged)
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `default_max_age` | `int` | `0` | Default cache time |
| `enable_etag` | `bool` | `True` | Generate ETags |
| `private` | `bool` | `False` | Private cache |
| `no_store` | `bool` | `False` | Disable caching |
| `vary_headers` | `tuple` | `("Accept", ...)` | Vary headers |
| `path_rules` | `dict` | `{}` | Path-specific rules |

---

## 🔧 Operations

### HealthCheckMiddleware

Built-in health, readiness, and liveness endpoints.

```python
from src import HealthCheckMiddleware, HealthConfig

# Basic usage
app.add_middleware(HealthCheckMiddleware)

# With custom checks
async def check_database():
    return await database.is_connected()

async def check_redis():
    return await redis.ping()

config = HealthConfig(
    version="1.0.0",
    service_name="my-api",
    custom_checks={
        "database": check_database,
        "redis": check_redis,
    },
)
app.add_middleware(HealthCheckMiddleware, config=config)
```

**Endpoints:**
| Endpoint | Description | Response |
|----------|-------------|----------|
| `/health` | Full health status | Detailed health info |
| `/ready` | Readiness check | Ready status |
| `/live` | Liveness check | Alive status |

**Health Response:**
```json
{
    "status": "healthy",
    "timestamp": "2024-01-01T00:00:00Z",
    "uptime_seconds": 3600.5,
    "version": "1.0.0",
    "service": "my-api",
    "checks": {
        "database": "healthy",
        "redis": "healthy"
    }
}
```

**Kubernetes Configuration:**
```yaml
livenessProbe:
  httpGet:
    path: /live
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /ready
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 10
```

---

### MaintenanceMiddleware

Enable maintenance mode that returns 503 responses.

```python
from src import MaintenanceMiddleware, MaintenanceConfig

# Static configuration
config = MaintenanceConfig(
    enabled=False,  # Toggle to True to enable
    message="We're upgrading our systems. Please try again later.",
    retry_after=1800,  # 30 minutes
    allowed_paths={"/health", "/status"},
    allowed_ips={"10.0.0.1", "192.168.1.1"},
    bypass_token="secret-admin-token",
)

app.add_middleware(MaintenanceMiddleware, config=config)
```

**Dynamic Toggle:**
```python
# Get middleware instance
middleware = MaintenanceMiddleware(app, config=config)

# Enable at runtime
middleware.enable(message="Deploying new version", retry_after=300)

# Disable
middleware.disable()

# Check status
if middleware.is_enabled():
    print("Maintenance mode is active")
```

**Bypass Options:**
| Method | Example |
|--------|---------|
| Allowed paths | `/health`, `/status` |
| Allowed IPs | Admin IPs bypass |
| Bypass token | `X-Maintenance-Bypass: secret-token` |

**Response (503):**
```json
{
    "error": true,
    "message": "We're upgrading our systems. Please try again later.",
    "maintenance": true,
    "retry_after": 1800
}
```

**HTML Mode:**
```python
config = MaintenanceConfig(
    enabled=True,
    use_html=True,  # Return HTML page instead of JSON
    html_template="<html>...</html>",  # Custom template
)
```

---

## 🎯 Best Practices

### Middleware Order

The order in which you add middleware matters. Middleware is executed in **reverse order** of addition (last added = first executed).

```python
# Recommended order (add in this sequence):

# 1. Compression (outermost - compresses final response)
app.add_middleware(CompressionMiddleware)

# 2. Timing (measures total time)
app.add_middleware(TimingMiddleware)

# 3. Logging (logs request/response)
app.add_middleware(LoggingMiddleware)

# 4. Error Handler (catches exceptions)
app.add_middleware(ErrorHandlerMiddleware)

# 5. Security Headers
app.add_middleware(SecurityHeadersMiddleware)

# 6. Cache (before rate limiting)
app.add_middleware(CacheMiddleware)

# 7. Rate Limiting (before auth)
app.add_middleware(RateLimitMiddleware)

# 8. Idempotency
app.add_middleware(IdempotencyMiddleware)

# 9. Authentication
app.add_middleware(AuthenticationMiddleware, backend=backend)

# 10. Request Context (innermost)
app.add_middleware(RequestContextMiddleware)

# 11. Health Check
app.add_middleware(HealthCheckMiddleware)

# 12. Metrics
app.add_middleware(MetricsMiddleware)

# 13. Trusted Host
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["..."])

# 14. CORS (must be last added = first executed)
app.add_middleware(CORSMiddleware, allow_origins=["..."])
```

### Production Configuration

```python
import os
from src import (
    CompressionMiddleware,
    SecurityHeadersMiddleware,
    RateLimitMiddleware,
    RateLimitConfig,
    AuthenticationMiddleware,
    JWTAuthBackend,
    LoggingMiddleware,
    RequestContextMiddleware,
    HealthCheckMiddleware,
    MetricsMiddleware,
    ErrorHandlerMiddleware,
    CORSMiddleware,
    TrustedHostMiddleware,
)

# Compression
app.add_middleware(CompressionMiddleware, minimum_size=1000)

# Error handling (production - no traceback)
app.add_middleware(ErrorHandlerMiddleware, log_exceptions=True)

# Security with HSTS
app.add_middleware(
    SecurityHeadersMiddleware,
    enable_hsts=True,
    hsts_preload=True,
    content_security_policy="default-src 'self'",
)

# Rate limiting
app.add_middleware(
    RateLimitMiddleware,
    config=RateLimitConfig(
        requests_per_minute=100,
        requests_per_hour=1000,
    ),
)

# JWT Authentication
app.add_middleware(
    AuthenticationMiddleware,
    backend=JWTAuthBackend(
        secret=os.environ["JWT_SECRET"],
        algorithm="HS256",
    ),
)

# Logging (exclude health checks)
app.add_middleware(
    LoggingMiddleware,
    exclude_paths={"/health", "/healthz", "/ready", "/live", "/metrics"},
)

# Request context
app.add_middleware(RequestContextMiddleware)

# Health checks
app.add_middleware(
    HealthCheckMiddleware,
    version=os.environ.get("APP_VERSION", "1.0.0"),
    service_name="my-api",
)

# Metrics
app.add_middleware(MetricsMiddleware)

# Trusted hosts
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=os.environ["ALLOWED_HOSTS"].split(","),
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ["ALLOWED_ORIGINS"].split(","),
    allow_credentials=True,
)
```

---

## 🔧 Custom Middleware

Extend `FastMVCMiddleware` to create your own middleware:

```python
from src import FastMVCMiddleware
from starlette.requests import Request
from starlette.responses import Response

class MyCustomMiddleware(FastMVCMiddleware):
    """
    Custom middleware that adds a custom header.
    
    Example:
        app.add_middleware(MyCustomMiddleware, custom_option="value")
    """
    
    def __init__(
        self,
        app,
        custom_option: str = "default",
        exclude_paths: set[str] | None = None,
        exclude_methods: set[str] | None = None,
    ):
        super().__init__(app, exclude_paths=exclude_paths, exclude_methods=exclude_methods)
        self.custom_option = custom_option
    
    async def dispatch(self, request: Request, call_next):
        # Skip excluded paths
        if self.should_skip(request):
            return await call_next(request)
        
        # Pre-processing
        client_ip = self.get_client_ip(request)
        
        # Process request
        response = await call_next(request)
        
        # Post-processing
        response.headers["X-Custom-Header"] = self.custom_option
        
        return response
```

---

## 🧪 Testing

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_security.py -v
```

### Testing Your Middleware

```python
import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient
from src import SecurityHeadersMiddleware

@pytest.fixture
def app():
    app = FastAPI()
    app.add_middleware(SecurityHeadersMiddleware, enable_hsts=True)
    
    @app.get("/")
    def root():
        return {"message": "Hello"}
    
    return app

@pytest.fixture
def client(app):
    return TestClient(app)

def test_security_headers(client):
    response = client.get("/")
    
    assert response.status_code == 200
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert "Strict-Transport-Security" in response.headers
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

- 📖 [Documentation](https://github.com/hyyre/fastmvc-middleware#readme)
- 🐛 [Issue Tracker](https://github.com/hyyre/fastmvc-middleware/issues)
- 💬 [Discussions](https://github.com/hyyre/fastmvc-middleware/discussions)
- 📧 Email: support@hyyre.dev
