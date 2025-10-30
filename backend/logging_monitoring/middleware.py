"""
FastAPI middleware for logging and metrics
"""

import time
from typing import Callable
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from .correlation import set_correlation_id, generate_correlation_id, get_correlation_id
from .logger import get_logger
from .metrics import get_metrics_tracker

logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware that adds structured logging to all requests
    
    - Generates/propagates correlation IDs
    - Logs request/response with timing
    - Captures exceptions
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate or extract correlation ID
        correlation_id = request.headers.get("X-Correlation-ID")
        if not correlation_id:
            correlation_id = generate_correlation_id()
        
        set_correlation_id(correlation_id)
        
        # Record request start
        start_time = time.time()
        
        # Log incoming request
        logger.info(
            f"Request started: {request.method} {request.url.path}",
            extra_fields={
                "method": request.method,
                "path": request.url.path,
                "query_params": dict(request.query_params),
                "client_host": request.client.host if request.client else None,
            }
        )
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Log response
            logger.info(
                f"Request completed: {request.method} {request.url.path}",
                extra_fields={
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration_ms": round(duration * 1000, 2),
                }
            )
            
            # Add correlation ID to response headers
            response.headers["X-Correlation-ID"] = correlation_id
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            
            logger.error(
                f"Request failed: {request.method} {request.url.path}",
                extra_fields={
                    "method": request.method,
                    "path": request.url.path,
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "duration_ms": round(duration * 1000, 2),
                },
                exc_info=True,
            )
            
            # Return error response
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal server error",
                    "correlation_id": correlation_id,
                },
                headers={"X-Correlation-ID": correlation_id},
            )


class MetricsMiddleware(BaseHTTPMiddleware):
    """
    Middleware that collects metrics for all requests
    
    - Records request counts
    - Tracks request duration
    - Counts errors
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip metrics endpoint to avoid recursion
        if request.url.path == "/api/metrics":
            return await call_next(request)
        
        start_time = time.time()
        metrics = get_metrics_tracker()
        
        # Increment request counter
        metrics.increment_counter(
            "api_requests_total",
            labels={
                "method": request.method,
                "path": request.url.path,
            }
        )
        
        try:
            response = await call_next(request)
            duration = time.time() - start_time
            
            # Record request duration
            metrics.record_duration(
                "api_request_duration_seconds",
                duration,
                labels={
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": str(response.status_code),
                }
            )
            
            # Track slow requests
            if duration > 1.0:  # More than 1 second
                logger.warning(
                    "Slow request detected",
                    extra_fields={
                        "method": request.method,
                        "path": request.url.path,
                        "duration_ms": round(duration * 1000, 2),
                    }
                )
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            
            # Increment error counter
            metrics.increment_counter(
                "api_errors_total",
                labels={
                    "method": request.method,
                    "path": request.url.path,
                    "error_type": type(e).__name__,
                }
            )
            
            # Record failed request duration
            metrics.record_duration(
                "api_request_duration_seconds",
                duration,
                labels={
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": "500",
                }
            )
            
            raise
