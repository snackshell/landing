"""
Centralized logging module with structured JSON logging
"""

import logging
import sys
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
from logging.handlers import RotatingFileHandler

from .correlation import get_correlation_id


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""
    
    def __init__(self, service: str = "selamai", environment: str = "development"):
        super().__init__()
        self.service = service
        self.environment = environment
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "service": self.service,
            "environment": self.environment,
        }
        
        # Add correlation ID if available
        correlation_id = get_correlation_id()
        if correlation_id:
            log_data["correlation_id"] = correlation_id
        
        # Add extra fields
        if hasattr(record, "extra_fields"):
            log_data.update(record.extra_fields)
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add source location
        log_data["source"] = {
            "file": record.filename,
            "line": record.lineno,
            "function": record.funcName,
        }
        
        return json.dumps(log_data)


class ColoredFormatter(logging.Formatter):
    """Colored console formatter for better readability"""
    
    COLORS = {
        "DEBUG": "\033[36m",      # Cyan
        "INFO": "\033[32m",       # Green
        "WARNING": "\033[33m",    # Yellow
        "ERROR": "\033[31m",      # Red
        "CRITICAL": "\033[35m",   # Magenta
        "RESET": "\033[0m",       # Reset
    }
    
    def format(self, record: logging.LogRecord) -> str:
        """Format with colors"""
        color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        reset = self.COLORS["RESET"]
        
        # Add correlation ID to message if available
        correlation_id = get_correlation_id()
        corr_str = f" [CID: {correlation_id[:8]}]" if correlation_id else ""
        
        formatted = f"{color}[{record.levelname}]{reset} {record.name}{corr_str}: {record.getMessage()}"
        
        if record.exc_info:
            formatted += "\n" + self.formatException(record.exc_info)
        
        return formatted


class StructuredLogger(logging.LoggerAdapter):
    """Logger adapter that supports structured logging with extra fields"""
    
    def process(self, msg: str, kwargs: Dict[str, Any]) -> tuple:
        """Process log message and add extra fields"""
        # Extract extra fields
        extra_fields = kwargs.pop("extra_fields", {})
        
        # Merge with existing extra
        if "extra" not in kwargs:
            kwargs["extra"] = {}
        kwargs["extra"]["extra_fields"] = extra_fields
        
        return msg, kwargs


_loggers: Dict[str, StructuredLogger] = {}
_logging_configured = False


def setup_logging(
    level: str = "INFO",
    log_format: str = "json",
    console_enabled: bool = True,
    file_enabled: bool = True,
    log_file: str = "logs/selamai.log",
    error_log_file: str = "logs/errors.log",
    max_bytes: int = 10485760,  # 10MB
    backup_count: int = 10,
    service: str = "selamai",
    environment: Optional[str] = None,
) -> None:
    """
    Setup centralized logging configuration
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Format type (json or text)
        console_enabled: Enable console logging
        file_enabled: Enable file logging
        log_file: Path to main log file
        error_log_file: Path to error log file
        max_bytes: Max file size before rotation
        backup_count: Number of backup files to keep
        service: Service name for structured logging
        environment: Environment name (development, staging, production)
    """
    global _logging_configured
    
    if _logging_configured:
        return
    
    if environment is None:
        environment = os.getenv("ENVIRONMENT", "development")
    
    # Create logs directory if it doesn't exist
    if file_enabled:
        log_dir = Path(log_file).parent
        log_dir.mkdir(parents=True, exist_ok=True)
        error_log_dir = Path(error_log_file).parent
        error_log_dir.mkdir(parents=True, exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))
    
    # Remove existing handlers
    root_logger.handlers = []
    
    # Console handler
    if console_enabled:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, level.upper()))
        
        if log_format == "json":
            console_formatter = JSONFormatter(service=service, environment=environment)
        else:
            console_formatter = ColoredFormatter()
        
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)
    
    # File handler (all logs)
    if file_enabled:
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = JSONFormatter(service=service, environment=environment)
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
        
        # Error file handler (errors only)
        error_handler = RotatingFileHandler(
            error_log_file,
            maxBytes=max_bytes,
            backupCount=backup_count // 2,
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_formatter)
        root_logger.addHandler(error_handler)
    
    _logging_configured = True


def get_logger(name: str) -> StructuredLogger:
    """
    Get a structured logger instance
    
    Args:
        name: Logger name (typically __name__)
    
    Returns:
        StructuredLogger instance
    
    Example:
        logger = get_logger(__name__)
        logger.info("Trade executed", extra_fields={
            "trade_id": "123",
            "symbol": "EUR/USD",
            "quantity": 1000,
        })
    """
    if name not in _loggers:
        base_logger = logging.getLogger(name)
        _loggers[name] = StructuredLogger(base_logger, {})
    
    return _loggers[name]


# Default logger
logger = get_logger("selamai")
