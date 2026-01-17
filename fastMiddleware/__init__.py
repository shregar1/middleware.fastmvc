"""
FastMVC Middleware - Production-ready middlewares for FastAPI applications.

A collection of battle-tested, configurable middleware components for building
robust FastAPI/Starlette applications with security, observability, and
rate limiting built-in.
"""

from fastMiddleware.base import FastMVCMiddleware

# Core Middlewares
from fastMiddleware.cors import CORSMiddleware
from fastMiddleware.logging import LoggingMiddleware
from fastMiddleware.timing import TimingMiddleware
from fastMiddleware.request_id import RequestIDMiddleware

# Security
from fastMiddleware.security import SecurityHeadersMiddleware, SecurityHeadersConfig
from fastMiddleware.trusted_host import TrustedHostMiddleware
from fastMiddleware.csrf import CSRFMiddleware, CSRFConfig
from fastMiddleware.https_redirect import HTTPSRedirectMiddleware, HTTPSRedirectConfig
from fastMiddleware.ip_filter import IPFilterMiddleware, IPFilterConfig

# Rate Limiting
from fastMiddleware.rate_limit import (
    RateLimitMiddleware,
    RateLimitConfig,
    RateLimitStore,
    InMemoryRateLimitStore,
)

# Authentication & Authorization
from fastMiddleware.authentication import (
    AuthenticationMiddleware,
    AuthConfig,
    AuthBackend,
    JWTAuthBackend,
    APIKeyAuthBackend,
)

# Request Context
from fastMiddleware.request_context import (
    RequestContextMiddleware,
    get_request_id,
    get_request_context,
)
from fastMiddleware.correlation import (
    CorrelationMiddleware,
    CorrelationConfig,
    get_correlation_id,
)

# Session Management
from fastMiddleware.session import (
    SessionMiddleware,
    SessionConfig,
    SessionStore,
    InMemorySessionStore,
    Session,
)

# Response Handling
from fastMiddleware.compression import CompressionMiddleware, CompressionConfig
from fastMiddleware.response_format import ResponseFormatMiddleware, ResponseFormatConfig
from fastMiddleware.cache import CacheMiddleware, CacheConfig

# Error Handling
from fastMiddleware.error_handler import ErrorHandlerMiddleware, ErrorConfig
from fastMiddleware.circuit_breaker import CircuitBreakerMiddleware, CircuitBreakerConfig, CircuitState

# Health & Monitoring
from fastMiddleware.health import HealthCheckMiddleware, HealthConfig
from fastMiddleware.metrics import MetricsMiddleware, MetricsConfig, MetricsCollector
from fastMiddleware.profiling import ProfilingMiddleware, ProfilingConfig

# Idempotency
from fastMiddleware.idempotency import (
    IdempotencyMiddleware,
    IdempotencyConfig,
    IdempotencyStore,
    InMemoryIdempotencyStore,
)

# Maintenance
from fastMiddleware.maintenance import MaintenanceMiddleware, MaintenanceConfig

# Request Processing
from fastMiddleware.timeout import TimeoutMiddleware, TimeoutConfig
from fastMiddleware.request_limit import RequestLimitMiddleware, RequestLimitConfig
from fastMiddleware.trailing_slash import TrailingSlashMiddleware, TrailingSlashConfig, SlashAction
from fastMiddleware.content_type import ContentTypeMiddleware, ContentTypeConfig

# API Management
from fastMiddleware.versioning import (
    VersioningMiddleware,
    VersioningConfig,
    VersionLocation,
    get_api_version,
)
from fastMiddleware.deprecation import DeprecationMiddleware, DeprecationConfig, DeprecationInfo
from fastMiddleware.retry_after import RetryAfterMiddleware, RetryAfterConfig

# Detection & Analytics
from fastMiddleware.bot_detection import BotDetectionMiddleware, BotConfig, BotAction
from fastMiddleware.geoip import GeoIPMiddleware, GeoIPConfig, get_geo_data

# Feature Management
from fastMiddleware.feature_flag import (
    FeatureFlagMiddleware,
    FeatureFlagConfig,
    get_feature_flags,
    is_feature_enabled,
)

__version__ = "0.3.0"
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
    
    # Security
    "SecurityHeadersMiddleware",
    "SecurityHeadersConfig",
    "TrustedHostMiddleware",
    "CSRFMiddleware",
    "CSRFConfig",
    "HTTPSRedirectMiddleware",
    "HTTPSRedirectConfig",
    "IPFilterMiddleware",
    "IPFilterConfig",
    
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
    "CorrelationMiddleware",
    "CorrelationConfig",
    "get_correlation_id",
    
    # Session Management
    "SessionMiddleware",
    "SessionConfig",
    "SessionStore",
    "InMemorySessionStore",
    "Session",
    
    # Response Handling
    "CompressionMiddleware",
    "CompressionConfig",
    "ResponseFormatMiddleware",
    "ResponseFormatConfig",
    "CacheMiddleware",
    "CacheConfig",
    
    # Error Handling
    "ErrorHandlerMiddleware",
    "ErrorConfig",
    "CircuitBreakerMiddleware",
    "CircuitBreakerConfig",
    "CircuitState",
    
    # Health & Monitoring
    "HealthCheckMiddleware",
    "HealthConfig",
    "MetricsMiddleware",
    "MetricsConfig",
    "MetricsCollector",
    "ProfilingMiddleware",
    "ProfilingConfig",
    
    # Idempotency
    "IdempotencyMiddleware",
    "IdempotencyConfig",
    "IdempotencyStore",
    "InMemoryIdempotencyStore",
    
    # Maintenance
    "MaintenanceMiddleware",
    "MaintenanceConfig",
    
    # Request Processing
    "TimeoutMiddleware",
    "TimeoutConfig",
    "RequestLimitMiddleware",
    "RequestLimitConfig",
    "TrailingSlashMiddleware",
    "TrailingSlashConfig",
    "SlashAction",
    "ContentTypeMiddleware",
    "ContentTypeConfig",
    
    # API Management
    "VersioningMiddleware",
    "VersioningConfig",
    "VersionLocation",
    "get_api_version",
    "DeprecationMiddleware",
    "DeprecationConfig",
    "DeprecationInfo",
    "RetryAfterMiddleware",
    "RetryAfterConfig",
    
    # Detection & Analytics
    "BotDetectionMiddleware",
    "BotConfig",
    "BotAction",
    "GeoIPMiddleware",
    "GeoIPConfig",
    "get_geo_data",
    
    # Feature Management
    "FeatureFlagMiddleware",
    "FeatureFlagConfig",
    "get_feature_flags",
    "is_feature_enabled",
]
