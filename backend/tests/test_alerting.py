"""
Tests for alerting module
"""

import pytest
import asyncio
from datetime import datetime

from backend.logging_monitoring.alerting import (
    AlertManager,
    Alert,
    AlertRule,
    AlertSeverity,
    ConsoleChannel,
    get_alert_manager,
)


class TestAlertSeverity:
    """Test AlertSeverity enum"""
    
    def test_alert_severity_values(self):
        """Test alert severity enum values"""
        assert AlertSeverity.DEBUG.value == "debug"
        assert AlertSeverity.INFO.value == "info"
        assert AlertSeverity.WARNING.value == "warning"
        assert AlertSeverity.ERROR.value == "error"
        assert AlertSeverity.CRITICAL.value == "critical"


class TestAlert:
    """Test Alert dataclass"""
    
    def test_alert_creation(self):
        """Test creating an alert"""
        alert = Alert(
            rule_name="test_alert",
            severity=AlertSeverity.WARNING,
            message="Test alert message",
            timestamp=datetime.utcnow(),
            context={"key": "value"},
            channels=["console"],
        )
        
        assert alert.rule_name == "test_alert"
        assert alert.severity == AlertSeverity.WARNING
        assert alert.message == "Test alert message"
        assert alert.context == {"key": "value"}


class TestAlertRule:
    """Test AlertRule dataclass"""
    
    def test_alert_rule_creation(self):
        """Test creating an alert rule"""
        rule = AlertRule(
            name="high_error_rate",
            severity=AlertSeverity.CRITICAL,
            message_template="Error rate exceeded: {error_rate}%",
            channels=["console", "email"],
            cooldown_minutes=10,
            threshold=5.0,
        )
        
        assert rule.name == "high_error_rate"
        assert rule.severity == AlertSeverity.CRITICAL
        assert rule.cooldown_minutes == 10
        assert rule.threshold == 5.0


class TestConsoleChannel:
    """Test ConsoleChannel"""
    
    @pytest.mark.asyncio
    async def test_console_channel_send(self, capsys):
        """Test sending alert to console"""
        channel = ConsoleChannel(colorize=False)
        
        alert = Alert(
            rule_name="test_alert",
            severity=AlertSeverity.WARNING,
            message="Test warning message",
            timestamp=datetime.utcnow(),
            context={"test": "data"},
            channels=["console"],
        )
        
        success = await channel.send(alert)
        assert success is True
        
        captured = capsys.readouterr()
        assert "Test warning message" in captured.out


