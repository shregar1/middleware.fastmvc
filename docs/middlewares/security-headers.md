# SecurityHeadersMiddleware

Adds comprehensive security headers to protect against common web vulnerabilities including XSS, clickjacking, and MIME sniffing attacks.

## Installation

```python
from fastMiddleware import SecurityHeadersMiddleware, SecurityHeadersConfig
```

## Quick Start

```python
from fastapi import FastAPI
from fastMiddleware import SecurityHeadersMiddleware

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
| `enable_hsts` | `bool` | `False` | Enable HTTP Strict Transport Security |
| `hsts_max_age` | `int` | `31536000` | HSTS max-age in seconds (1 year) |
| `hsts_preload` | `bool` | `False` | Add preload directive for HSTS preload list |
| `hsts_include_subdomains` | `bool` | `True` | Apply HSTS to all subdomains |
| `content_security_policy` | `str \| None` | `None` | Content-Security-Policy header value |
| `x_frame_options` | `str` | `"DENY"` | X-Frame-Options header value |
| `x_content_type_options` | `str` | `"nosniff"` | X-Content-Type-Options header value |
| `referrer_policy` | `str` | `"strict-origin-when-cross-origin"` | Referrer-Policy header value |
| `permissions_policy` | `str \| None` | `None` | Permissions-Policy header value |
| `cross_origin_opener_policy` | `str` | `"same-origin"` | Cross-Origin-Opener-Policy value |
| `cross_origin_resource_policy` | `str` | `"same-origin"` | Cross-Origin-Resource-Policy value |

## Headers Added

| Header | Default Value | Purpose |
|--------|---------------|---------|
| `X-Content-Type-Options` | `nosniff` | Prevents MIME type sniffing |
| `X-Frame-Options` | `DENY` | Prevents clickjacking attacks |
| `X-XSS-Protection` | `1; mode=block` | Legacy XSS filter (for older browsers) |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Controls referrer information |
| `Content-Security-Policy` | Configurable | Controls resource loading |
| `Permissions-Policy` | Configurable | Controls browser features |
| `Strict-Transport-Security` | Optional | Forces HTTPS connections |
| `Cross-Origin-Opener-Policy` | `same-origin` | Isolates browsing context |
| `Cross-Origin-Resource-Policy` | `same-origin` | Controls cross-origin access |

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

### With HSTS for Production

```python
app.add_middleware(
    SecurityHeadersMiddleware,
    enable_hsts=True,
    hsts_preload=True,
    hsts_max_age=31536000,
)
```

Additional header:
```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

### With Content Security Policy

```python
config = SecurityHeadersConfig(
    content_security_policy=(
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.example.com; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self' https://fonts.googleapis.com; "
        "connect-src 'self' https://api.example.com"
    ),
)

app.add_middleware(SecurityHeadersMiddleware, config=config)
```

### Allowing Frames from Same Origin

```python
app.add_middleware(
    SecurityHeadersMiddleware,
    x_frame_options="SAMEORIGIN",  # Allow embedding in same-origin iframes
)
```

### Restricting Browser Features

```python
app.add_middleware(
    SecurityHeadersMiddleware,
    permissions_policy=(
        "geolocation=(), "
        "microphone=(), "
        "camera=(), "
        "payment=(), "
        "usb=()"
    ),
)
```

### Full Production Configuration

```python
from fastMiddleware import SecurityHeadersMiddleware, SecurityHeadersConfig

config = SecurityHeadersConfig(
    enable_hsts=True,
    hsts_preload=True,
    hsts_max_age=31536000,
    hsts_include_subdomains=True,
    content_security_policy=(
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self'; "
        "frame-ancestors 'none'"
    ),
    x_frame_options="DENY",
    referrer_policy="strict-origin-when-cross-origin",
    permissions_policy="geolocation=(), microphone=(), camera=()",
)

app.add_middleware(SecurityHeadersMiddleware, config=config)
```

## Path Exclusion

Exclude specific paths from header addition:

```python
app.add_middleware(
    SecurityHeadersMiddleware,
    exclude_paths={"/legacy", "/embed"},
)
```

## Best Practices

1. **Always enable HSTS in production** - Protects against protocol downgrade attacks
2. **Use CSP** - Mitigates XSS attacks by controlling resource loading
3. **Start with strict policies** - Relax as needed rather than starting permissive
4. **Test thoroughly** - CSP can break functionality if misconfigured
5. **Use report-uri** - Monitor CSP violations in production

## Security Considerations

- HSTS preload is permanent - ensure HTTPS works before enabling
- CSP with `'unsafe-inline'` weakens XSS protection
- Some older browsers don't support all headers
- Test across different browsers before deployment

## Related Middlewares

- [TrustedHostMiddleware](./trusted-host.md) - Host header validation
- [CORSMiddleware](./cors.md) - Cross-origin resource sharing
- [AuthenticationMiddleware](./authentication.md) - Request authentication
