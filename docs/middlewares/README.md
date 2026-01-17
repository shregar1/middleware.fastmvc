# Middleware Documentation

Individual documentation for each middleware component.

## Security & Authentication

| Middleware | Description |
|------------|-------------|
| [SecurityHeadersMiddleware](./security-headers.md) | XSS, clickjacking protection |
| [TrustedHostMiddleware](./trusted-host.md) | Host header validation |
| [CORSMiddleware](./cors.md) | Cross-origin resource sharing |
| [AuthenticationMiddleware](./authentication.md) | JWT & API key auth |

## Observability

| Middleware | Description |
|------------|-------------|
| [LoggingMiddleware](./logging.md) | Request/response logging |
| [TimingMiddleware](./timing.md) | Processing time tracking |
| [RequestIDMiddleware](./request-id.md) | Unique request IDs |
| [RequestContextMiddleware](./request-context.md) | Async-safe context |
| [MetricsMiddleware](./metrics.md) | Prometheus metrics |

## Resilience

| Middleware | Description |
|------------|-------------|
| [RateLimitMiddleware](./rate-limit.md) | Rate limiting |
| [ErrorHandlerMiddleware](./error-handler.md) | Error formatting |
| [IdempotencyMiddleware](./idempotency.md) | Safe retries |

## Performance

| Middleware | Description |
|------------|-------------|
| [CompressionMiddleware](./compression.md) | GZip compression |
| [CacheMiddleware](./cache.md) | HTTP caching & ETags |

## Operations

| Middleware | Description |
|------------|-------------|
| [HealthCheckMiddleware](./health.md) | Health endpoints |
| [MaintenanceMiddleware](./maintenance.md) | Maintenance mode |

## Middleware Order

```python
# Recommended order (first added = last executed)
app.add_middleware(CompressionMiddleware)
app.add_middleware(TimingMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(CacheMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(IdempotencyMiddleware)
app.add_middleware(AuthenticationMiddleware)
app.add_middleware(RequestContextMiddleware)
app.add_middleware(HealthCheckMiddleware)
app.add_middleware(MetricsMiddleware)
app.add_middleware(TrustedHostMiddleware)
app.add_middleware(CORSMiddleware)
```

