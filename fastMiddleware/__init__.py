"""
FastMVC Middleware - Production-ready middlewares for FastAPI applications.

A collection of battle-tested, configurable middleware components for building
robust FastAPI/Starlette applications with security, observability, and
rate limiting built-in.
"""

from fastMiddleware.base import FastMVCMiddleware
from fastMiddleware.cors import CORSMiddleware
from fastMiddleware.logging import LoggingMiddleware
from fastMiddleware.timing import TimingMiddleware
from fastMiddleware.request_id import RequestIDMiddleware
from fastMiddleware.security import SecurityHeadersMiddleware, SecurityHeadersConfig
from fastMiddleware.rate_limit import (
    RateLimitMiddleware,
    RateLimitConfig,
    RateLimitStore,
    InMemoryRateLimitStore,
)
from fastMiddleware.authentication import (
    AuthenticationMiddleware,
    AuthConfig,
    AuthBackend,
    JWTAuthBackend,
    APIKeyAuthBackend,
)
from fastMiddleware.request_context import (
    RequestContextMiddleware,
    get_request_id,
    get_request_context,
)
from fastMiddleware.compression import (
    CompressionMiddleware,
    CompressionConfig,
)
from fastMiddleware.trusted_host import TrustedHostMiddleware
from fastMiddleware.error_handler import (
    ErrorHandlerMiddleware,
    ErrorConfig,
)
from fastMiddleware.health import (
    HealthCheckMiddleware,
    HealthConfig,
)
from fastMiddleware.idempotency import (
    IdempotencyMiddleware,
    IdempotencyConfig,
    IdempotencyStore,
    InMemoryIdempotencyStore,
)
from fastMiddleware.cache import (
    CacheMiddleware,
    CacheConfig,
)
from fastMiddleware.metrics import (
    MetricsMiddleware,
    MetricsConfig,
    MetricsCollector,
)
from fastMiddleware.maintenance import (
    MaintenanceMiddleware,
    MaintenanceConfig,
)

__version__ = "0.2.0"
__author__ = "Shiv"
__license__ = "MIT"

__all__ = [
    # Base
    "FastMVCMiddleware",
    
    # Core Middlewares
    "CORSMiddleware",
    "LoggingMiddleware",
    "TimingMiddleware",
    "RequestIDMiddleware",
    "SecurityHeadersMiddleware",
    "SecurityHeadersConfig",
    
    # Rate Limiting
    "RateLimitMiddleware",
    "RateLimitConfig",
    "RateLimitStore",
    "InMemoryRateLimitStore",
    
    # Authentication
    "AuthenticationMiddleware",
    "AuthConfig",
    "AuthBackend",
    "JWTAuthBackend",
    "APIKeyAuthBackend",
    
    # Request Context
    "RequestContextMiddleware",
    "get_request_id",
    "get_request_context",
    
    # Compression
    "CompressionMiddleware",
    "CompressionConfig",
    
    # Trusted Host
    "TrustedHostMiddleware",
    
    # Error Handling
    "ErrorHandlerMiddleware",
    "ErrorConfig",
    
    # Health Checks
    "HealthCheckMiddleware",
    "HealthConfig",
    
    # Idempotency
    "IdempotencyMiddleware",
    "IdempotencyConfig",
    "IdempotencyStore",
    "InMemoryIdempotencyStore",
    
    # Caching
    "CacheMiddleware",
    "CacheConfig",
    
    # Metrics
    "MetricsMiddleware",
    "MetricsConfig",
    "MetricsCollector",
    
    # Maintenance Mode
    "MaintenanceMiddleware",
    "MaintenanceConfig",
]