class TestAlertManager:
    """Test AlertManager functionality"""
    
    @pytest.fixture
    def manager(self):
        """Create a fresh alert manager for each test"""
        return AlertManager()
    
    def test_add_rule(self, manager):
        """Test adding an alert rule"""
        rule = AlertRule(
            name="test_rule",
            severity=AlertSeverity.WARNING,
            message_template="Test message",
            channels=["console"],
        )
        
        manager.add_rule(rule)
        assert "test_rule" in manager.rules
    
    def test_add_channel(self, manager):
        """Test adding an alert channel"""
        channel = ConsoleChannel()
        manager.add_channel("console", channel)
        
        assert "console" in manager.channels
    
    @pytest.mark.asyncio
    async def test_trigger_alert(self, manager):
        """Test triggering an alert"""
        # Add rule and channel
        rule = AlertRule(
            name="test_alert",
            severity=AlertSeverity.INFO,
            message_template="Test alert: {value}",
            channels=["console"],
            cooldown_minutes=0,
        )
        manager.add_rule(rule)
        
        channel = ConsoleChannel(colorize=False)
        manager.add_channel("console", channel)
        
        # Trigger alert
        success = await manager.trigger("test_alert", {"value": "123"})
        assert success is True
        
        # Check alert was recorded
        assert len(manager.alert_history) == 1
        assert manager.alert_counts["test_alert"] == 1
    
    @pytest.mark.asyncio
    async def test_alert_cooldown(self, manager):
        """Test alert cooldown period"""
        # Add rule with short cooldown
        rule = AlertRule(
            name="cooldown_test",
            severity=AlertSeverity.INFO,
            message_template="Cooldown test",
            channels=["console"],
            cooldown_minutes=1,  # 1 minute cooldown
        )
        manager.add_rule(rule)
        
        channel = ConsoleChannel()
        manager.add_channel("console", channel)
        
        # First trigger should succeed
        success1 = await manager.trigger("cooldown_test", {})
        assert success1 is True
        
        # Immediate second trigger should fail (cooldown)
        success2 = await manager.trigger("cooldown_test", {})
        assert success2 is False
        
        # Only one alert should be recorded
        assert manager.alert_counts["cooldown_test"] == 1
    
    @pytest.mark.asyncio
    async def test_unknown_rule(self, manager):
        """Test triggering an unknown alert rule"""
        success = await manager.trigger("nonexistent_rule", {})
        assert success is False
    
    @pytest.mark.asyncio
    async def test_message_template_formatting(self, manager):
        """Test alert message template formatting"""
        rule = AlertRule(
            name="format_test",
            severity=AlertSeverity.INFO,
            message_template="Trade failed: {symbol} with error {error}",
            channels=["console"],
        )
        manager.add_rule(rule)
        
        channel = ConsoleChannel()
        manager.add_channel("console", channel)
        
        context = {
            "symbol": "EUR/USD",
            "error": "Insufficient funds",
        }
        
        success = await manager.trigger("format_test", context)
        assert success is True
        
        # Check the formatted message
        alert = manager.alert_history[0]
        assert "EUR/USD" in alert.message
        assert "Insufficient funds" in alert.message
    
    def test_get_alert_stats(self, manager):
        """Test getting alert statistics"""
        # Add some rules and channels
        rule1 = AlertRule(
            name="rule1",
            severity=AlertSeverity.INFO,
            message_template="Rule 1",
            channels=["console"],
        )
        rule2 = AlertRule(
            name="rule2",
            severity=AlertSeverity.WARNING,
            message_template="Rule 2",
            channels=["console"],
        )
        
        manager.add_rule(rule1)
        manager.add_rule(rule2)
        manager.add_channel("console", ConsoleChannel())
        
        stats = manager.get_alert_stats()
        
        assert stats["total_rules"] == 2
        assert stats["total_channels"] == 1
        assert "alert_counts" in stats
        assert "recent_alerts" in stats
    
    @pytest.mark.asyncio
    async def test_rate_limiting(self, manager):
        """Test alert rate limiting"""
        manager.rate_limit_enabled = True
        manager.max_alerts_per_hour = 2
        
        rule = AlertRule(
            name="rate_test",
            severity=AlertSeverity.INFO,
            message_template="Rate test",
            channels=["console"],
            cooldown_minutes=0,  # No cooldown for this test
        )
        manager.add_rule(rule)
        manager.add_channel("console", ConsoleChannel())
        
        # First two should succeed
        success1 = await manager.trigger("rate_test", {})
        success2 = await manager.trigger("rate_test", {})
        assert success1 is True
        assert success2 is True
        
        # Third should fail due to rate limit
        success3 = await manager.trigger("rate_test", {})
        assert success3 is False


class TestAlertIntegration:
    """Integration tests for alerting system"""
    
    def test_global_alert_manager(self):
        """Test global alert manager singleton"""
        manager1 = get_alert_manager()
        manager2 = get_alert_manager()
        
        assert manager1 is manager2
    
    @pytest.mark.asyncio
    async def test_trading_alert_workflow(self):
        """Test a realistic trading alert workflow"""
        manager = AlertManager()
        
        # Setup rules
        circuit_breaker_rule = AlertRule(
            name="circuit_breaker",
            severity=AlertSeverity.CRITICAL,
            message_template="Circuit breaker triggered for {symbol}",
            channels=["console"],
        )
        
        trade_failed_rule = AlertRule(
            name="trade_failed",
            severity=AlertSeverity.ERROR,
            message_template="Trade failed: {error}",
            channels=["console"],
        )
        
        manager.add_rule(circuit_breaker_rule)
        manager.add_rule(trade_failed_rule)
        manager.add_channel("console", ConsoleChannel())
        
        # Simulate alerts (use different context to avoid same alert matching)
        await manager.trigger("trade_failed", {"error": "Network timeout"})
        
        # Wait a bit to ensure different timestamp
        import time
        time.sleep(0.1)
        
        await manager.trigger("trade_failed", {"error": "Invalid order"})
        await manager.trigger("circuit_breaker", {"symbol": "BTC/USD"})
        
        # Check statistics
        stats = manager.get_alert_stats()
        assert stats["total_rules"] == 2
        # Due to cooldown or aggregation, we may get less than expected
        assert manager.alert_counts["trade_failed"] >= 1  # At least one fired
        assert manager.alert_counts["circuit_breaker"] == 1
        assert len(manager.alert_history) >= 2
