# Middleware Documentation

Complete reference for all 94 middlewares in FastMVC Middleware.

## Prerequisites

| Symbol | Meaning |
|--------|---------|
| ✅ | No additional dependencies (only `starlette`) |
| 🔑 | Requires `pip install fastmvc-middleware[jwt]` |
| 🌐 | Requires `pip install fastmvc-middleware[proxy]` |

## Middleware Index

### 🔒 Security (14)

| Middleware | Prerequisites | Description |
|------------|--------------|-------------|
| [SecurityHeadersMiddleware](security-headers.md) | ✅ | OWASP security headers |
| [CORSMiddleware](cors.md) | ✅ | Cross-Origin Resource Sharing |
| [CSRFMiddleware](csrf.md) | ✅ | CSRF protection |
| [HTTPSRedirectMiddleware](https-redirect.md) | ✅ | HTTP to HTTPS redirect |
| [IPFilterMiddleware](ip-filter.md) | ✅ | IP whitelist/blacklist |
| [TrustedHostMiddleware](trusted-host.md) | ✅ | Host header validation |
| [OriginMiddleware](origin.md) | ✅ | Origin header validation |
| [WebhookMiddleware](webhook.md) | ✅ | Webhook signature validation |
| [ReferrerPolicyMiddleware](referrer-policy.md) | ✅ | Referrer-Policy header |
| [PermissionsPolicyMiddleware](permissions-policy.md) | ✅ | Browser permissions |
| [CSPReportMiddleware](csp-report.md) | ✅ | CSP violation reports |
| [HoneypotMiddleware](honeypot.md) | ✅ | Honeypot traps |
| [SanitizationMiddleware](sanitization.md) | ✅ | Input sanitization |
| [ReplayPreventionMiddleware](replay-prevention.md) | ✅ | Replay attack prevention |
| [RequestSigningMiddleware](request-signing.md) | ✅ | HMAC request signing |

### 🔐 Authentication (6)

| Middleware | Prerequisites | Description |
|------------|--------------|-------------|
| [AuthenticationMiddleware](authentication.md) | 🔑 | JWT/API Key auth |
| [BasicAuthMiddleware](basic-auth.md) | ✅ | HTTP Basic auth |
| [BearerAuthMiddleware](bearer-auth.md) | ✅ | Bearer token auth |
| [ScopeMiddleware](scope.md) | ✅ | OAuth scope validation |
| [RouteAuthMiddleware](route-auth.md) | ✅ | Per-route auth |

### 📊 Observability (10)

| Middleware | Prerequisites | Description |
|------------|--------------|-------------|
| [LoggingMiddleware](logging.md) | ✅ | Request/response logging |
| [TimingMiddleware](timing.md) | ✅ | Response timing |
| [RequestIDMiddleware](request-id.md) | ✅ | Request ID generation |
| [RequestContextMiddleware](request-context.md) | ✅ | Async-safe context |
| [MetricsMiddleware](metrics.md) | ✅ | Prometheus metrics |
| [ProfilingMiddleware](profiling.md) | ✅ | Performance profiling |
| [AuditMiddleware](audit.md) | ✅ | Audit logging |
| [ServerTimingMiddleware](server-timing.md) | ✅ | Server-Timing header |
| [RequestLoggerMiddleware](request-logger.md) | ✅ | Access logging |
| [CostTrackingMiddleware](cost-tracking.md) | ✅ | Request cost tracking |
| [RequestSamplerMiddleware](request-sampler.md) | ✅ | Request sampling |

### 🛡️ Resilience (10)

| Middleware | Prerequisites | Description |
|------------|--------------|-------------|
| [RateLimitMiddleware](rate-limit.md) | ✅ | Rate limiting |
| [CircuitBreakerMiddleware](circuit-breaker.md) | ✅ | Circuit breaker |
| [BulkheadMiddleware](bulkhead.md) | ✅ | Bulkhead isolation |
| [LoadSheddingMiddleware](load-shedding.md) | ✅ | Load shedding |
| [TimeoutMiddleware](timeout.md) | ✅ | Request timeout |
| [ErrorHandlerMiddleware](error-handler.md) | ✅ | Error formatting |
| [ExceptionHandlerMiddleware](exception-handler.md) | ✅ | Exception handling |
| [GracefulShutdownMiddleware](graceful-shutdown.md) | ✅ | Graceful shutdown |
| [RequestDedupMiddleware](request-dedup.md) | ✅ | Request deduplication |
| [RequestCoalescingMiddleware](request-coalescing.md) | ✅ | Request coalescing |

### ⚡ Performance (10)

| Middleware | Prerequisites | Description |
|------------|--------------|-------------|
| [CompressionMiddleware](compression.md) | ✅ | GZip compression |
| [CacheMiddleware](cache.md) | ✅ | HTTP caching |
| [ETagMiddleware](etag.md) | ✅ | ETag generation |
| [ResponseCacheMiddleware](response-cache.md) | ✅ | In-memory cache |
| [BandwidthMiddleware](bandwidth.md) | ✅ | Bandwidth throttling |
| [NoCacheMiddleware](no-cache.md) | ✅ | Disable caching |
| [ConditionalRequestMiddleware](conditional-request.md) | ✅ | If-None-Match |
| [EarlyHintsMiddleware](early-hints.md) | ✅ | HTTP 103 hints |
| [ResponseSignatureMiddleware](response-signature.md) | ✅ | Response signing |

### 🔧 Operations (5)

