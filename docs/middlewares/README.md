# Middleware Documentation

Complete documentation for all 94+ middlewares in FastMVC Middleware.

## 📚 Documentation Index

### Core Middlewares

- [CORSMiddleware](cors.md) - Cross-Origin Resource Sharing

- [LoggingMiddleware](logging.md) - Structured request/response logging

- [TimingMiddleware](timing.md) - Response timing headers

- [RequestIDMiddleware](request-id.md) - Unique request ID generation

### Security

- [SecurityHeadersMiddleware](security-headers.md) - OWASP security headers

- [CSRFMiddleware](csrf.md) - CSRF protection

- [HTTPSRedirectMiddleware](https-redirect.md) - HTTP to HTTPS redirect

- [IPFilterMiddleware](ip-filter.md) - IP whitelist/blacklist

- [TrustedHostMiddleware](trusted-host.md) - Host header validation

- [OriginMiddleware](origin.md) - Origin header validation

- [WebhookMiddleware](webhook.md) - Webhook signature validation

- [ReferrerPolicyMiddleware](referrer-policy.md) - Referrer-Policy header

- [PermissionsPolicyMiddleware](permissions-policy.md) - Feature permissions

- [CSPReportMiddleware](csp-report.md) - CSP violation reports

- [HoneypotMiddleware](honeypot.md) - Trap malicious requests

- [SanitizationMiddleware](sanitization.md) - Input sanitization

- [ReplayPreventionMiddleware](replay-prevention.md) - Prevent replay attacks

- [RequestSigningMiddleware](request-signing.md) - HMAC signature validation

- [ResponseSignatureMiddleware](response-signature.md) - Sign responses

### Rate Limiting & Protection

- [RateLimitMiddleware](rate-limit.md) - Request rate limiting

- [QuotaMiddleware](quota.md) - Usage quota enforcement

- [LoadSheddingMiddleware](load-shedding.md) - Load shedding

- [BulkheadMiddleware](bulkhead.md) - Bulkhead pattern

- [RequestDedupMiddleware](request-dedup.md) - Request deduplication

- [RequestCoalescingMiddleware](request-coalescing.md) - Request coalescing

### Authentication & Authorization

- [AuthenticationMiddleware](authentication.md) - JWT/API key auth

- [BasicAuthMiddleware](basic-auth.md) - HTTP Basic auth

- [BearerAuthMiddleware](bearer-auth.md) - Bearer token auth

- [ScopeMiddleware](scope.md) - OAuth scope validation

- [RouteAuthMiddleware](route-auth.md) - Per-route auth rules

### Session & Context

- [SessionMiddleware](session.md) - Server-side sessions

- [RequestContextMiddleware](request-context.md) - Request context

- [CorrelationMiddleware](correlation.md) - Correlation IDs

- [TenantMiddleware](tenant.md) - Multi-tenancy

- [ContextMiddleware](context.md) - Shared context values

- [RequestIDPropagationMiddleware](request-id-propagation.md) - ID propagation

- [RealIPMiddleware](real-ip.md) - Extract real IP

- [XFFTrustMiddleware](xff-trust.md) - X-Forwarded-For handling

### Response Handling

- [CompressionMiddleware](compression.md) - GZip compression

- [CacheMiddleware](cache.md) - HTTP caching headers

- [ETagMiddleware](etag.md) - ETag generation

- [ResponseCacheMiddleware](response-cache.md) - In-memory caching

- [ResponseFormatMiddleware](response-format.md) - Response formatting

- [DataMaskingMiddleware](data-masking.md) - Mask sensitive data

- [HATEOASMiddleware](hateoas.md) - Hypermedia links

- [BandwidthMiddleware](bandwidth.md) - Bandwidth throttling

- [NoCacheMiddleware](no-cache.md) - Disable caching

- [ConditionalRequestMiddleware](conditional-request.md) - 304 handling

- [EarlyHintsMiddleware](early-hints.md) - HTTP 103 Early Hints

### Error Handling

- [ErrorHandlerMiddleware](error-handler.md) - Error formatting

- [ExceptionHandlerMiddleware](exception-handler.md) - Custom handlers

- [CircuitBreakerMiddleware](circuit-breaker.md) - Circuit breaker

### Health & Monitoring

- [HealthCheckMiddleware](health.md) - Health endpoints

- [MetricsMiddleware](metrics.md) - Prometheus metrics

- [ProfilingMiddleware](profiling.md) - Request profiling

- [AuditMiddleware](audit.md) - Audit logging

- [ServerTimingMiddleware](server-timing.md) - Server-Timing header

- [RequestLoggerMiddleware](request-logger.md) - Access logging

- [ResponseTimeMiddleware](response-time.md) - SLA monitoring

- [CostTrackingMiddleware](cost-tracking.md) - Request cost tracking

- [RequestSamplerMiddleware](request-sampler.md) - Request sampling

### Idempotency

- [IdempotencyMiddleware](idempotency.md) - Idempotency keys

### Maintenance & Lifecycle

- [MaintenanceMiddleware](maintenance.md) - Maintenance mode

- [WarmupMiddleware](warmup.md) - Container warmup

- [GracefulShutdownMiddleware](graceful-shutdown.md) - Graceful shutdown

- [ChaosMiddleware](chaos.md) - Chaos engineering

- [SlowResponseMiddleware](slow-response.md) - Artificial delays

### Request Processing

- [TimeoutMiddleware](timeout.md) - Request timeouts

- [RequestLimitMiddleware](request-limit.md) - Body size limits

- [PayloadSizeMiddleware](payload-size.md) - Request/response limits

- [ContentTypeMiddleware](content-type.md) - Content-Type validation

- [RequestValidatorMiddleware](request-validator.md) - Request validation

- [JSONSchemaMiddleware](json-schema.md) - JSON Schema validation

- [TrailingSlashMiddleware](trailing-slash.md) - Trailing slash handling

- [MethodOverrideMiddleware](method-override.md) - HTTP method override

- [HeaderTransformMiddleware](header-transform.md) - Header transformation

- [RequestFingerprintMiddleware](request-fingerprint.md) - Request fingerprints

- [RequestPriorityMiddleware](request-priority.md) - Request prioritization

### Routing

- [RedirectMiddleware](redirect.md) - URL redirects

- [PathRewriteMiddleware](path-rewrite.md) - Path rewriting

- [ProxyMiddleware](proxy.md) - Reverse proxy

### API Management

- [VersioningMiddleware](versioning.md) - API versioning

- [DeprecationMiddleware](deprecation.md) - Deprecation warnings

- [RetryAfterMiddleware](retry-after.md) - Retry-After headers

- [APIVersionHeaderMiddleware](api-version-header.md) - Version headers

- [ContentNegotiationMiddleware](content-negotiation.md) - Content negotiation

### Detection & Analytics

- [BotDetectionMiddleware](bot-detection.md) - Bot detection

- [UserAgentMiddleware](user-agent.md) - User-Agent parsing

- [GeoIPMiddleware](geoip.md) - GeoIP detection

- [ClientHintsMiddleware](client-hints.md) - Client hints

### Feature Management

- [FeatureFlagMiddleware](feature-flag.md) - Feature flags

- [ABTestMiddleware](ab-testing.md) - A/B testing

### Localization

- [LocaleMiddleware](locale.md) - Locale detection

- [AcceptLanguageMiddleware](accept-language.md) - Language negotiation

## 🚀 Quick Links

- [Main README](../../README.md)
- [API Reference](../API.md)
- [Examples](../EXAMPLES.md)
- [Contributing](../../CONTRIBUTING.md)
