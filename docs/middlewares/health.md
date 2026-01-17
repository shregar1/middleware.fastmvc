# HealthCheckMiddleware

Provides built-in health, readiness, and liveness endpoints for Kubernetes and monitoring systems.

## Installation

```python
from src import HealthCheckMiddleware, HealthConfig
```

## Quick Start

```python
from fastapi import FastAPI
from src import HealthCheckMiddleware

app = FastAPI()

app.add_middleware(HealthCheckMiddleware)
```

## Configuration

### HealthConfig

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `health_path` | `str` | `"/health"` | Health endpoint path |
| `ready_path` | `str` | `"/ready"` | Readiness endpoint path |
| `live_path` | `str` | `"/live"` | Liveness endpoint path |
| `version` | `str \| None` | `None` | Application version |
| `service_name` | `str \| None` | `None` | Service name |
| `include_details` | `bool` | `True` | Include detailed info |
| `custom_checks` | `dict` | `{}` | Custom health check functions |

## Endpoints

| Endpoint | Purpose | Success | Failure |
|----------|---------|---------|---------|
| `/health` | Full health status | 200 | 503 |
| `/ready` | Ready to receive traffic | 200 | 503 |
| `/live` | Application is running | 200 | - |

## Response Formats

### Health Endpoint

```json
{
    "status": "healthy",
    "timestamp": "2024-01-01T00:00:00Z",
    "uptime_seconds": 3600.5,
    "version": "1.0.0",
    "service": "my-api",
    "checks": {
        "database": "healthy",
        "cache": "healthy"
    }
}
```

### Ready Endpoint

```json
{
    "ready": true,
    "timestamp": "2024-01-01T00:00:00Z",
    "checks": {
        "database": "healthy"
    }
}
```

### Live Endpoint

```json
{
    "alive": true,
    "timestamp": "2024-01-01T00:00:00Z"
}
```

## Examples

### Basic Configuration

```python
from src import HealthCheckMiddleware, HealthConfig

config = HealthConfig(
    version="1.0.0",
    service_name="my-api",
)

app.add_middleware(HealthCheckMiddleware, config=config)
```

### Custom Health Checks

```python
async def check_database() -> bool:
    """Check database connection."""
    try:
        await db.execute("SELECT 1")
        return True
    except Exception:
        return False

async def check_redis() -> bool:
    """Check Redis connection."""
    try:
        await redis.ping()
        return True
    except Exception:
        return False

async def check_disk_space() -> bool:
    """Check disk space."""
    import shutil
    usage = shutil.disk_usage("/")
    return usage.free > 1_000_000_000  # > 1GB free

config = HealthConfig(
    version="1.0.0",
    custom_checks={
        "database": check_database,
        "redis": check_redis,
        "disk": check_disk_space,
    },
)
```

### Custom Paths

```python
config = HealthConfig(
    health_path="/healthz",
    ready_path="/readiness",
    live_path="/liveness",
)
```

### Without Details

```python
config = HealthConfig(
    include_details=False,  # Only status, no uptime/version
)
```

Response:
```json
{
    "status": "healthy",
    "timestamp": "2024-01-01T00:00:00Z"
}
```

## Kubernetes Integration

### Pod Spec

```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: my-api
      image: my-api:latest
      ports:
        - containerPort: 8000
      
      livenessProbe:
        httpGet:
          path: /live
          port: 8000
        initialDelaySeconds: 10
        periodSeconds: 10
        failureThreshold: 3
      
      readinessProbe:
        httpGet:
          path: /ready
          port: 8000
        initialDelaySeconds: 5
        periodSeconds: 5
        failureThreshold: 3
      
      startupProbe:
        httpGet:
          path: /health
          port: 8000
        initialDelaySeconds: 0
        periodSeconds: 5
        failureThreshold: 30
```

### Probe Types

| Probe | Purpose | Endpoint |
|-------|---------|----------|
| `livenessProbe` | Restart if dead | `/live` |
| `readinessProbe` | Remove from load balancer if not ready | `/ready` |
| `startupProbe` | Wait for app to start | `/health` |

## Load Balancer Integration

### AWS ALB

```yaml
# Target Group Health Check
HealthCheckPath: /health
HealthCheckIntervalSeconds: 30
HealthyThresholdCount: 2
UnhealthyThresholdCount: 3
```

### Nginx

```nginx
upstream backend {
    server backend1:8000;
    server backend2:8000;
}

location /health {
    proxy_pass http://backend/health;
}
```

## Graceful Shutdown

The `/ready` endpoint can return 503 during shutdown:

```python
import signal

shutdown_flag = False

async def check_not_shutting_down() -> bool:
    return not shutdown_flag

config = HealthConfig(
    custom_checks={
        "accepting_traffic": check_not_shutting_down,
    },
)

def handle_sigterm(signum, frame):
    global shutdown_flag
    shutdown_flag = True
    # Allow 30 seconds for in-flight requests

signal.signal(signal.SIGTERM, handle_sigterm)
```

## Dependency Check Examples

### Database (PostgreSQL)

```python
import asyncpg

async def check_postgres() -> bool:
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        await conn.execute("SELECT 1")
        await conn.close()
        return True
    except Exception:
        return False
```

### Redis

```python
import redis.asyncio as redis

async def check_redis() -> bool:
    try:
        client = redis.from_url(REDIS_URL)
        await client.ping()
        await client.close()
        return True
    except Exception:
        return False
```

### External API

```python
import httpx

async def check_external_api() -> bool:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.example.com/health",
                timeout=5.0
            )
            return response.status_code == 200
    except Exception:
        return False
```

### Message Queue (RabbitMQ)

```python
import aio_pika

async def check_rabbitmq() -> bool:
    try:
        connection = await aio_pika.connect(RABBITMQ_URL)
        await connection.close()
        return True
    except Exception:
        return False
```

## Best Practices

1. **Keep liveness simple** - Just check if app is running
2. **Make readiness thorough** - Check all dependencies
3. **Don't block on slow checks** - Use timeouts
4. **Return 503 during shutdown** - Graceful termination
5. **Include version** - Helps debugging

## Related

- [MetricsMiddleware](metrics.md) - Prometheus metrics
- [MaintenanceMiddleware](maintenance.md) - Maintenance mode

