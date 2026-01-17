# TrustedHostMiddleware

Validates the HTTP Host header against a list of allowed hosts to prevent host header attacks.

## Installation

```python
from src import TrustedHostMiddleware
```

## Quick Start

```python
from fastapi import FastAPI
from src import TrustedHostMiddleware

app = FastAPI()

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["example.com", "www.example.com"],
)
```

## Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `allowed_hosts` | `list[str]` | `["*"]` | Allowed host patterns |
| `www_redirect` | `bool` | `False` | Redirect www to non-www |
| `redirect_to_primary` | `bool` | `False` | Redirect to primary host |
| `primary_host` | `str \| None` | `None` | Primary host for redirects |

## Host Patterns

| Pattern | Matches | Example |
|---------|---------|---------|
| `"example.com"` | Exact match | `example.com` ✓, `api.example.com` ✗ |
| `"*.example.com"` | Any subdomain | `api.example.com` ✓, `example.com` ✗ |
| `"*"` | Any host | All hosts (development only!) |

## Examples

### Production Configuration

```python
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "api.example.com",
        "example.com",
        "www.example.com",
    ],
)
```

### Wildcard Subdomains

```python
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "*.example.com",  # All subdomains
        "example.com",     # Root domain
    ],
)
```

### Development (Allow All)

```python
# ⚠️ Only for development!
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],
)
```

### With WWW Redirect

```python
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["example.com", "www.example.com"],
    www_redirect=True,  # Redirect www.example.com → example.com
)
```

### Redirect to Primary Host

```python
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["example.com", "legacy.example.com"],
    redirect_to_primary=True,
    primary_host="example.com",
)
```

## Error Response

Invalid host requests receive a 400 Bad Request:

```http
HTTP/1.1 400 Bad Request
Content-Type: text/plain

Invalid host header
```

## Why Use This?

### Host Header Attacks

Without validation, attackers can manipulate the Host header:

```http
GET /reset-password HTTP/1.1
Host: evil.com
```

If your app uses the Host header to generate URLs (e.g., password reset links), this could redirect users to malicious sites.

### Cache Poisoning

Invalid Host headers can poison web caches, serving malicious content to legitimate users.

## Security Best Practices

1. **Always specify allowed hosts** in production
2. **Never use `"*"`** in production
3. **Include all valid domains** (with and without www)
4. **Use with HTTPS** for complete protection
5. **Place early in middleware stack** (first to execute)

## Middleware Order

```python
# Trusted host should be last added (first executed)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["..."])
```

## Related

- [SecurityHeadersMiddleware](security-headers.md) - Security headers
- [CORSMiddleware](cors.md) - CORS handling

