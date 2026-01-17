# AuthenticationMiddleware

Pluggable authentication middleware supporting JWT tokens and API keys with configurable backends.

## Installation

```python
from fastMiddleware import (
    AuthenticationMiddleware,
    AuthConfig,
    JWTAuthBackend,
    APIKeyAuthBackend,
)
```

## Quick Start

```python
from fastapi import FastAPI
from fastMiddleware import AuthenticationMiddleware, JWTAuthBackend

app = FastAPI()

backend = JWTAuthBackend(secret="your-secret-key")
app.add_middleware(AuthenticationMiddleware, backend=backend)
```

## Configuration

### AuthConfig

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `exclude_paths` | `set[str]` | Health/docs paths | Paths without auth |
| `exclude_methods` | `set[str]` | `{"OPTIONS"}` | Methods without auth |
| `header_name` | `str` | `"Authorization"` | Auth header name |
| `header_scheme` | `str` | `"Bearer"` | Auth scheme prefix |
| `error_message` | `str` | `"Authentication required"` | Error message |
| `error_status_code` | `int` | `401` | Error status code |

## Backends

### JWTAuthBackend

JSON Web Token authentication.

```python
backend = JWTAuthBackend(
    secret="your-secret-key",
    algorithm="HS256",
    verify_exp=True,
    audience=None,
    issuer=None,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `secret` | `str` | Required | JWT secret key |
| `algorithm` | `str` | `"HS256"` | JWT algorithm |
| `verify_exp` | `bool` | `True` | Verify expiration |
| `audience` | `str \| None` | `None` | Expected audience |
| `issuer` | `str \| None` | `None` | Expected issuer |

### APIKeyAuthBackend

API key authentication.

```python
# Static keys
backend = APIKeyAuthBackend(
    valid_keys={"key1", "key2", "key3"},
    header_name="X-API-Key",
)

# Dynamic validation
backend = APIKeyAuthBackend(
    validator=my_validator_func,
    header_name="X-API-Key",
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `valid_keys` | `set[str] \| None` | `None` | Static valid keys |
| `validator` | `Callable \| None` | `None` | Async validator function |
| `header_name` | `str` | `"X-API-Key"` | Header name |

## Examples

### JWT Authentication

```python
from fastMiddleware import AuthenticationMiddleware, AuthConfig, JWTAuthBackend
import os

backend = JWTAuthBackend(
    secret=os.environ["JWT_SECRET"],
    algorithm="HS256",
)

config = AuthConfig(
    exclude_paths={
        "/",
        "/health",
        "/docs",
        "/openapi.json",
        "/login",
        "/register",
    },
)

app.add_middleware(
    AuthenticationMiddleware,
    backend=backend,
    config=config,
)
```

### Accessing User Data

```python
from fastapi import Request

@app.get("/me")
async def get_current_user(request: Request):
    # Auth data is stored in request.state.auth
    user = request.state.auth
    return {
        "user_id": user["sub"],
        "email": user.get("email"),
    }

@app.get("/protected")
async def protected_route(request: Request):
    if not hasattr(request.state, "auth"):
        # This shouldn't happen if middleware is configured correctly
        raise HTTPException(401, "Not authenticated")
    
    return {"message": f"Hello, {request.state.auth['sub']}"}
```

### API Key with Static Keys

```python
from fastMiddleware import APIKeyAuthBackend

backend = APIKeyAuthBackend(
    valid_keys={
        "sk_live_abc123",
        "sk_live_def456",
        "sk_test_xyz789",
    }
)

app.add_middleware(AuthenticationMiddleware, backend=backend)
```

### API Key with Database Validation

```python
async def validate_api_key(key: str) -> dict | None:
    """Validate API key against database."""
    from your_app.db import get_api_key
    
    api_key = await get_api_key(key)
    
    if api_key and api_key.is_active:
        return {
            "user_id": api_key.user_id,
            "tier": api_key.tier,
            "scopes": api_key.scopes,
            "rate_limit": api_key.rate_limit,
        }
    
    return None

backend = APIKeyAuthBackend(validator=validate_api_key)
```

### Combined JWT and API Key

```python
class CombinedAuthBackend:
    """Support both JWT and API key authentication."""
    
    def __init__(self, jwt_secret: str, api_keys: set[str]):
        self.jwt_backend = JWTAuthBackend(secret=jwt_secret)
        self.api_key_backend = APIKeyAuthBackend(valid_keys=api_keys)
    
    async def authenticate(self, request: Request) -> dict | None:
        # Try JWT first
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            return await self.jwt_backend.authenticate(request)
        
        # Try API key
        if "X-API-Key" in request.headers:
            return await self.api_key_backend.authenticate(request)
        
        return None

backend = CombinedAuthBackend(
    jwt_secret=os.environ["JWT_SECRET"],
    api_keys={"key1", "key2"},
)
```

### Custom Error Response

```python
config = AuthConfig(
    error_message="Please login to access this resource",
    error_status_code=401,
)
```

Response:
```json
{
    "detail": "Please login to access this resource"
}
```

## Request Flow

1. Request arrives at middleware
2. Check if path/method is excluded
3. Extract token from header
4. Validate token with backend
5. If valid: store auth data in `request.state.auth`
6. If invalid: return 401 error

## Error Responses

### Missing Token

```json
{
    "detail": "Authentication required"
}
```

### Invalid Token

```json
{
    "detail": "Invalid authentication credentials"
}
```

### Expired Token

```json
{
    "detail": "Token has expired"
}
```

## Best Practices

1. **Use environment variables** for secrets
2. **Exclude public routes** explicitly
3. **Set short expiration times** for JWT tokens
4. **Rotate secrets** regularly
5. **Use HTTPS** in production
6. **Log authentication failures** for security monitoring

## Security Considerations

- Never hardcode secrets in source code
- Use strong, random secrets (32+ characters)
- Implement token refresh for long sessions
- Consider using RS256 for distributed systems
- Rate limit authentication endpoints

## Related Middlewares

- [RateLimitMiddleware](./rate-limit.md) - Rate limiting
- [SecurityHeadersMiddleware](./security-headers.md) - Security headers
- [RequestContextMiddleware](./request-context.md) - Request context
