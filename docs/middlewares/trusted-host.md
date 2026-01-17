# TrustedHostMiddleware

Validates the HTTP Host header to prevent host header attacks, DNS rebinding, and cache poisoning.

## Installation

```python
from fastMiddleware import TrustedHostMiddleware, TrustedHostConfig
```

## Quick Start

```python
from fastapi import FastAPI
from fastMiddleware import TrustedHostMiddleware

app = FastAPI()

# Allow specific hosts
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["example.com", "www.example.com"],
)
```

## Configuration

### TrustedHostConfig

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `allowed_hosts` | `Sequence[str]` | `["*"]` | List of allowed host patterns |
| `www_redirect` | `bool` | `False` | Redirect www to non-www |
| `redirect_to_primary` | `bool` | `False` | Redirect all hosts to primary |
| `primary_host` | `str \| None` | `None` | Primary host for redirects |

## Host Patterns

| Pattern | Matches | Example |
|---------|---------|---------|
| `example.com` | Exact host | Only `example.com` |
| `*.example.com` | Subdomains | `api.example.com`, `www.example.com` |
| `*` | Any host | All hosts (development only) |

## Examples

### Single Host

```python
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["api.example.com"],
)
```

### Multiple Hosts

```python
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "example.com",
        "www.example.com",
        "api.example.com",
    ],
)
```

### Wildcard Subdomains

```python
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*.example.com"],  # Matches any subdomain
)
```

### Mixed Patterns

```python
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "example.com",           # Exact match
        "*.staging.example.com", # Staging subdomains
        "localhost",             # Local development
    ],
)
```

### Development Mode

```python
# Allow any host (development only!)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],
)
```

> ⚠️ **Warning**: Never use `["*"]` in production!

### WWW Redirect

```python
config = TrustedHostConfig(
    allowed_hosts=["example.com", "www.example.com"],
    www_redirect=True,  # Redirect www.example.com → example.com
)

app.add_middleware(TrustedHostMiddleware, config=config)
```

### Primary Host Redirect

```python
config = TrustedHostConfig(
    allowed_hosts=["example.com", "example.org", "example.net"],
    redirect_to_primary=True,
    primary_host="example.com",  # All requests redirect here
)

app.add_middleware(TrustedHostMiddleware, config=config)
```

## Response

### Valid Host

Request proceeds normally.

### Invalid Host

```http
HTTP/1.1 400 Bad Request

Invalid host header
```

## Path Exclusion

Exclude paths from host validation (e.g., for health checks):

```python
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["api.example.com"],
    exclude_paths={"/health", "/ready", "/live"},
)
```

## Environment-Based Configuration

```python
import os

# Development vs Production
if os.environ.get("ENVIRONMENT") == "development":
    allowed_hosts = ["localhost", "127.0.0.1", "*.localhost"]
else:
    allowed_hosts = os.environ["ALLOWED_HOSTS"].split(",")

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=allowed_hosts,
)
```

## Kubernetes/Docker

For containerized applications:

```python
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "api.example.com",    # Public domain
        "api.internal",       # Internal service name
        "api.default.svc",    # Kubernetes service
        "localhost",          # Health checks
    ],
)
```

## Security Considerations

### Host Header Attacks

Without validation, attackers can:
- **Cache poisoning**: Inject malicious content into CDN caches
- **Password reset poisoning**: Redirect password reset links
- **Web cache deception**: Steal sensitive cached data
- **Server-Side Request Forgery (SSRF)**: Bypass access controls

### Best Practices

1. **Be specific** - List only necessary hosts
2. **Avoid wildcards in production** - Use exact matches when possible
3. **Include all valid hosts** - Don't forget www, API subdomains
4. **Test thoroughly** - Ensure all legitimate traffic works

## Common Issues

### Port Numbers

Hosts with non-standard ports are handled automatically:

```python
# This works for both example.com and example.com:8080
allowed_hosts=["example.com"]
```

### Case Sensitivity

Host matching is case-insensitive:

```python
# Matches EXAMPLE.COM, Example.Com, example.com
allowed_hosts=["example.com"]
```

### Behind a Proxy

If behind a reverse proxy, ensure the proxy forwards the original Host header:

```nginx
# nginx configuration
proxy_set_header Host $host;
```

## Related Middlewares

- [SecurityHeadersMiddleware](./security-headers.md) - Security headers
- [CORSMiddleware](./cors.md) - Cross-origin settings
