"""
Security Headers Middleware for FastMVC.
"""

from typing import Callable, Awaitable

from starlette.requests import Request
from starlette.responses import Response

from middlewares.base import FastMVCMiddleware


class SecurityHeadersMiddleware(FastMVCMiddleware):
    """
    Middleware that adds security headers to all responses.
    
    Adds common security headers such as:
    - X-Content-Type-Options
    - X-Frame-Options
    - X-XSS-Protection
    - Strict-Transport-Security
    - Content-Security-Policy
    - Referrer-Policy
    - Permissions-Policy
    
    Example:
        ```python
        from fastapi import FastAPI
        from middlewares import SecurityHeadersMiddleware
        
        app = FastAPI()
        app.add_middleware(
            SecurityHeadersMiddleware,
            enable_hsts=True,
            content_security_policy="default-src 'self'"
        )
        ```
    """
    
    def __init__(
        self,
        app,
        x_content_type_options: str = "nosniff",
        x_frame_options: str = "DENY",
        x_xss_protection: str = "1; mode=block",
        enable_hsts: bool = False,
        hsts_max_age: int = 31536000,
        hsts_include_subdomains: bool = True,
        hsts_preload: bool = False,
        content_security_policy: str | None = None,
        referrer_policy: str = "strict-origin-when-cross-origin",
        permissions_policy: str | None = None,
    ) -> None:
        super().__init__(app)
        self.x_content_type_options = x_content_type_options
        self.x_frame_options = x_frame_options
        self.x_xss_protection = x_xss_protection
        self.enable_hsts = enable_hsts
        self.hsts_max_age = hsts_max_age
        self.hsts_include_subdomains = hsts_include_subdomains
        self.hsts_preload = hsts_preload
        self.content_security_policy = content_security_policy
        self.referrer_policy = referrer_policy
        self.permissions_policy = permissions_policy
    
    def _build_hsts_header(self) -> str:
        """Build the HSTS header value."""
        parts = [f"max-age={self.hsts_max_age}"]
        if self.hsts_include_subdomains:
            parts.append("includeSubDomains")
        if self.hsts_preload:
            parts.append("preload")
        return "; ".join(parts)
    
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        response = await call_next(request)
        
        # Add security headers
        if self.x_content_type_options:
            response.headers["X-Content-Type-Options"] = self.x_content_type_options
        
        if self.x_frame_options:
            response.headers["X-Frame-Options"] = self.x_frame_options
        
        if self.x_xss_protection:
            response.headers["X-XSS-Protection"] = self.x_xss_protection
        
        if self.enable_hsts:
            response.headers["Strict-Transport-Security"] = self._build_hsts_header()
        
        if self.content_security_policy:
            response.headers["Content-Security-Policy"] = self.content_security_policy
        
        if self.referrer_policy:
            response.headers["Referrer-Policy"] = self.referrer_policy
        
        if self.permissions_policy:
            response.headers["Permissions-Policy"] = self.permissions_policy
        
        return response

