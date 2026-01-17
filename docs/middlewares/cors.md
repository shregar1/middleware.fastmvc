# CORSMiddleware

Cross-Origin Resource Sharing (CORS) middleware for handling browser security restrictions on cross-origin HTTP requests.

## Installation

```python
from fastMiddleware import CORSMiddleware
```

## Quick Start

```python
from fastapi import FastAPI
from fastMiddleware import CORSMiddleware

app = FastAPI()

# Allow specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `allow_origins` | `list[str]` | `[]` | Allowed origin URLs |
| `allow_methods` | `list[str]` | `["GET", "POST", ...]` | Allowed HTTP methods |
| `allow_headers` | `list[str]` | `["*"]` | Allowed request headers |
| `allow_credentials` | `bool` | `True` | Allow cookies/auth headers |
| `expose_headers` | `list[str]` | `[]` | Headers exposed to browser |
| `max_age` | `int` | `600` | Preflight cache duration (seconds) |

## Examples

### Development (Allow All)

```python
# ⚠️ Development only!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # Required when using "*"
)
```

### Single Origin

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],
    allow_credentials=True,
)
```

### Multiple Origins

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://app.example.com",
        "https://admin.example.com",
        "https://mobile.example.com",
    ],
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
    allow_credentials=True,
)
```

### Expose Custom Headers

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],
    expose_headers=[
        "X-Request-ID",
        "X-RateLimit-Remaining",
        "X-RateLimit-Reset",
    ],
)
```

### Long Preflight Cache

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],
    max_age=86400,  # Cache preflight for 24 hours
)
```

### Specific Methods Only

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],
    allow_methods=["GET", "POST"],  # Only GET and POST
    allow_headers=["Content-Type", "Authorization"],
)
```

## Response Headers

### Simple Request

For simple requests (GET, HEAD, POST with simple content types):

```http
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Credentials: true
```

### Preflight Response (OPTIONS)

For complex requests, browsers send a preflight:

```http
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Allow-Credentials: true
Access-Control-Max-Age: 600
```

### Exposed Headers

When headers are exposed:

```http
Access-Control-Expose-Headers: X-Request-ID, X-RateLimit-Remaining
```

## How CORS Works

### Simple Requests

1. Browser sends request with `Origin` header
2. Server responds with `Access-Control-Allow-Origin`
3. Browser allows/blocks based on response

### Preflight Requests

For "complex" requests (custom headers, PUT/DELETE, etc.):

1. Browser sends OPTIONS request (preflight)
2. Server responds with allowed methods/headers
3. If allowed, browser sends actual request
4. Server responds normally

## Common Issues

### Wildcard with Credentials

```python
# ❌ This doesn't work!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,  # Cannot use with "*"
)

# ✅ Use specific origins instead
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],
    allow_credentials=True,
)
```

### Missing Headers

If custom headers aren't accessible in JavaScript:

```python
app.add_middleware(
    CORSMiddleware,
    expose_headers=["X-Custom-Header"],  # Must expose explicitly
)
```

### Preflight Not Cached

Browser keeps sending OPTIONS requests:

```python
app.add_middleware(
    CORSMiddleware,
    max_age=86400,  # Cache for 24 hours
)
```

## Environment Configuration

```python
import os

origins = os.environ.get("CORS_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins[0] else [],
    allow_credentials=True,
)
```

## Best Practices

1. **Never use `*` in production** with credentials
2. **Be specific** about allowed origins
3. **Use HTTPS** for all production origins
4. **Cache preflights** to reduce OPTIONS requests
5. **Only expose necessary headers**

## Security Considerations

- CORS is enforced by browsers, not servers
- Server-side requests bypass CORS entirely
- Always validate/authenticate requests server-side
- Don't rely on CORS as your only security measure

## Related Middlewares

- [SecurityHeadersMiddleware](./security-headers.md) - Security headers
- [TrustedHostMiddleware](./trusted-host.md) - Host validation
- [AuthenticationMiddleware](./authentication.md) - Request authentication