| Middleware | Prerequisites | Description |
|------------|--------------|-------------|
| [HealthCheckMiddleware](health.md) | ✅ | Health endpoints |
| [MaintenanceMiddleware](maintenance.md) | ✅ | Maintenance mode |
| [WarmupMiddleware](warmup.md) | ✅ | Container warmup |
| [ChaosMiddleware](chaos.md) | ✅ | Chaos engineering |
| [SlowResponseMiddleware](slow-response.md) | ✅ | Artificial delays |

### 🌐 API Management (7)

| Middleware | Prerequisites | Description |
|------------|--------------|-------------|
| [VersioningMiddleware](versioning.md) | ✅ | API versioning |
| [DeprecationMiddleware](deprecation.md) | ✅ | Deprecation warnings |
| [RetryAfterMiddleware](retry-after.md) | ✅ | Retry-After headers |
| [APIVersionHeaderMiddleware](api-version-header.md) | ✅ | Version headers |
| [ContentNegotiationMiddleware](content-negotiation.md) | ✅ | Accept negotiation |
| [JSONSchemaMiddleware](json-schema.md) | ✅ | JSON Schema validation |
| [HATEOASMiddleware](hateoas.md) | ✅ | Hypermedia links |

### 👤 Detection (5)

| Middleware | Prerequisites | Description |
|------------|--------------|-------------|
| [BotDetectionMiddleware](bot-detection.md) | ✅ | Bot detection |
| [UserAgentMiddleware](user-agent.md) | ✅ | User-Agent parsing |
| [GeoIPMiddleware](geoip.md) | ✅ | GeoIP extraction |
| [ClientHintsMiddleware](client-hints.md) | ✅ | Client Hints |
| [RequestFingerprintMiddleware](request-fingerprint.md) | ✅ | Fingerprinting |

### 🧪 Testing (2)

| Middleware | Prerequisites | Description |
|------------|--------------|-------------|
| [FeatureFlagMiddleware](feature-flag.md) | ✅ | Feature flags |
| [ABTestMiddleware](ab-testing.md) | ✅ | A/B testing |

### 🌍 Localization (2)

| Middleware | Prerequisites | Description |
|------------|--------------|-------------|
| [LocaleMiddleware](locale.md) | ✅ | Locale detection |
| [AcceptLanguageMiddleware](accept-language.md) | ✅ | Language negotiation |

### 🔀 Routing (7)

| Middleware | Prerequisites | Description |
|------------|--------------|-------------|
| [RedirectMiddleware](redirect.md) | ✅ | URL redirects |
| [PathRewriteMiddleware](path-rewrite.md) | ✅ | Path rewriting |
| [ProxyMiddleware](proxy.md) | 🌐 | Reverse proxy |
| [MethodOverrideMiddleware](method-override.md) | ✅ | Method override |
| [TrailingSlashMiddleware](trailing-slash.md) | ✅ | Trailing slash |
| [HeaderTransformMiddleware](header-transform.md) | ✅ | Header transformation |
| [ContentTypeMiddleware](content-type.md) | ✅ | Content-Type validation |

### 🆔 Context (8)

| Middleware | Prerequisites | Description |
|------------|--------------|-------------|
| [SessionMiddleware](session.md) | ✅ | Server-side sessions |
| [TenantMiddleware](tenant.md) | ✅ | Multi-tenancy |
| [CorrelationMiddleware](correlation.md) | ✅ | Correlation IDs |
| [RequestIDPropagationMiddleware](request-id-propagation.md) | ✅ | ID propagation |
| [ContextMiddleware](context.md) | ✅ | Shared context |
| [RealIPMiddleware](real-ip.md) | ✅ | Real IP extraction |
| [XFFTrustMiddleware](xff-trust.md) | ✅ | XFF trust |

### 📄 Additional (8)

| Middleware | Prerequisites | Description |
|------------|--------------|-------------|
| [DataMaskingMiddleware](data-masking.md) | ✅ | Sensitive data masking |
| [QuotaMiddleware](quota.md) | ✅ | Usage quotas |
| [IdempotencyMiddleware](idempotency.md) | ✅ | Idempotency keys |
| [RequestLimitMiddleware](request-limit.md) | ✅ | Body size limits |
| [PayloadSizeMiddleware](payload-size.md) | ✅ | Payload limits |
| [RequestValidatorMiddleware](request-validator.md) | ✅ | Request validation |
| [ResponseTimeMiddleware](response-time.md) | ✅ | SLA monitoring |
| [RequestPriorityMiddleware](request-priority.md) | ✅ | Request priority |

## Common Patterns

### Recommended Middleware Order

```python
# Order: First added = Last executed (outermost to innermost)
app.add_middleware(CompressionMiddleware)      # 8. Compress response
app.add_middleware(ResponseTimeMiddleware)     # 7. Track timing
app.add_middleware(LoggingMiddleware)          # 6. Log request/response
app.add_middleware(ErrorHandlerMiddleware)     # 5. Handle errors
app.add_middleware(AuthenticationMiddleware)   # 4. Authenticate
app.add_middleware(RateLimitMiddleware)        # 3. Rate limit
app.add_middleware(SecurityHeadersMiddleware)  # 2. Add security headers
app.add_middleware(RequestIDMiddleware)        # 1. Generate request ID
```

### Excluding Paths

All middlewares support path exclusion:

```python
app.add_middleware(
    AuthenticationMiddleware,
    exclude_paths={"/health", "/login", "/public/*"},
)
```

### Configuration Objects

All middlewares support configuration via dataclasses:

```python
from fastMiddleware import RateLimitMiddleware, RateLimitConfig

config = RateLimitConfig(
    requests_per_minute=100,
    burst_size=10,
)
app.add_middleware(RateLimitMiddleware, config=config)
```

Or via keyword arguments:

```python
app.add_middleware(
    RateLimitMiddleware,
    requests_per_minute=100,
    burst_size=10,
)
```
