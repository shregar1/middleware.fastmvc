# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-01-17

### Added

- Initial release of FastMVC Middleware
- **CORSMiddleware**: Cross-origin resource sharing with sensible defaults
- **SecurityHeadersMiddleware**: Comprehensive security headers (CSP, HSTS, X-Frame-Options, etc.)
- **RateLimitMiddleware**: Sliding window rate limiting with configurable limits
- **AuthenticationMiddleware**: Pluggable authentication with JWT and API key backends
- **LoggingMiddleware**: Structured request/response logging
- **TimingMiddleware**: Request processing time tracking
- **RequestIDMiddleware**: Unique request identifier generation
- **RequestContextMiddleware**: Async-safe context variables for request tracking
- **FastMVCMiddleware**: Base class for creating custom middleware
- Comprehensive test suite
- Example applications
- Full documentation in README

### Features

- Python 3.10+ support
- Type hints throughout
- Fully async
- Zero required dependencies beyond Starlette
- Optional JWT support via PyJWT
- Configurable via dataclasses or keyword arguments
- Path and method exclusion support
- Standard rate limit headers (X-RateLimit-*)
- Standard security headers (OWASP recommended)
- Context variables for async-safe request tracking

[Unreleased]: https://github.com/hyyre/fastmvc-middleware/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/hyyre/fastmvc-middleware/releases/tag/v0.1.0

