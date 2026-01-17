# AuthenticationMiddleware

Pluggable authentication middleware supporting JWT tokens and API keys with customizable backends.

## Installation

```python
from src import (
    AuthenticationMiddleware,
    AuthConfig,
    JWTAuthBackend,
    APIKeyAuthBackend,
)
```

## Quick Start

```python
from fastapi import FastAPI
from src import AuthenticationMiddleware, JWTAuthBackend

app = FastAPI()

backend = JWTAuthBackend(secret="your-secret-key")

app.add_middleware(
    AuthenticationMiddleware,
    backend=backend,
)
```

## Configuration

### AuthConfig

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `exclude_paths` | `set[str]` | Health/docs paths | Paths without auth |
| `exclude_methods` | `set[str]` | `{"OPTIONS"}` | Methods without auth |
| `header_name` | `str` | `"Authorization"` | Auth header name |
| `header_scheme` | `str` | `"Bearer"` | Auth scheme prefix |
| `error_message` | `str` | `"Authentication required"` | Unauthorized message |
| `error_status_code` | `int` | `401` | Unauthorized status |

## Auth Backends

### JWTAuthBackend

```python
from src import JWTAuthBackend

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
| `secret` | `str` | Required | JWT signing secret |
| `algorithm` | `str` | `"HS256"` | JWT algorithm |
| `verify_exp` | `bool` | `True` | Verify expiration |
| `audience` | `str \| None` | `None` | Expected audience |
| `issuer` | `str \| None` | `None` | Expected issuer |

### APIKeyAuthBackend

```python
from src import APIKeyAuthBackend

# Static keys
backend = APIKeyAuthBackend(
    valid_keys={"key1", "key2", "key3"},
    header_name="X-API-Key",
)

# Dynamic validation
backend = APIKeyAuthBackend(
    validator=my_validator_function,
    header_name="X-API-Key",
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `valid_keys` | `set[str] \| None` | `None` | Static valid keys |
| `validator` | `Callable \| None` | `None` | Async validator function |
| `header_name` | `str` | `"X-API-Key"` | API key header |

## Examples

### JWT Authentication

```python
import os
from fastapi import FastAPI, Request
from src import AuthenticationMiddleware, AuthConfig, JWTAuthBackend

app = FastAPI()

backend = JWTAuthBackend(
    secret=os.environ["JWT_SECRET"],
    algorithm="HS256",
    verify_exp=True,
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

@app.get("/me")
async def get_current_user(request: Request):
    # Access decoded JWT payload
    return {"user": request.state.auth}
```

### API Key Authentication

```python
from src import AuthenticationMiddleware, APIKeyAuthBackend

# Static keys
backend = APIKeyAuthBackend(
    valid_keys={
        "sk_live_abc123",
        "sk_live_def456",
    }
)

app.add_middleware(AuthenticationMiddleware, backend=backend)
```

### Dynamic API Key Validation

```python
from src import APIKeyAuthBackend

async def validate_api_key(key: str) -> dict | None:
    """Validate API key and return user info."""
    # Query database
    key_record = await db.api_keys.find_one({"key": key})
    
    if key_record and key_record["active"]:
        return {
            "user_id": key_record["user_id"],
            "tier": key_record["tier"],
            "scopes": key_record["scopes"],
        }
    return None

backend = APIKeyAuthBackend(validator=validate_api_key)
```

### Custom Auth Backend

```python
from src.authentication import AuthBackend

class CustomAuthBackend(AuthBackend):
    """Custom authentication backend."""
    
    async def authenticate(self, token: str) -> dict | None:
        """Authenticate and return user data or None."""
        # Your custom logic
        if await self.verify_token(token):
            return {"user_id": "123", "role": "admin"}
        return None

backend = CustomAuthBackend()
app.add_middleware(AuthenticationMiddleware, backend=backend)
```

### Exclude Multiple Paths

```python
config = AuthConfig(
    exclude_paths={
        # Public endpoints
        "/",
        "/about",
        "/pricing",
        
        # Auth endpoints
        "/login",
        "/register",
        "/forgot-password",
        "/reset-password",
        
        # Health checks
        "/health",
        "/ready",
        "/live",
        
        # API documentation
        "/docs",
        "/redoc",
        "/openapi.json",
    },
    exclude_methods={"OPTIONS", "HEAD"},
)
```

## Request State

After authentication, user data is available in `request.state.auth`:

```python
@app.get("/profile")
async def get_profile(request: Request):
    user_data = request.state.auth
    
    # JWT payload example
    # {
    #     "sub": "user123",
    #     "email": "user@example.com",
    #     "exp": 1234567890,
    #     "iat": 1234567800,
    # }
    
    return {"user_id": user_data.get("sub")}
```

## Error Responses

### Missing Token

```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
    "detail": "Authentication required"
}
```

### Invalid Token

```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
    "detail": "Invalid authentication credentials"
}
```

## Security Best Practices

1. **Use environment variables** for secrets
2. **Enable expiration verification** (`verify_exp=True`)
3. **Use short token lifetimes** (15-60 minutes)
4. **Implement refresh tokens** for long sessions
5. **Exclude only necessary paths** from auth
6. **Use HTTPS** to protect tokens in transit

## Related

- [RateLimitMiddleware](rate-limit.md) - Rate limiting
- [RequestIDMiddleware](request-id.md) - Request tracing

