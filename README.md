# FastMVC Middleware

[![PyPI version](https://badge.fury.io/py/fastmvc-middleware.svg)](https://badge.fury.io/py/fastmvc-middleware)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Production-ready middleware collection for FastAPI/Starlette applications.**

A comprehensive set of battle-tested, configurable middleware components for building robust APIs with security, observability, rate limiting, and authentication built-in.

## ✨ Features

- 🔒 **Security Headers** - Comprehensive protection against XSS, clickjacking, and other vulnerabilities
- 🚦 **Rate Limiting** - Sliding window algorithm with configurable limits and storage backends
- 🔑 **Authentication** - Pluggable auth with JWT and API key backends included
- 📝 **Request Logging** - Structured logging with configurable verbosity
- ⏱️ **Timing** - Request processing time tracking
- 🆔 **Request IDs** - Distributed tracing support with unique identifiers
- 🌐 **CORS** - Cross-origin resource sharing with sensible defaults
- 🧵 **Request Context** - Async-safe context variables accessible anywhere

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
from fastmvc_middleware import (
    CORSMiddleware,
    SecurityHeadersMiddleware,
    LoggingMiddleware,
    TimingMiddleware,
    RequestIDMiddleware,
)

app = FastAPI()

# Add middleware (order matters - first added = last executed)
app.add_middleware(TimingMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(SecurityHeadersMiddleware, enable_hsts=True)
app.add_middleware(RequestIDMiddleware)
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

## 📚 Middleware Reference

### SecurityHeadersMiddleware

Adds comprehensive security headers to protect against common web vulnerabilities.

```python
from fastmvc_middleware import SecurityHeadersMiddleware, SecurityHeadersConfig

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
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Content-Security-Policy`
- `Permissions-Policy`
- `Strict-Transport-Security` (when HSTS enabled)
- `Cross-Origin-Opener-Policy`
- `Cross-Origin-Resource-Policy`

---

### RateLimitMiddleware

Protects your API from abuse with configurable rate limiting.

```python
from fastmvc_middleware import RateLimitMiddleware, RateLimitConfig

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
    # Fall back to IP
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"

config = RateLimitConfig(key_func=get_user_key)
app.add_middleware(RateLimitMiddleware, config=config)
```

**Response Headers:**
- `X-RateLimit-Limit`: Maximum requests allowed
- `X-RateLimit-Remaining`: Remaining requests in window
- `X-RateLimit-Reset`: Unix timestamp when limit resets
- `Retry-After`: Seconds until requests are allowed (when limited)

---

### AuthenticationMiddleware

Pluggable authentication with support for JWT tokens and API keys.

```python
from fastmvc_middleware import (
    AuthenticationMiddleware,
    AuthConfig,
    JWTAuthBackend,
    APIKeyAuthBackend,
)

# JWT Authentication
jwt_backend = JWTAuthBackend(
    secret="your-secret-key",
    algorithm="HS256",
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

---

### LoggingMiddleware

Structured request/response logging with configurable verbosity.

```python
from fastmvc_middleware import LoggingMiddleware
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

---

### TimingMiddleware

Adds request processing time to response headers.

```python
from fastmvc_middleware import TimingMiddleware

app.add_middleware(
    TimingMiddleware,
    header_name="X-Process-Time",
    include_unit=True,
    precision=2,
)
```

**Response Header:** `X-Process-Time: 12.34ms`

---

### RequestIDMiddleware

Generates unique request identifiers for distributed tracing.

```python
from fastmvc_middleware import RequestIDMiddleware

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

---

### RequestContextMiddleware

Provides async-safe context variables accessible from anywhere in your code.

```python
from fastmvc_middleware import (
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
- `request_id`: Unique request identifier
- `start_time`: Request start time (datetime)
- `client_ip`: Client IP address
- `method`: HTTP method
- `path`: Request path

---

### CORSMiddleware

Cross-origin resource sharing with sensible defaults.

```python
from fastmvc_middleware import CORSMiddleware

# Specific origins (production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com", "https://app.example.com"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    allow_credentials=True,
    max_age=600,
)

# All origins (development only!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # Required when using "*"
)
```

## 🎯 Best Practices

### Middleware Order

The order in which you add middleware matters. Middleware is executed in **reverse order** of addition (last added = first executed).

**Recommended order:**

```python
# 1. Timing (outermost - measures total time)
app.add_middleware(TimingMiddleware)

# 2. Logging (logs request/response)
app.add_middleware(LoggingMiddleware)

# 3. Security Headers
app.add_middleware(SecurityHeadersMiddleware)

# 4. Rate Limiting (before auth to protect login endpoints)
app.add_middleware(RateLimitMiddleware)

# 5. Authentication
app.add_middleware(AuthenticationMiddleware, backend=backend)

# 6. Request ID/Context (innermost)
app.add_middleware(RequestContextMiddleware)

# 7. CORS (must be last added = first executed)
app.add_middleware(CORSMiddleware, allow_origins=["..."])
```

### Production Configuration

```python
from fastmvc_middleware import (
    SecurityHeadersMiddleware,
    RateLimitMiddleware,
    RateLimitConfig,
    AuthenticationMiddleware,
    JWTAuthBackend,
    LoggingMiddleware,
    RequestContextMiddleware,
    CORSMiddleware,
)

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
    exclude_paths={"/health", "/healthz", "/metrics"},
)

# Request context
app.add_middleware(RequestContextMiddleware)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ["ALLOWED_ORIGINS"].split(","),
    allow_credentials=True,
)
```

## 🔧 Custom Middleware

Extend `FastMVCMiddleware` to create your own middleware:

```python
from fastmvc_middleware import FastMVCMiddleware
from starlette.requests import Request
from starlette.responses import Response

class MyCustomMiddleware(FastMVCMiddleware):
    def __init__(self, app, custom_option: str = "default"):
        super().__init__(app)
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

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

- 📖 [Documentation](https://github.com/hyyre/fastmvc-middleware#readme)
- 🐛 [Issue Tracker](https://github.com/hyyre/fastmvc-middleware/issues)
- 💬 [Discussions](https://github.com/hyyre/fastmvc-middleware/discussions)
