"""
Correlation ID management for request tracing
"""

import uuid
from contextvars import ContextVar
from typing import Optional
from contextlib import contextmanager

# Context variable for storing correlation ID
_correlation_id: ContextVar[Optional[str]] = ContextVar("correlation_id", default=None)


def generate_correlation_id() -> str:
    """Generate a new correlation ID"""
    return str(uuid.uuid4())


def get_correlation_id() -> Optional[str]:
    """Get the current correlation ID from context"""
    return _correlation_id.get()


def set_correlation_id(correlation_id: str) -> None:
    """Set the correlation ID in context"""
    _correlation_id.set(correlation_id)


def ensure_correlation_id() -> str:
    """Ensure a correlation ID exists, create one if not"""
    corr_id = get_correlation_id()
    if not corr_id:
        corr_id = generate_correlation_id()
        set_correlation_id(corr_id)
    return corr_id


@contextmanager
def correlation_context(correlation_id: Optional[str] = None):
    """
    Context manager for correlation ID
    
    Usage:
        with correlation_context("my-correlation-id"):
            # All logs within this context will have the correlation ID
            logger.info("Processing request")
    """
    if correlation_id is None:
        correlation_id = generate_correlation_id()
    
    token = _correlation_id.set(correlation_id)
    try:
        yield correlation_id
    finally:
        _correlation_id.reset(token)
