# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.5.x   | :white_check_mark: |
| < 0.5   | :x:                |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to: **security@hyyre.dev**

Please include:

1. **Description**: Clear description of the vulnerability
2. **Impact**: What an attacker could achieve
3. **Steps to Reproduce**: Detailed steps to reproduce the issue
4. **Affected Components**: Which middleware(s) are affected
5. **Suggested Fix**: If you have one (optional)

### What to Expect

- **Acknowledgment**: Within 48 hours
- **Initial Assessment**: Within 1 week
- **Resolution Timeline**: Based on severity
  - Critical: 24-48 hours
  - High: 1 week
  - Medium: 2 weeks
  - Low: Next release

### Disclosure Policy

- We follow responsible disclosure practices
- We'll work with you to understand and resolve the issue
- We'll credit you in our security advisories (unless you prefer anonymity)
- We'll notify you when the fix is released

## Security Best Practices

When using this middleware package:

### Secret Management

```python
# ❌ Never hardcode secrets
app.add_middleware(AuthMiddleware, secret_key="my-secret-key")

# ✅ Use environment variables
import os
app.add_middleware(
    AuthMiddleware,
    secret_key=os.environ["JWT_SECRET_KEY"]
)
```

### HTTPS Only

```python
# Always use HTTPS in production
app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(
    SecurityHeadersMiddleware,
    enable_hsts=True,
    hsts_preload=True,
)
```

### Rate Limiting

```python
# Protect against DDoS
app.add_middleware(
    RateLimitMiddleware,
    requests_per_minute=100,
)
```

### Input Validation

```python
# Validate all inputs
app.add_middleware(
    JSONSchemaMiddleware,
    schemas={"/api/users": user_schema},
)
```

### Secure Headers

The `SecurityHeadersMiddleware` adds these headers by default:

- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Content-Security-Policy` (configurable)
- `Strict-Transport-Security` (when enabled)

### Recommended Middleware Stack

```python
# Production security stack
app.add_middleware(CompressionMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(AuthenticationMiddleware, ...)
app.add_middleware(RateLimitMiddleware, requests_per_minute=100)
app.add_middleware(SecurityHeadersMiddleware, enable_hsts=True)
app.add_middleware(CSRFMiddleware, secret_key=os.environ["CSRF_SECRET"])
app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["example.com"])
app.add_middleware(RequestIDMiddleware)
```

## Known Security Considerations

### AuthenticationMiddleware (JWT)

- Use strong secrets (32+ characters)
- Set appropriate token expiration
- Use `HS256` minimum, prefer `RS256` for production
- Never expose secret keys in logs

### RateLimitMiddleware

- Use per-IP or per-user limiting
- Consider using Redis for distributed systems
- Set appropriate limits for your use case

### CSRFMiddleware

- Always use with forms/cookies
- Exclude API endpoints that use token auth
- Use secure, HTTPOnly cookies

### SessionMiddleware

- Use secure cookies in production
- Set appropriate session timeouts
- Regenerate session IDs after authentication

## Security Scanning

We use:

- **Bandit**: Static security analysis
- **CodeQL**: Code scanning
- **Dependabot**: Dependency updates
- **detect-secrets**: Secret detection

Run locally:

```bash
make security  # Runs bandit
```

## Security Updates

Security updates are released as:

1. Patch versions for the current minor release
2. GitHub Security Advisories
3. Release notes with CVE references (if applicable)

Subscribe to releases to get notifications.
