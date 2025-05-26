"""
Rate limiting middleware for API protection.
"""
import time
from collections import defaultdict
from typing import Dict, Tuple, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

class RateLimiter(BaseHTTPMiddleware):
    """
    Rate limiting middleware for FastAPI.
    Limits requests by IP address.
    """
    
    def __init__(
        self,
        app: ASGIApp,
        requests_limit: int = 100,
        window_seconds: int = 60,
        block_duration_seconds: int = 300
    ):
        super().__init__(app)
        self.requests_limit = requests_limit
        self.window_seconds = window_seconds
        self.block_duration_seconds = block_duration_seconds
        self.ips: Dict[str, Dict[str, int]] = defaultdict(dict)
    
    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        ip = request.client.host
        path = request.url.path
        
        # Exclude auth endpoints from rate limiting
        if path.startswith("/api/auth"):
            return await call_next(request)
        
        current_time = int(time.time())
        
        # Check if IP is currently blocked
        if self.is_blocked(ip, current_time):
            return Response(
                content="Rate limit exceeded. Too many requests.",
                status_code=429
            )
        
        # Record request
        self.record_request(ip, current_time)
        
        # Check if request limit is exceeded
        if self.is_rate_limited(ip, current_time):
            self.block_ip(ip, current_time)
            return Response(
                content="Rate limit exceeded. Too many requests.",
                status_code=429
            )
        
        return await call_next(request)
    
    def is_blocked(self, ip: str, current_time: int) -> bool:
        """Check if an IP is currently blocked."""
        if ip not in self.ips:
            return False
        
        block_until = self.ips[ip].get("block_until", 0)
        if block_until > current_time:
            return True
        
        return False
    
    def block_ip(self, ip: str, current_time: int) -> None:
        """Block an IP for the configured duration."""
        self.ips[ip]["block_until"] = current_time + self.block_duration_seconds
    
    def record_request(self, ip: str, current_time: int) -> None:
        """Record a request from an IP."""
        if "requests" not in self.ips[ip]:
            self.ips[ip]["requests"] = []
        
        # Add current request timestamp
        self.ips[ip]["requests"].append(current_time)
        
        # Remove requests older than the window
        window_start = current_time - self.window_seconds
        self.ips[ip]["requests"] = [
            timestamp for timestamp in self.ips[ip]["requests"]
            if timestamp > window_start
        ]
    
    def is_rate_limited(self, ip: str, current_time: int) -> bool:
        """Check if the request limit for an IP is exceeded."""
        return len(self.ips[ip].get("requests", [])) > self.requests_limit
