# SecurityHeadersMiddleware

Adds comprehensive security headers to protect against common web vulnerabilities like XSS, clickjacking, and MIME-type sniffing.

## Installation

```python
from src import SecurityHeadersMiddleware, SecurityHeadersConfig
```

## Quick Start

```python
from fastapi import FastAPI
from src import SecurityHeadersMiddleware

app = FastAPI()

# Basic usage
app.add_middleware(SecurityHeadersMiddleware)

# With HSTS enabled
app.add_middleware(SecurityHeadersMiddleware, enable_hsts=True)
```

## Configuration

### SecurityHeadersConfig

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `enable_hsts` | `bool` | `False` | Enable Strict-Transport-Security |
| `hsts_max_age` | `int` | `31536000` | HSTS max-age in seconds (1 year) |
| `hsts_preload` | `bool` | `False` | Add HSTS preload directive |
| `hsts_include_subdomains` | `bool` | `True` | Include subdomains in HSTS |
| `content_security_policy` | `str \| None` | `None` | Content-Security-Policy header value |
| `x_frame_options` | `str` | `"DENY"` | X-Frame-Options header value |
| `x_content_type_options` | `str` | `"nosniff"` | X-Content-Type-Options value |
| `referrer_policy` | `str` | `"strict-origin-when-cross-origin"` | Referrer-Policy value |
| `permissions_policy` | `str \| None` | `None` | Permissions-Policy value |
| `cross_origin_opener_policy` | `str` | `"same-origin"` | Cross-Origin-Opener-Policy |
| `cross_origin_resource_policy` | `str` | `"same-origin"` | Cross-Origin-Resource-Policy |

## Headers Added

| Header | Default Value | Purpose |
|--------|---------------|---------|
| `X-Content-Type-Options` | `nosniff` | Prevents MIME-type sniffing attacks |
| `X-Frame-Options` | `DENY` | Prevents clickjacking by blocking iframes |
| `X-XSS-Protection` | `1; mode=block` | Legacy XSS filter (for older browsers) |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Controls referrer information leakage |
| `Content-Security-Policy` | Configurable | Controls which resources can be loaded |
| `Permissions-Policy` | Configurable | Controls browser feature access |
| `Strict-Transport-Security` | Optional | Forces HTTPS connections |
| `Cross-Origin-Opener-Policy` | `same-origin` | Isolates browsing context |
| `Cross-Origin-Resource-Policy` | `same-origin` | Controls cross-origin resource sharing |

## Examples

### Basic Security Headers

```python
app.add_middleware(SecurityHeadersMiddleware)
```

Response headers:
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Resource-Policy: same-origin
```

### Production Configuration with HSTS

```python
from src import SecurityHeadersMiddleware, SecurityHeadersConfig

config = SecurityHeadersConfig(
    enable_hsts=True,
    hsts_max_age=31536000,  # 1 year
    hsts_preload=True,
    hsts_include_subdomains=True,
    content_security_policy="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:;",
    permissions_policy="geolocation=(), microphone=(), camera=()",
)

app.add_middleware(SecurityHeadersMiddleware, config=config)
```

### Allowing Iframes from Same Origin

```python
app.add_middleware(
    SecurityHeadersMiddleware,
    x_frame_options="SAMEORIGIN",
)
```

### Content Security Policy

```python
# Strict CSP
csp = "; ".join([
    "default-src 'self'",
    "script-src 'self'",
    "style-src 'self' 'unsafe-inline'",
    "img-src 'self' data: https:",
    "font-src 'self'",
    "connect-src 'self' https://api.example.com",
    "frame-ancestors 'none'",
    "base-uri 'self'",
    "form-action 'self'",
])

app.add_middleware(
    SecurityHeadersMiddleware,
    content_security_policy=csp,
)
```

### Exclude Paths

```python
app.add_middleware(
    SecurityHeadersMiddleware,
    exclude_paths={"/embed", "/widget"},  # Allow iframes for these
)
```

## Security Recommendations

### For Production

1. **Enable HSTS** - Always enable for HTTPS sites
2. **Use CSP** - Define a strict Content-Security-Policy
3. **Disable embedding** - Use `X-Frame-Options: DENY` unless needed
4. **Limit permissions** - Use Permissions-Policy to disable unused features

### For Development

```python
# Less strict for development
app.add_middleware(
    SecurityHeadersMiddleware,
    enable_hsts=False,  # Don't force HTTPS locally
    content_security_policy=None,  # Allow all resources
)
```

## Response Example

```http
HTTP/1.1 200 OK
Content-Type: application/json
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
Content-Security-Policy: default-src 'self'
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Resource-Policy: same-origin
```

## Related

- [TrustedHostMiddleware](trusted-host.md) - Host header validation
- [CORSMiddleware](cors.md) - Cross-origin resource sharing

