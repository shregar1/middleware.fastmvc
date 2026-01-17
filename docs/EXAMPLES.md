# FastMVC Middleware Examples

This document provides practical examples for common use cases.

## Table of Contents

- [Basic Setup](#basic-setup)
- [Security Configuration](#security-configuration)
- [Rate Limiting](#rate-limiting)
- [Authentication](#authentication)
- [Caching](#caching)
- [Health Checks](#health-checks)
- [Metrics & Monitoring](#metrics--monitoring)
- [Maintenance Mode](#maintenance-mode)
- [Production Configuration](#production-configuration)
- [Custom Middleware](#custom-middleware)

---

## Basic Setup

### Minimal Configuration

```python
from fastapi import FastAPI
from fastMiddleware import (
    CORSMiddleware,
    SecurityHeadersMiddleware,
    TimingMiddleware,
    RequestIDMiddleware,
)

app = FastAPI()

# Add middleware (order matters)
app.add_middleware(TimingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=["*"])

@app.get("/")
async def root():
    return {"message": "Hello, World!"}
```

### With Logging

```python
import logging
from fastMiddleware import LoggingMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app.add_middleware(
    LoggingMiddleware,
    log_level=logging.INFO,
    exclude_paths={"/health", "/metrics"},
)
```

---

## Security Configuration

### Strict Security Headers

```python
from fastMiddleware import SecurityHeadersMiddleware, SecurityHeadersConfig

config = SecurityHeadersConfig(
    enable_hsts=True,
    hsts_max_age=31536000,
    hsts_preload=True,
    hsts_include_subdomains=True,
    content_security_policy="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:;",
    x_frame_options="DENY",
    referrer_policy="strict-origin-when-cross-origin",
    permissions_policy="geolocation=(), microphone=(), camera=()",
)

app.add_middleware(SecurityHeadersMiddleware, config=config)
```

### Trusted Hosts (Production)

```python
from fastMiddleware import TrustedHostMiddleware

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "api.example.com",
        "*.example.com",  # Allow all subdomains
    ],
)
```

### CORS for API

```python
from fastMiddleware import CORSMiddleware

# Production CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://app.example.com",
        "https://admin.example.com",
    ],
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
    allow_credentials=True,
    expose_headers=["X-Request-ID", "X-RateLimit-Remaining"],
    max_age=3600,
)
```

---

## Rate Limiting

### Basic Rate Limiting

```python
from fastMiddleware import RateLimitMiddleware, RateLimitConfig

config = RateLimitConfig(
    requests_per_minute=60,
    requests_per_hour=1000,
)

app.add_middleware(RateLimitMiddleware, config=config)
```

### Per-User Rate Limiting

```python
from starlette.requests import Request

def get_user_key(request: Request) -> str:
    """Extract rate limit key from request."""
    # Try to get user ID from auth
    if hasattr(request.state, "auth"):
        return f"user:{request.state.auth.get('user_id', 'unknown')}"
    
    # Try API key
    api_key = request.headers.get("X-API-Key")
    if api_key:
        return f"api:{api_key[:8]}"
    
    # Fall back to IP
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return f"ip:{forwarded.split(',')[0].strip()}"
    
    return f"ip:{request.client.host if request.client else 'unknown'}"

config = RateLimitConfig(
    requests_per_minute=100,
    key_func=get_user_key,
)

app.add_middleware(RateLimitMiddleware, config=config)
```

### Tiered Rate Limits

```python
from starlette.requests import Request

# Define tiers
RATE_LIMITS = {
    "free": 60,
    "pro": 300,
    "enterprise": 1000,
}

def tiered_rate_limit(request: Request) -> str:
    tier = "free"
    if hasattr(request.state, "auth"):
        tier = request.state.auth.get("tier", "free")
    
    # Include tier in key for separate buckets
    user_id = getattr(request.state, "auth", {}).get("user_id", "anon")
    return f"{tier}:{user_id}"

# Create multiple middleware instances or use dynamic limits
config = RateLimitConfig(
    requests_per_minute=60,  # Default
    key_func=tiered_rate_limit,
)
```

---

## Authentication

### JWT Authentication

```python
from fastMiddleware import (
    AuthenticationMiddleware,
    AuthConfig,
    JWTAuthBackend,
)
import os

jwt_backend = JWTAuthBackend(
    secret=os.environ["JWT_SECRET"],
    algorithm="HS256",
    verify_exp=True,
)

auth_config = AuthConfig(
    exclude_paths={
        "/",
        "/health",
        "/ready",
        "/live",
        "/docs",
        "/openapi.json",
        "/login",
        "/register",
        "/forgot-password",
    },
    exclude_methods={"OPTIONS"},
)

app.add_middleware(
    AuthenticationMiddleware,
    backend=jwt_backend,
    config=auth_config,
)

# Access authenticated user
@app.get("/me")
async def get_current_user(request: Request):
    return {"user": request.state.auth}
```

### API Key Authentication

```python
from fastMiddleware import APIKeyAuthBackend

# Static API keys
backend = APIKeyAuthBackend(
    valid_keys={
        "sk_live_abc123",
        "sk_live_def456",
    }
)

# Or with dynamic validation
async def validate_api_key(key: str) -> dict | None:
    """Validate API key against database."""
    from your_app.db import get_api_key_info
    
    key_info = await get_api_key_info(key)
    if key_info and key_info.is_active:
        return {
            "user_id": key_info.user_id,
            "tier": key_info.tier,
            "scopes": key_info.scopes,
        }
    return None

backend = APIKeyAuthBackend(validator=validate_api_key)
```

---

## Caching

### Basic Caching

```python
from fastMiddleware import CacheMiddleware, CacheConfig

config = CacheConfig(
    default_max_age=300,  # 5 minutes
    enable_etag=True,
)

app.add_middleware(CacheMiddleware, config=config)
```

### Path-Specific Cache Rules

```python
config = CacheConfig(
    default_max_age=60,
    path_rules={
        # Static assets: long cache
        "/static": {"max_age": 86400, "public": True},
        "/assets": {"max_age": 31536000, "public": True, "immutable": True},
        
        # API data: short cache
        "/api/public": {"max_age": 300, "public": True},
        
        # User data: no cache
        "/api/user": {"no_store": True, "private": True},
        
        # Admin: no cache
        "/admin": {"no_store": True, "no_cache": True},
    },
)
```

### Conditional Request Handling

The cache middleware automatically handles conditional requests:

```bash
# First request
curl -i https://api.example.com/data
# Returns: ETag: "abc123"

# Subsequent request
curl -i -H "If-None-Match: \"abc123\"" https://api.example.com/data
# Returns: 304 Not Modified (if unchanged)
```

---

## Health Checks

### Basic Health Check

```python
from fastMiddleware import HealthCheckMiddleware, HealthConfig

config = HealthConfig(
    version="1.0.0",
    service_name="my-api",
)

app.add_middleware(HealthCheckMiddleware, config=config)
```

### With Dependency Checks

```python
from your_app.db import database
from your_app.cache import redis

async def check_database() -> bool:
    """Check database connection."""
    try:
        await database.execute("SELECT 1")
        return True
    except Exception:
        return False

async def check_redis() -> bool:
    """Check Redis connection."""
    try:
        await redis.ping()
        return True
    except Exception:
        return False

async def check_external_api() -> bool:
    """Check external API availability."""
    import httpx
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.example.com/health",
                timeout=5.0
            )
            return response.status_code == 200
    except Exception:
        return False

config = HealthConfig(
    version=os.environ.get("APP_VERSION", "0.0.0"),
    service_name="my-api",
    custom_checks={
        "database": check_database,
        "redis": check_redis,
        "external_api": check_external_api,
    },
)
```

### Kubernetes Probes

```yaml
# kubernetes/deployment.yaml
spec:
  containers:
    - name: my-api
      livenessProbe:
        httpGet:
          path: /live
          port: 8000
        initialDelaySeconds: 10
        periodSeconds: 10
        failureThreshold: 3
      
      readinessProbe:
        httpGet:
          path: /ready
          port: 8000
        initialDelaySeconds: 5
        periodSeconds: 5
        failureThreshold: 3
      
      startupProbe:
        httpGet:
          path: /health
          port: 8000
        initialDelaySeconds: 0
        periodSeconds: 5
        failureThreshold: 30
```

---

## Metrics & Monitoring

### Basic Metrics

```python
from fastMiddleware import MetricsMiddleware

app.add_middleware(MetricsMiddleware)
```

### Custom Path Normalization

```python
from fastMiddleware import MetricsMiddleware, MetricsConfig

config = MetricsConfig(
    metrics_path="/prometheus",
    path_patterns={
        r"/users/\d+": "/users/{id}",
        r"/orders/[a-f0-9-]+": "/orders/{uuid}",
        r"/products/\w+": "/products/{slug}",
    },
)

app.add_middleware(MetricsMiddleware, config=config)
```

### Prometheus Setup

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'my-api'
    static_configs:
      - targets: ['my-api:8000']
    metrics_path: /metrics
    scrape_interval: 15s
```

### Grafana Dashboard Query Examples

```promql
# Request rate
rate(fastmvc_http_requests_total[5m])

# Error rate
rate(fastmvc_http_requests_total{status=~"5.."}[5m])
  / rate(fastmvc_http_requests_total[5m])

# Latency (95th percentile)
histogram_quantile(0.95, 
  rate(fastmvc_http_request_duration_seconds_bucket[5m])
)

# Current in-flight requests
fastmvc_http_in_flight_requests

# Uptime
fastmvc_uptime_seconds
```

---

## Maintenance Mode

### Basic Maintenance

```python
from fastMiddleware import MaintenanceMiddleware, MaintenanceConfig

config = MaintenanceConfig(
    enabled=False,  # Toggle to enable
    message="We're upgrading our systems. Please try again in a few minutes.",
    retry_after=1800,  # 30 minutes
    allowed_paths={"/health", "/metrics"},
)

middleware = MaintenanceMiddleware(app, config=config)
```

### Dynamic Toggle

```python
from fastapi import FastAPI
from fastMiddleware import MaintenanceMiddleware, MaintenanceConfig

app = FastAPI()
config = MaintenanceConfig(enabled=False)
maintenance = MaintenanceMiddleware(app, config=config)

# Admin endpoints to control maintenance
@app.post("/admin/maintenance/enable")
async def enable_maintenance(
    message: str = "Service temporarily unavailable",
    retry_after: int = 300,
):
    maintenance.enable(message=message, retry_after=retry_after)
    return {"status": "enabled"}

@app.post("/admin/maintenance/disable")
async def disable_maintenance():
    maintenance.disable()
    return {"status": "disabled"}

@app.get("/admin/maintenance/status")
async def maintenance_status():
    return {
        "enabled": maintenance.is_enabled(),
        "message": maintenance.config.message,
        "retry_after": maintenance.config.retry_after,
    }
```

### Admin Bypass

```python
config = MaintenanceConfig(
    enabled=True,
    message="Scheduled maintenance in progress",
    bypass_token="super-secret-admin-token",
    allowed_ips={"10.0.0.1", "192.168.1.1"},
)

# Admin can bypass with header:
# curl -H "X-Maintenance-Bypass: super-secret-admin-token" https://api.example.com/
```

### Custom HTML Page

```python
MAINTENANCE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Maintenance</title>
    <style>
        body { font-family: system-ui; text-align: center; padding: 50px; }
        h1 { color: #333; }
        p { color: #666; }
    </style>
</head>
<body>
    <h1>🔧 Under Maintenance</h1>
    <p>{message}</p>
    <p>We'll be back in approximately {retry_minutes} minutes.</p>
</body>
</html>
"""

config = MaintenanceConfig(
    enabled=True,
    use_html=True,
    html_template=MAINTENANCE_HTML,
    message="Upgrading database",
    retry_after=900,
)
```

---

## Production Configuration

### Full Production Setup

```python
import os
import logging
from fastapi import FastAPI
from fastMiddleware import (
    # Security
    CORSMiddleware,
    SecurityHeadersMiddleware,
    TrustedHostMiddleware,
    AuthenticationMiddleware,
    JWTAuthBackend,
    AuthConfig,
    
    # Observability
    LoggingMiddleware,
    TimingMiddleware,
    RequestIDMiddleware,
    RequestContextMiddleware,
    MetricsMiddleware,
    
    # Resilience
    RateLimitMiddleware,
    RateLimitConfig,
    ErrorHandlerMiddleware,
    IdempotencyMiddleware,
    
    # Performance
    CompressionMiddleware,
    CacheMiddleware,
    CacheConfig,
    
    # Operations
    HealthCheckMiddleware,
    HealthConfig,
    MaintenanceMiddleware,
    MaintenanceConfig,
)

# Configuration from environment
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "").split(",")
JWT_SECRET = os.environ["JWT_SECRET"]
APP_VERSION = os.environ.get("APP_VERSION", "0.0.0")

app = FastAPI(
    title="My API",
    version=APP_VERSION,
    debug=DEBUG,
)

# 1. Compression (outermost)
app.add_middleware(CompressionMiddleware, minimum_size=1000)

# 2. Timing
app.add_middleware(TimingMiddleware)

# 3. Logging
app.add_middleware(
    LoggingMiddleware,
    exclude_paths={"/health", "/ready", "/live", "/metrics"},
)

# 4. Error handling
app.add_middleware(
    ErrorHandlerMiddleware,
    include_traceback=DEBUG,
    log_exceptions=True,
)

# 5. Metrics
app.add_middleware(MetricsMiddleware)

# 6. Security headers
app.add_middleware(
    SecurityHeadersMiddleware,
    enable_hsts=not DEBUG,
    content_security_policy="default-src 'self'" if not DEBUG else None,
)

# 7. Cache
cache_config = CacheConfig(
    default_max_age=60,
    enable_etag=True,
    path_rules={
        "/api/public": {"max_age": 300, "public": True},
        "/api/user": {"no_store": True},
    },
)
app.add_middleware(CacheMiddleware, config=cache_config)

# 8. Rate limiting
rate_config = RateLimitConfig(
    requests_per_minute=100 if not DEBUG else 1000,
    requests_per_hour=5000,
)
app.add_middleware(RateLimitMiddleware, config=rate_config)

# 9. Idempotency
app.add_middleware(IdempotencyMiddleware)

# 10. Authentication
jwt_backend = JWTAuthBackend(secret=JWT_SECRET)
auth_config = AuthConfig(
    exclude_paths={
        "/", "/health", "/ready", "/live", "/metrics",
        "/docs", "/openapi.json", "/login", "/register",
    },
)
app.add_middleware(
    AuthenticationMiddleware,
    backend=jwt_backend,
    config=auth_config,
)

# 11. Request ID
app.add_middleware(RequestIDMiddleware)

# 12. Request context
app.add_middleware(RequestContextMiddleware)

# 13. Health checks
health_config = HealthConfig(
    version=APP_VERSION,
    service_name="my-api",
)
app.add_middleware(HealthCheckMiddleware, config=health_config)

# 14. Maintenance mode
maintenance_config = MaintenanceConfig(
    enabled=False,
    allowed_paths={"/health", "/ready", "/live", "/metrics"},
)
app.add_middleware(MaintenanceMiddleware, config=maintenance_config)

# 15. Trusted hosts
if ALLOWED_HOSTS and ALLOWED_HOSTS[0]:
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=ALLOWED_HOSTS)

# 16. CORS (last added = first executed)
if ALLOWED_ORIGINS and ALLOWED_ORIGINS[0]:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
```

---

## Custom Middleware

### Tenant Isolation

```python
from fastMiddleware import FastMVCMiddleware
from starlette.requests import Request
from starlette.responses import Response

class TenantMiddleware(FastMVCMiddleware):
    """Multi-tenant isolation middleware."""
    
    async def dispatch(self, request: Request, call_next) -> Response:
        if self.should_skip(request):
            return await call_next(request)
        
        # Extract tenant from subdomain or header
        host = request.headers.get("Host", "")
        tenant_id = host.split(".")[0] if "." in host else None
        
        # Or from header
        if not tenant_id:
            tenant_id = request.headers.get("X-Tenant-ID")
        
        if not tenant_id:
            return Response("Tenant not found", status_code=400)
        
        # Set tenant in state
        request.state.tenant_id = tenant_id
        
        response = await call_next(request)
        response.headers["X-Tenant-ID"] = tenant_id
        
        return response

app.add_middleware(TenantMiddleware)
```

### Request Validation

```python
class RequestValidationMiddleware(FastMVCMiddleware):
    """Validate incoming requests."""
    
    def __init__(self, app, max_body_size: int = 10_000_000):
        super().__init__(app)
        self.max_body_size = max_body_size
    
    async def dispatch(self, request: Request, call_next) -> Response:
        if self.should_skip(request):
            return await call_next(request)
        
        # Check content length
        content_length = request.headers.get("Content-Length")
        if content_length:
            if int(content_length) > self.max_body_size:
                return Response(
                    "Request too large",
                    status_code=413,
                )
        
        # Validate content type for POST/PUT
        if request.method in ("POST", "PUT", "PATCH"):
            content_type = request.headers.get("Content-Type", "")
            if not content_type.startswith(("application/json", "multipart/form-data")):
                return Response(
                    "Unsupported content type",
                    status_code=415,
                )
        
        return await call_next(request)
```

### IP Blocking

```python
class IPBlockMiddleware(FastMVCMiddleware):
    """Block requests from specific IPs."""
    
    def __init__(self, app, blocked_ips: set[str] = None):
        super().__init__(app)
        self.blocked_ips = blocked_ips or set()
    
    def add_ip(self, ip: str):
        self.blocked_ips.add(ip)
    
    def remove_ip(self, ip: str):
        self.blocked_ips.discard(ip)
    
    async def dispatch(self, request: Request, call_next) -> Response:
        client_ip = self.get_client_ip(request)
        
        if client_ip in self.blocked_ips:
            return Response(
                "Access denied",
                status_code=403,
            )
        
        return await call_next(request)

# Usage
ip_blocker = IPBlockMiddleware(app)

@app.post("/admin/block-ip")
async def block_ip(ip: str):
    ip_blocker.add_ip(ip)
    return {"blocked": ip}
```

### Request Tracing (OpenTelemetry Style)

```python
import uuid
from contextvars import ContextVar

trace_id_var: ContextVar[str] = ContextVar("trace_id")
span_id_var: ContextVar[str] = ContextVar("span_id")

class TracingMiddleware(FastMVCMiddleware):
    """Distributed tracing middleware."""
    
    async def dispatch(self, request: Request, call_next) -> Response:
        # Extract or generate trace ID
        trace_id = request.headers.get("X-Trace-ID", str(uuid.uuid4()))
        parent_span_id = request.headers.get("X-Span-ID")
        span_id = str(uuid.uuid4())[:16]
        
        # Set context
        trace_id_var.set(trace_id)
        span_id_var.set(span_id)
        
        # Store in request state
        request.state.trace_id = trace_id
        request.state.span_id = span_id
        request.state.parent_span_id = parent_span_id
        
        response = await call_next(request)
        
        # Add to response headers
        response.headers["X-Trace-ID"] = trace_id
        response.headers["X-Span-ID"] = span_id
        
        return response

def get_trace_id() -> str | None:
    return trace_id_var.get(None)

def get_span_id() -> str | None:
    return span_id_var.get(None)
```

