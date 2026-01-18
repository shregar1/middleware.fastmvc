# HealthCheckMiddleware

Built-in health, readiness, and liveness endpoints for Kubernetes and load balancer health checks.

## Installation

```python
from fastmiddleware import HealthCheckMiddleware, HealthConfig

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import HealthCheckMiddleware

app = FastAPI()

app.add_middleware(HealthCheckMiddleware)

```

## Configuration

### HealthConfig

| Parameter | Type | Default | Description |
| ----------- | ------ | --------- | ------------- |
| `health_path` | `str` | `"/health"` | Health endpoint path |
| `ready_path` | `str` | `"/ready"` | Readiness endpoint path |
| `live_path` | `str` | `"/live"` | Liveness endpoint path |
| `include_details` | `bool` | `True` | Include detailed info |
| `version` | `str \| None` | `None` | Application version |
| `service_name` | `str \| None` | `None` | Service name |
| `custom_checks` | `dict` | `{}` | Custom health checks |

## Endpoints

| Endpoint | Purpose | Returns |
| ---------- | --------- | --------- |
| `/health` | Full health status | Detailed health info |
| `/ready` | Readiness check | Ready/not ready |
| `/live` | Liveness check | Alive/not alive |

## Response Formats

### /health

```json
{
    "status": "healthy",
    "timestamp": "2024-01-01T00:00:00Z",
    "uptime_seconds": 3600.5,
    "version": "1.0.0",
    "service": "my-api",
    "checks": {
        "database": "healthy",
        "redis": "healthy"
    }
}

```

### /ready

```json
{
    "ready": true,
    "timestamp": "2024-01-01T00:00:00Z",
    "checks": {
        "database": "healthy",
        "redis": "healthy"
    }
}

```

### /live

```json
{
    "alive": true,
    "timestamp": "2024-01-01T00:00:00Z"
}

```

## Examples

### Basic Configuration

```python
config = HealthConfig(
    version="1.0.0",
    service_name="my-api",
)

app.add_middleware(HealthCheckMiddleware, config=config)

```

### With Custom Checks

```python
async def check_database() -> bool:
    """Check database connectivity."""
    try:
        await database.execute("SELECT 1")
        return True
    except Exception:
        return False

async def check_redis() -> bool:
    """Check Redis connectivity."""
    try:
        await redis.ping()
        return True
    except Exception:
        return False

async def check_external_api() -> bool:
    """Check external API availability."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.example.com/health",
                timeout=5.0
            )
            return response.status_code == 200
    except Exception:
        return False

config = HealthConfig(
    version="1.0.0",
    service_name="my-api",
    custom_checks={
        "database": check_database,
        "redis": check_redis,
        "external_api": check_external_api,
    },
)

app.add_middleware(HealthCheckMiddleware, config=config)

```

### Custom Paths

```python
config = HealthConfig(
    health_path="/healthz",
    ready_path="/readiness",
    live_path="/liveness",
)

app.add_middleware(HealthCheckMiddleware, config=config)

```

### Without Details

```python
config = HealthConfig(
    include_details=False,
)

# Response:

# {"status": "healthy", "timestamp": "..."}

```

## Kubernetes Configuration

### Pod Spec

```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: my-api
      image: my-api:1.0.0
      ports:
        - containerPort: 8000

      livenessProbe:
        httpGet:
          path: /live
          port: 8000
        initialDelaySeconds: 10
        periodSeconds: 10
        timeoutSeconds: 5
        failureThreshold: 3

      readinessProbe:
        httpGet:
          path: /ready
          port: 8000
        initialDelaySeconds: 5
        periodSeconds: 5
        timeoutSeconds: 3
        failureThreshold: 3

      startupProbe:
        httpGet:
          path: /health
          port: 8000
        initialDelaySeconds: 0
        periodSeconds: 5
        failureThreshold: 30

```

### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-api
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: my-api
          livenessProbe:
            httpGet:
              path: /live
              port: 8000
          readinessProbe:
            httpGet:
              path: /ready
              port: 8000

```

## Health Check Types

### Liveness

**Purpose**: Is the application running?

- Simple check
- Always returns 200 if process is alive
- Failure triggers pod restart

**When to fail**:

- Application deadlock

- Unrecoverable state

- Resource exhaustion

### Readiness

**Purpose**: Can the application serve traffic?

- Checks dependencies
- Returns 503 if not ready
- Failure removes from load balancer

**When to fail**:

- Database unavailable

- Cache unavailable

- Required service down

### Health (Startup)

**Purpose**: Full application health

- Detailed status
- Includes all checks
- Used for startup verification

## Status Codes

| Condition | /health | /ready | /live |
| ----------- | --------- | -------- | ------- |
| All healthy | 200 | 200 | 200 |
| Some checks failed | 503 | 503 | 200 |
| Application alive | 200/503 | 200/503 | 200 |

## Check Failure Handling

When a check fails:

```json
{
    "status": "unhealthy",
    "timestamp": "2024-01-01T00:00:00Z",
    "checks": {
        "database": "healthy",
        "redis": "unhealthy"  // Failed check
    }
}

```

HTTP Status: `503 Service Unavailable`

## Best Practices

1. **Keep liveness simple** - Should always pass if app is running
2. **Use readiness for dependencies** - Database, cache, etc.
3. **Set appropriate timeouts** - Don't let checks hang
4. **Log check failures** - For debugging
5. **Don't expose sensitive info** - In health responses

## Performance Considerations

- Health checks run on every request to health endpoints
- Keep checks fast (< 1 second)
- Cache check results if expensive
- Use connection pools for database checks

## Related Middlewares

- [MetricsMiddleware](./metrics.md) - Monitor health check metrics
- [MaintenanceMiddleware](./maintenance.md) - Maintenance mode
