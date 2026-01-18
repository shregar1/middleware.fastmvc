# FastMVC Middleware Examples

Comprehensive examples for common use cases.

## Table of Contents

1. [Production API Setup](#production-api-setup)
2. [Microservices Configuration](#microservices-configuration)
3. [Multi-Tenant SaaS Application](#multi-tenant-saas-application)
4. [High-Traffic API](#high-traffic-api)
5. [Secure Financial API](#secure-financial-api)
6. [API Gateway](#api-gateway)
7. [A/B Testing Platform](#ab-testing-platform)
8. [Monitoring Stack](#monitoring-stack)

---

## Production API Setup

A complete production-ready API configuration.

```python
from fastapi import FastAPI
from fastMiddleware import (
    CORSMiddleware,
    SecurityHeadersMiddleware,
    RateLimitMiddleware,
    LoggingMiddleware,
    TimingMiddleware,
    RequestIDMiddleware,
    HealthCheckMiddleware,
    CompressionMiddleware,
    ErrorHandlerMiddleware,
    AuthenticationMiddleware,
    JWTAuthBackend,
)

app = FastAPI(title="Production API")

# Order matters! First added = last executed

# 1. Compress responses
app.add_middleware(CompressionMiddleware, minimum_size=1000)

# 2. Add timing header
app.add_middleware(TimingMiddleware)

# 3. Log all requests
app.add_middleware(
    LoggingMiddleware,
    exclude_paths={"/health", "/metrics"},
)

# 4. Handle errors gracefully
app.add_middleware(
    ErrorHandlerMiddleware,
    include_traceback=False,
)

# 5. Authenticate requests
app.add_middleware(
    AuthenticationMiddleware,
    backend=JWTAuthBackend(
        secret_key="your-jwt-secret",
        algorithm="HS256",
    ),
    exclude_paths={"/health", "/login", "/register"},
)

# 6. Rate limit
app.add_middleware(
    RateLimitMiddleware,
    requests_per_minute=100,
)

# 7. Security headers
app.add_middleware(
    SecurityHeadersMiddleware,
    enable_hsts=True,
    content_security_policy="default-src 'self'",
)

# 8. Request ID for tracing
app.add_middleware(RequestIDMiddleware)

# 9. Health endpoints
app.add_middleware(
    HealthCheckMiddleware,
    version="1.0.0",
)

# 10. CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}
```

---

## Microservices Configuration

Configuration for a microservice with distributed tracing.

```python
from fastapi import FastAPI
from fastMiddleware import (
    RequestIDPropagationMiddleware,
    CorrelationMiddleware,
    ServerTimingMiddleware,
    CircuitBreakerMiddleware,
    TimeoutMiddleware,
    GracefulShutdownMiddleware,
    HealthCheckMiddleware,
    MetricsMiddleware,
    LoggingMiddleware,
    get_correlation_id,
    get_request_ids,
    timing,
)
import httpx

app = FastAPI(title="User Service")

# Graceful shutdown
shutdown_mw = GracefulShutdownMiddleware(app, timeout=30.0)

# Middleware stack
app.add_middleware(ServerTimingMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    TimeoutMiddleware,
    timeout=10.0,
    path_timeouts={"/api/slow": 60.0},
)
app.add_middleware(
    CircuitBreakerMiddleware,
    failure_threshold=5,
    recovery_timeout=30,
)
app.add_middleware(RequestIDPropagationMiddleware)
app.add_middleware(CorrelationMiddleware)
app.add_middleware(
    HealthCheckMiddleware,
    version="2.1.0",
)
app.add_middleware(MetricsMiddleware, endpoint="/metrics")

@app.get("/api/users/{user_id}")
async def get_user(user_id: int):
    correlation_id = get_correlation_id()
    
    with timing("database", "User lookup"):
        user = await db.get_user(user_id)
    
    with timing("orders_service", "Fetch orders"):
        async with httpx.AsyncClient() as client:
            orders = await client.get(
                f"http://orders-service/api/users/{user_id}/orders",
                headers={"X-Correlation-ID": correlation_id},
            )
    
    return {"user": user, "orders": orders.json()}

@app.on_event("shutdown")
async def on_shutdown():
    await shutdown_mw.shutdown()
```

---

## Multi-Tenant SaaS Application

SaaS application with tenant isolation.

```python
from fastapi import FastAPI, Request
from fastMiddleware import (
    TenantMiddleware,
    SessionMiddleware,
    RateLimitMiddleware,
    QuotaMiddleware,
    AuditMiddleware,
    FeatureFlagMiddleware,
    get_tenant_id,
    is_feature_enabled,
)

app = FastAPI(title="SaaS Platform")

# Tenant-aware rate limiting
app.add_middleware(
    RateLimitMiddleware,
    key_func=lambda req: f"{get_tenant_id()}:{req.client.host}",
    requests_per_minute=100,
)

# Usage quotas per tenant
app.add_middleware(
    QuotaMiddleware,
    quotas={
        "free": {"requests_per_day": 1000},
        "pro": {"requests_per_day": 100000},
        "enterprise": {"requests_per_day": -1},  # Unlimited
    },
)

# Audit logging for compliance
app.add_middleware(
    AuditMiddleware,
    log_request_body=True,
    sensitive_headers={"Authorization", "Cookie"},
)

# Feature flags per tenant
app.add_middleware(
    FeatureFlagMiddleware,
    flags={
        "new_dashboard": True,
        "advanced_analytics": False,
    },
)

# Session management
app.add_middleware(
    SessionMiddleware,
    secret_key="session-secret",
)

# Tenant identification (subdomain-based)
app.add_middleware(
    TenantMiddleware,
    use_subdomain=True,
)

@app.get("/api/dashboard")
async def dashboard(request: Request):
    tenant_id = get_tenant_id()
    
    if is_feature_enabled("new_dashboard"):
        return await new_dashboard(tenant_id)
    return await old_dashboard(tenant_id)

@app.get("/api/data")
async def get_data():
    tenant_id = get_tenant_id()
    # All queries automatically scoped to tenant
    return await db.query(
        "SELECT * FROM data WHERE tenant_id = ?",
        [tenant_id],
    )
```

---

## High-Traffic API

Configuration for handling high traffic with protection.

```python
from fastapi import FastAPI
from fastMiddleware import (
    RateLimitMiddleware,
    BulkheadMiddleware,
    LoadSheddingMiddleware,
    CircuitBreakerMiddleware,
    ResponseCacheMiddleware,
    RequestDedupMiddleware,
    RequestCoalescingMiddleware,
    CompressionMiddleware,
    TimeoutMiddleware,
)

app = FastAPI(title="High-Traffic API")

# Response caching
cache_mw = ResponseCacheMiddleware(
    app,
    default_ttl=60,
    max_size=10000,
    path_ttls={
        "/api/static": 3600,    # 1 hour
        "/api/trending": 30,     # 30 seconds
    },
)

# Compress large responses
app.add_middleware(CompressionMiddleware, minimum_size=500)

# Coalesce identical concurrent requests
app.add_middleware(
    RequestCoalescingMiddleware,
    window=0.05,  # 50ms
)

# Deduplicate requests
app.add_middleware(
    RequestDedupMiddleware,
    window=0.1,  # 100ms
)

# Request timeout
app.add_middleware(
    TimeoutMiddleware,
    timeout=5.0,
)

# Circuit breaker for downstream services
app.add_middleware(
    CircuitBreakerMiddleware,
    failure_threshold=10,
    recovery_timeout=60,
)

# Load shedding under pressure
app.add_middleware(
    LoadSheddingMiddleware,
    max_concurrent=5000,
    shed_probability=0.5,
)

# Bulkhead for isolation
app.add_middleware(
    BulkheadMiddleware,
    max_concurrent=1000,
    max_waiting=500,
)

# Rate limiting
app.add_middleware(
    RateLimitMiddleware,
    requests_per_minute=1000,
    burst_size=100,
)

@app.get("/api/popular")
async def get_popular():
    # This response will be cached
    return await fetch_popular_items()

# Cache invalidation
@app.post("/api/invalidate")
async def invalidate():
    cache_mw.invalidate("/api/popular")
    return {"invalidated": True}
```

---

## Secure Financial API

Security-focused configuration for financial applications.

```python
from fastapi import FastAPI
from fastMiddleware import (
    SecurityHeadersMiddleware,
    HTTPSRedirectMiddleware,
    CSRFMiddleware,
    IPFilterMiddleware,
    ReplayPreventionMiddleware,
    RequestSigningMiddleware,
    IdempotencyMiddleware,
    AuditMiddleware,
    DataMaskingMiddleware,
    RateLimitMiddleware,
    MaskingRule,
)

app = FastAPI(title="Financial API")

# Mask sensitive data in logs
app.add_middleware(
    DataMaskingMiddleware,
    rules=[
        MaskingRule(field="card_number", mask="****-****-****-{last4}"),
        MaskingRule(field="ssn", mask="XXX-XX-{last4}"),
        MaskingRule(field="password", mask="***"),
        MaskingRule(field="pin", mask="****"),
    ],
)

# Comprehensive audit logging
app.add_middleware(
    AuditMiddleware,
    log_request_body=True,
    log_response_body=True,
)

# Idempotency for payment requests
app.add_middleware(
    IdempotencyMiddleware,
    header_name="Idempotency-Key",
    ttl=86400,  # 24 hours
)

# Rate limiting
app.add_middleware(
    RateLimitMiddleware,
    requests_per_minute=60,
)

# Replay attack prevention
app.add_middleware(
    ReplayPreventionMiddleware,
    max_age=300,  # 5 minutes
)

# Request signature validation
app.add_middleware(
    RequestSigningMiddleware,
    secret_key="hmac-secret-key",
    algorithm="sha256",
    exclude_paths={"/health"},
)

# CSRF protection
app.add_middleware(
    CSRFMiddleware,
    secret_key="csrf-secret",
    exclude_paths={"/api/webhooks"},
)

# IP whitelist for admin
app.add_middleware(
    IPFilterMiddleware,
    whitelist={"10.0.0.0/8"},  # Internal network only
    exclude_paths={"/api/public"},
)

# Force HTTPS
app.add_middleware(HTTPSRedirectMiddleware)

# Security headers
app.add_middleware(
    SecurityHeadersMiddleware,
    enable_hsts=True,
    hsts_preload=True,
    content_security_policy="default-src 'none'; frame-ancestors 'none'",
)

@app.post("/api/transfer")
async def transfer(request: Request):
    # Idempotency key ensures no duplicate transfers
    # Signature validates request integrity
    # Audit log captures everything
    return await process_transfer(request)
```

---

## API Gateway

API gateway configuration with routing and proxying.

```python
from fastapi import FastAPI
from fastMiddleware import (
    ProxyMiddleware,
    ProxyRoute,
    RateLimitMiddleware,
    AuthenticationMiddleware,
    APIKeyAuthBackend,
    VersioningMiddleware,
    VersionLocation,
    PathRewriteMiddleware,
    RewriteRule,
    RedirectMiddleware,
    RedirectRule,
    CORSMiddleware,
    RequestIDMiddleware,
    LoggingMiddleware,
)

app = FastAPI(title="API Gateway")

# Logging
app.add_middleware(LoggingMiddleware)

# Request ID propagation
app.add_middleware(RequestIDMiddleware)

# API versioning
app.add_middleware(
    VersioningMiddleware,
    location=VersionLocation.HEADER,
    default_version="1.0",
)

# Rate limiting
app.add_middleware(
    RateLimitMiddleware,
    key_func=lambda req: req.headers.get("X-API-Key", req.client.host),
    requests_per_minute=1000,
)

# API key authentication
app.add_middleware(
    AuthenticationMiddleware,
    backend=APIKeyAuthBackend(
        api_keys={
            "key-123": {"client": "mobile-app", "tier": "premium"},
            "key-456": {"client": "web-app", "tier": "free"},
        },
    ),
    exclude_paths={"/health", "/docs"},
)

# Redirects
app.add_middleware(
    RedirectMiddleware,
    rules=[
        RedirectRule("/old-api/*", "/api/v1/{path}", permanent=True),
    ],
)

# Path rewriting
app.add_middleware(
    PathRewriteMiddleware,
    rules=[
        RewriteRule("/api/users", "/user-service/api/users"),
        RewriteRule("/api/orders", "/order-service/api/orders"),
    ],
)

# Proxy to backend services
app.add_middleware(
    ProxyMiddleware,
    routes=[
        ProxyRoute(
            path_prefix="/user-service",
            target="http://user-service:8000",
            strip_prefix=True,
        ),
        ProxyRoute(
            path_prefix="/order-service",
            target="http://order-service:8000",
            strip_prefix=True,
        ),
        ProxyRoute(
            path_prefix="/payment-service",
            target="http://payment-service:8000",
            strip_prefix=True,
            add_headers={"X-Gateway": "true"},
        ),
    ],
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## A/B Testing Platform

A/B testing and feature flag configuration.

```python
from fastapi import FastAPI
from fastMiddleware import (
    ABTestMiddleware,
    Experiment,
    FeatureFlagMiddleware,
    UserAgentMiddleware,
    RequestSamplerMiddleware,
    get_variant,
    is_feature_enabled,
    get_user_agent,
    is_sampled,
)

app = FastAPI(title="A/B Testing Platform")

# Request sampling for analytics
app.add_middleware(
    RequestSamplerMiddleware,
    rate=0.1,  # 10% sampling
)

# User agent detection
app.add_middleware(UserAgentMiddleware)

# Feature flags
app.add_middleware(
    FeatureFlagMiddleware,
    flags={
        "new_checkout": True,
        "dark_mode": False,
        "beta_features": False,
    },
)

# A/B experiments
app.add_middleware(
    ABTestMiddleware,
    experiments=[
        Experiment(
            name="checkout_flow",
            variants=["control", "simplified", "express"],
            weights=[0.34, 0.33, 0.33],
        ),
        Experiment(
            name="pricing_display",
            variants=["monthly", "yearly", "both"],
            weights=[0.4, 0.4, 0.2],
        ),
        Experiment(
            name="cta_button",
            variants=["blue", "green", "orange"],
            weights=[0.33, 0.33, 0.34],
        ),
    ],
)

@app.get("/checkout")
async def checkout():
    variant = get_variant("checkout_flow")
    ua = get_user_agent()
    
    # Mobile gets simplified by default
    if ua["is_mobile"] and variant == "control":
        variant = "simplified"
    
    if variant == "simplified":
        return simplified_checkout()
    elif variant == "express":
        return express_checkout()
    return standard_checkout()

@app.get("/pricing")
async def pricing():
    if is_feature_enabled("new_checkout"):
        pricing_variant = get_variant("pricing_display")
        return render_pricing(pricing_variant)
    return legacy_pricing()

@app.post("/track")
async def track_event(event: dict):
    if is_sampled():
        # Full tracking for sampled requests
        await analytics.track_full(event, get_variant("checkout_flow"))
    else:
        # Minimal tracking
        await analytics.track_minimal(event)
    return {"tracked": True}
```

---

## Monitoring Stack

Complete monitoring and observability setup.

```python
from fastapi import FastAPI
from fastMiddleware import (
    MetricsMiddleware,
    LoggingMiddleware,
    RequestLoggerMiddleware,
    ServerTimingMiddleware,
    ResponseTimeMiddleware,
    ResponseTimeSLA,
    ProfilingMiddleware,
    HealthCheckMiddleware,
    RequestIDMiddleware,
    CorrelationMiddleware,
    CostTrackingMiddleware,
    timing,
    add_cost,
)

app = FastAPI(title="Monitored API")

# Health endpoints
app.add_middleware(
    HealthCheckMiddleware,
    health_path="/health",
    ready_path="/ready",
    live_path="/live",
    version="3.0.0",
)

# Prometheus metrics
app.add_middleware(
    MetricsMiddleware,
    endpoint="/metrics",
    include_path_labels=True,
)

# Server-Timing for browser devtools
app.add_middleware(ServerTimingMiddleware)

# Response time SLA monitoring
app.add_middleware(
    ResponseTimeMiddleware,
    slas=[
        ResponseTimeSLA("/api/health", target_ms=10, warning_ms=50, critical_ms=100),
        ResponseTimeSLA("/api/users", target_ms=100, warning_ms=500, critical_ms=1000),
        ResponseTimeSLA("/api/search", target_ms=200, warning_ms=1000, critical_ms=2000),
    ],
)

# Cost tracking
app.add_middleware(
    CostTrackingMiddleware,
    path_costs={
        "/api/ai": 10.0,
        "/api/search": 2.0,
    },
    default_cost=1.0,
)

# Profiling (enable selectively)
app.add_middleware(
    ProfilingMiddleware,
    enabled=True,
    threshold_ms=100,  # Only profile slow requests
)

# Structured logging
app.add_middleware(
    RequestLoggerMiddleware,
    format="json",
)

# Correlation and request IDs
app.add_middleware(CorrelationMiddleware)
app.add_middleware(RequestIDMiddleware)

@app.get("/api/complex")
async def complex_operation():
    with timing("database", "Primary query"):
        data = await db.query(...)
        add_cost(0.5)
    
    with timing("cache", "Cache lookup"):
        cached = await cache.get(...)
    
    with timing("external_api", "Third-party call"):
        external = await call_external_api(...)
        add_cost(5.0)  # External API cost
    
    with timing("processing", "Data processing"):
        result = process(data, cached, external)
    
    return result
```

---

## Custom Middleware

Creating your own middleware.

```python
from fastMiddleware import FastMVCMiddleware
from starlette.requests import Request
from starlette.responses import Response
from typing import Callable, Awaitable

class CustomMiddleware(FastMVCMiddleware):
    """Custom middleware example."""
    
    def __init__(
        self,
        app,
        custom_option: str = "default",
        exclude_paths=None,
    ):
        super().__init__(app, exclude_paths=exclude_paths)
        self.custom_option = custom_option
    
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        # Skip if path excluded
        if self.should_skip(request):
            return await call_next(request)
        
        # Pre-processing
        request.state.custom_data = self.custom_option
        
        # Call next middleware/route
        response = await call_next(request)
        
        # Post-processing
        response.headers["X-Custom-Header"] = self.custom_option
        
        return response

# Use your custom middleware
app.add_middleware(
    CustomMiddleware,
    custom_option="my-value",
    exclude_paths={"/health"},
)
```
