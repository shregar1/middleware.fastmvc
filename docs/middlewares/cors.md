# CORSMiddleware

Cross-Origin Resource Sharing (CORS) middleware that handles preflight requests and adds appropriate headers for cross-origin access.

## Installation

```python
from src import CORSMiddleware
```

## Quick Start

```python
from fastapi import FastAPI
from src import CORSMiddleware

app = FastAPI()

# Allow specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
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
| `max_age` | `int` | `600` | Preflight cache time (seconds) |

## Examples

### Production Configuration

```python
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
    max_age=3600,  # Cache preflight for 1 hour
)
```

### Development (Allow All)

```python
# ⚠️ Only for development!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # Required when using "*"
)
```

### Allow Multiple Origins with Credentials

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8080",
        "https://staging.example.com",
        "https://app.example.com",
    ],
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
        "X-RateLimit-Limit",
        "X-RateLimit-Remaining",
        "X-RateLimit-Reset",
    ],
)
```

## How It Works

### Simple Requests

For simple requests (GET, POST with simple content types), CORS headers are added to the response:

```http
HTTP/1.1 200 OK
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Credentials: true
```

### Preflight Requests

For complex requests, browsers send an OPTIONS preflight request first:

```http
OPTIONS /api/data HTTP/1.1
Origin: https://app.example.com
Access-Control-Request-Method: POST
Access-Control-Request-Headers: Content-Type, Authorization
```

Response:

```http
HTTP/1.1 200 OK
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Allow-Credentials: true
Access-Control-Max-Age: 3600
```

## Headers Reference

### Request Headers (from browser)

| Header | Description |
|--------|-------------|
| `Origin` | The requesting origin |
| `Access-Control-Request-Method` | Method for preflight |
| `Access-Control-Request-Headers` | Headers for preflight |

### Response Headers (from server)

| Header | Description |
|--------|-------------|
| `Access-Control-Allow-Origin` | Allowed origin(s) |
| `Access-Control-Allow-Methods` | Allowed methods |
| `Access-Control-Allow-Headers` | Allowed headers |
| `Access-Control-Allow-Credentials` | Allow credentials |
| `Access-Control-Expose-Headers` | Exposed headers |
| `Access-Control-Max-Age` | Preflight cache time |

## Common Issues

### Credentials with Wildcard Origin

```python
# ❌ This will fail - can't use credentials with "*"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,  # Error!
)

# ✅ Use specific origins with credentials
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],
    allow_credentials=True,
)
```

### Missing Exposed Headers

If JavaScript can't read custom headers:

```python
# ✅ Expose the headers you need
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],
    expose_headers=["X-Custom-Header", "X-Request-ID"],
)
```

### Preflight Caching

Increase `max_age` to reduce preflight requests:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],
    max_age=86400,  # Cache for 24 hours
)
```

## Security Best Practices

1. **Never use `"*"` in production** with credentials
2. **List specific origins** instead of wildcards
3. **Limit allowed methods** to what's needed
4. **Limit allowed headers** to what's needed
5. **Use HTTPS origins** in production

## Related

- [SecurityHeadersMiddleware](security-headers.md) - Security headers
- [TrustedHostMiddleware](trusted-host.md) - Host validation

