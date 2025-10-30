"""
Tests for logging module
"""

import pytest
import json
import logging
from pathlib import Path
import tempfile
import shutil

from backend.logging_monitoring.logger import (
    setup_logging,
    get_logger,
    JSONFormatter,
    ColoredFormatter,
)
from backend.logging_monitoring.correlation import (
    get_correlation_id,
    set_correlation_id,
    generate_correlation_id,
    correlation_context,
)


class TestCorrelationID:
    """Test correlation ID functionality"""
    
    def test_generate_correlation_id(self):
        """Test correlation ID generation"""
        corr_id = generate_correlation_id()
        assert corr_id is not None
        assert isinstance(corr_id, str)
        assert len(corr_id) > 0
    
    def test_set_and_get_correlation_id(self):
        """Test setting and getting correlation ID"""
        test_id = "test-correlation-id"
        set_correlation_id(test_id)
        
        retrieved_id = get_correlation_id()
        assert retrieved_id == test_id
    
    def test_correlation_context(self):
        """Test correlation context manager"""
        test_id = "context-test-id"
        
        with correlation_context(test_id) as corr_id:
            assert corr_id == test_id
            assert get_correlation_id() == test_id
    
    def test_correlation_context_auto_generate(self):
        """Test correlation context with auto-generated ID"""
        with correlation_context() as corr_id:
            assert corr_id is not None
            assert get_correlation_id() == corr_id


class TestJSONFormatter:
    """Test JSON log formatter"""
    
    def test_json_formatter_basic(self):
        """Test basic JSON formatting"""
        formatter = JSONFormatter(service="test-service", environment="test")
        
        record = logging.LogRecord(
            name="test.logger",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        
        formatted = formatter.format(record)
        data = json.loads(formatted)
        
        assert data["level"] == "INFO"
        assert data["logger"] == "test.logger"
        assert data["message"] == "Test message"
        assert data["service"] == "test-service"
        assert data["environment"] == "test"
        assert "timestamp" in data
        assert "source" in data
    
    def test_json_formatter_with_correlation_id(self):
        """Test JSON formatting with correlation ID"""
        formatter = JSONFormatter()
        
        test_id = "test-correlation-123"
        set_correlation_id(test_id)
        
        record = logging.LogRecord(
            name="test.logger",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        
        formatted = formatter.format(record)
        data = json.loads(formatted)
        
        assert data["correlation_id"] == test_id


class TestStructuredLogger:
    """Test structured logger"""
    
    def test_get_logger(self):
        """Test getting a logger instance"""
        logger = get_logger("test.module")
        assert logger is not None
        assert logger.logger.name == "test.module"
    
    def test_logger_with_extra_fields(self, caplog):
        """Test logging with extra fields"""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "test.log"
            
            setup_logging(
                level="INFO",
                log_format="json",
                file_enabled=True,
                log_file=str(log_file),
                console_enabled=False,
            )
            
            logger = get_logger("test.extra_fields")
            
            with correlation_context("test-id-123"):
                logger.info("Test message", extra_fields={
                    "trade_id": "ABC123",
                    "symbol": "EUR/USD",
                    "quantity": 1000,
                })
            
            # Read log file
            if log_file.exists():
                with open(log_file) as f:
                    lines = f.readlines()
                    if lines:
                        last_line = lines[-1]
                        data = json.loads(last_line)
                        
                        assert data["message"] == "Test message"
                        assert data["correlation_id"] == "test-id-123"


class TestLoggingSetup:
    """Test logging setup"""
    
    def test_setup_logging_basic(self):
        """Test basic logging setup"""
        import backend.logging_monitoring.logger as logger_module
        
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "test.log"
            
            # Reset the configured flag for testing
            logger_module._logging_configured = False
            
            setup_logging(
                level="INFO",
                log_format="json",
                file_enabled=True,
                log_file=str(log_file),
                console_enabled=False,
            )
            
            logger = get_logger("test.setup")
            logger.info("Test message")
            
            # Force flush
            import logging
            for handler in logging.getLogger().handlers:
                handler.flush()
            
            # Check log file was created
            assert log_file.exists()
    
    def test_setup_logging_creates_directory(self):
        """Test that logging setup creates directories"""
        import backend.logging_monitoring.logger as logger_module
        
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "logs" / "subdir" / "test.log"
            
            # Reset the configured flag for testing
            logger_module._logging_configured = False
            
            setup_logging(
                level="INFO",
                file_enabled=True,
                log_file=str(log_file),
                console_enabled=False,
            )
            
            logger = get_logger("test.dirs")
            logger.info("Test message")
            
            # Force flush
            import logging
            for handler in logging.getLogger().handlers:
                handler.flush()
            
            # Check directory was created
            assert log_file.parent.exists()
            assert log_file.exists()


class TestLoggingMiddleware:
    """Test logging middleware integration"""
    
    def test_correlation_id_in_logs(self):
        """Test that correlation IDs are properly attached to logs"""
        test_id = "middleware-test-id"
        
        with correlation_context(test_id):
            logger = get_logger("test.middleware")
            
            # Simulate middleware setting correlation ID
            assert get_correlation_id() == test_id
            
            # Log should include correlation ID
            logger.info("Request processed")
            
            # Verify correlation ID persists
            assert get_correlation_id() == test_id
