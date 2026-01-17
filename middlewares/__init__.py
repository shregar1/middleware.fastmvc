"""
FastMVC Middleware - A collection of middlewares for FastAPI/FastMVC applications.
"""

from middlewares.cors import CORSMiddleware
from middlewares.logging import LoggingMiddleware
from middlewares.timing import TimingMiddleware
from middlewares.request_id import RequestIDMiddleware
from middlewares.security import SecurityHeadersMiddleware

__version__ = "0.1.0"
__all__ = [
    "CORSMiddleware",
    "LoggingMiddleware",
    "TimingMiddleware",
    "RequestIDMiddleware",
    "SecurityHeadersMiddleware",
]

