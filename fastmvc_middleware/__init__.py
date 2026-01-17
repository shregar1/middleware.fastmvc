"""
FastMVC Middleware - Production-ready middlewares for FastAPI applications.

A collection of battle-tested, configurable middleware components for building
robust FastAPI/Starlette applications with security, observability, and
rate limiting built-in.
"""

from fastmvc_middleware.base import FastMVCMiddleware
from fastmvc_middleware.cors import CORSMiddleware
from fastmvc_middleware.logging import LoggingMiddleware
from fastmvc_middleware.timing import TimingMiddleware
from fastmvc_middleware.request_id import RequestIDMiddleware
from fastmvc_middleware.security import SecurityHeadersMiddleware, SecurityHeadersConfig
from fastmvc_middleware.rate_limit import (
    RateLimitMiddleware,
    RateLimitConfig,
    RateLimitStore,
    InMemoryRateLimitStore,
)
from fastmvc_middleware.authentication import (
    AuthenticationMiddleware,
    AuthConfig,
    JWTAuthBackend,
    APIKeyAuthBackend,
)
from fastmvc_middleware.request_context import (
    RequestContextMiddleware,
    get_request_id,
    get_request_context,
)

__version__ = "0.1.0"
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
    "JWTAuthBackend",
    "APIKeyAuthBackend",
    # Request Context
    "RequestContextMiddleware",
    "get_request_id",
    "get_request_context",
]
