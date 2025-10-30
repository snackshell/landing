"""
Alerting system for critical events and threshold violations
"""

import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from dataclasses import dataclass, asdict
import json
from collections import defaultdict
import aiohttp

from .logger import get_logger

logger = get_logger(__name__)


class AlertSeverity(Enum):
    """Alert severity levels"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class Alert:
    """Represents an alert event"""
    rule_name: str
    severity: AlertSeverity
    message: str
    timestamp: datetime
    context: Dict[str, Any]
    channels: List[str]


@dataclass
class AlertRule:
    """Alert rule configuration"""
    name: str
    severity: AlertSeverity
    message_template: str
    channels: List[str]
    cooldown_minutes: int = 5
    threshold: Optional[float] = None
    window_minutes: Optional[int] = None


class AlertChannel:
    """Base class for alert channels"""
    
    async def send(self, alert: Alert) -> bool:
        """Send alert through this channel"""
        raise NotImplementedError


class ConsoleChannel(AlertChannel):
    """Console alert channel"""
    
    def __init__(self, colorize: bool = True):
        self.colorize = colorize
        self.colors = {
            AlertSeverity.DEBUG: "\033[36m",      # Cyan
            AlertSeverity.INFO: "\033[32m",       # Green
            AlertSeverity.WARNING: "\033[33m",    # Yellow
            AlertSeverity.ERROR: "\033[31m",      # Red
            AlertSeverity.CRITICAL: "\033[35m",   # Magenta
        }
        self.reset = "\033[0m"
    
    async def send(self, alert: Alert) -> bool:
        """Print alert to console"""
        try:
            if self.colorize:
                color = self.colors.get(alert.severity, "")
                print(f"{color}[ALERT {alert.severity.value.upper()}] {alert.message}{self.reset}")
            else:
                print(f"[ALERT {alert.severity.value.upper()}] {alert.message}")
            
            if alert.context:
                print(f"  Context: {json.dumps(alert.context, indent=2)}")
            
            return True
        except Exception as e:
            logger.error("Failed to send console alert", extra_fields={
                "error": str(e),
                "alert": alert.rule_name,
            })
            return False


class EmailChannel(AlertChannel):
    """Email alert channel"""
    
    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        smtp_user: str,
        smtp_password: str,
        from_address: str,
        to_addresses: List[str],
        subject_prefix: str = "[Alert]",
    ):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.from_address = from_address
        self.to_addresses = to_addresses
        self.subject_prefix = subject_prefix
    
    async def send(self, alert: Alert) -> bool:
        """Send alert via email"""
        try:
            msg = MIMEMultipart()
            msg["From"] = self.from_address
            msg["To"] = ", ".join(self.to_addresses)
            msg["Subject"] = f"{self.subject_prefix} {alert.severity.value.upper()}: {alert.rule_name}"
            
            # Create email body
            body = f"""
Alert: {alert.rule_name}
Severity: {alert.severity.value.upper()}
Time: {alert.timestamp.isoformat()}

Message:
{alert.message}

Context:
{json.dumps(alert.context, indent=2)}
"""
            msg.attach(MIMEText(body, "plain"))
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            logger.info("Email alert sent", extra_fields={
                "alert": alert.rule_name,
                "recipients": self.to_addresses,
            })
            return True
            
        except Exception as e:
            logger.error("Failed to send email alert", extra_fields={
                "error": str(e),
                "alert": alert.rule_name,
            })
            return False


class SlackChannel(AlertChannel):
    """Slack webhook alert channel"""
    
    def __init__(
        self,
        webhook_url: str,
        channel: Optional[str] = None,
        username: str = "Alert Bot",
        icon_emoji: str = ":warning:",
    ):
        self.webhook_url = webhook_url
        self.channel = channel
        self.username = username
        self.icon_emoji = icon_emoji
        
        self.severity_colors = {
            AlertSeverity.DEBUG: "#36A2EB",
            AlertSeverity.INFO: "#4BC0C0",
            AlertSeverity.WARNING: "#FFCE56",
            AlertSeverity.ERROR: "#FF6384",
            AlertSeverity.CRITICAL: "#FF4444",
        }
    
    async def send(self, alert: Alert) -> bool:
        """Send alert to Slack"""
        try:
            color = self.severity_colors.get(alert.severity, "#808080")
            
            payload = {
                "username": self.username,
                "icon_emoji": self.icon_emoji,
                "attachments": [
                    {
                        "color": color,
                        "title": f"{alert.severity.value.upper()}: {alert.rule_name}",
                        "text": alert.message,
                        "fields": [
                            {
                                "title": key,
                                "value": str(value),
                                "short": True,
                            }
                            for key, value in alert.context.items()
                        ],
                        "footer": "SelamAI Trading Platform",
                        "ts": int(alert.timestamp.timestamp()),
                    }
                ],
            }
            
            if self.channel:
                payload["channel"] = self.channel
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.webhook_url, json=payload) as response:
                    if response.status == 200:
                        logger.info("Slack alert sent", extra_fields={
                            "alert": alert.rule_name,
                        })
                        return True
                    else:
                        logger.error("Slack alert failed", extra_fields={
                            "status": response.status,
                            "alert": alert.rule_name,
                        })
                        return False
                        
        except Exception as e:
            logger.error("Failed to send Slack alert", extra_fields={
                "error": str(e),
                "alert": alert.rule_name,
            })
            return False


class WebhookChannel(AlertChannel):
    """Generic webhook alert channel"""
    
    def __init__(
        self,
        url: str,
        method: str = "POST",
        headers: Optional[Dict[str, str]] = None,
    ):
        self.url = url
        self.method = method
        self.headers = headers or {"Content-Type": "application/json"}
    
    async def send(self, alert: Alert) -> bool:
        """Send alert to webhook"""
        try:
            payload = {
                "rule": alert.rule_name,
                "severity": alert.severity.value,
                "message": alert.message,
                "timestamp": alert.timestamp.isoformat(),
                "context": alert.context,
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    self.method,
                    self.url,
                    json=payload,
                    headers=self.headers,
                ) as response:
                    if 200 <= response.status < 300:
                        logger.info("Webhook alert sent", extra_fields={
                            "alert": alert.rule_name,
                            "url": self.url,
                        })
                        return True
                    else:
                        logger.error("Webhook alert failed", extra_fields={
                            "status": response.status,
                            "alert": alert.rule_name,
                        })
                        return False
                        
        except Exception as e:
            logger.error("Failed to send webhook alert", extra_fields={
                "error": str(e),
                "alert": alert.rule_name,
            })
            return False


class AlertManager:
    """
    Centralized alert manager for handling critical events
    
    Supports multiple channels: console, email, Slack, webhooks
    Implements cooldown periods and rate limiting
    """
    
    def __init__(self):
        self.rules: Dict[str, AlertRule] = {}
        self.channels: Dict[str, AlertChannel] = {}
        self.last_alert_times: Dict[str, datetime] = {}
        self.alert_history: List[Alert] = []
        self.alert_counts: Dict[str, int] = defaultdict(int)
        self.rate_limit_enabled = True
        self.max_alerts_per_hour = 100
        self.aggregation_enabled = True
        self.aggregation_window = 60  # seconds
        
        logger.info("AlertManager initialized")
    
    def add_rule(self, rule: AlertRule) -> None:
        """Add an alert rule"""
        self.rules[rule.name] = rule
        logger.info("Alert rule added", extra_fields={
            "rule": rule.name,
            "severity": rule.severity.value,
        })
    
    def add_channel(self, name: str, channel: AlertChannel) -> None:
        """Add an alert channel"""
        self.channels[name] = channel
        logger.info("Alert channel added", extra_fields={
            "channel": name,
        })
    
    async def trigger(
        self,
        rule_name: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Trigger an alert
        
        Args:
            rule_name: Name of the alert rule
            context: Additional context data
        
        Returns:
            True if alert was sent, False otherwise
        """
        if rule_name not in self.rules:
            logger.warning("Unknown alert rule", extra_fields={
                "rule": rule_name,
            })
            return False
        
        rule = self.rules[rule_name]
        context = context or {}
        
        # Check cooldown
        if not self._check_cooldown(rule_name, rule.cooldown_minutes):
            logger.debug("Alert in cooldown period", extra_fields={
                "rule": rule_name,
            })
            return False
        
        # Check rate limit
        if self.rate_limit_enabled and not self._check_rate_limit():
            logger.warning("Alert rate limit exceeded")
            return False
        
        # Format message with context
        try:
            message = rule.message_template.format(**context)
        except KeyError as e:
            message = f"{rule.message_template} (context incomplete: {str(e)})"
        
        # Create alert
        alert = Alert(
            rule_name=rule_name,
            severity=rule.severity,
            message=message,
            timestamp=datetime.utcnow(),
            context=context,
            channels=rule.channels,
        )
        
        # Send to channels
        success = await self._send_alert(alert)
        
        if success:
            self.last_alert_times[rule_name] = datetime.utcnow()
            self.alert_history.append(alert)
            self.alert_counts[rule_name] += 1
            
            logger.info("Alert triggered", extra_fields={
                "rule": rule_name,
                "severity": rule.severity.value,
            })
        
        return success
    
    async def _send_alert(self, alert: Alert) -> bool:
        """Send alert to all configured channels"""
        success = False
        
        for channel_name in alert.channels:
            if channel_name not in self.channels:
                logger.warning("Unknown alert channel", extra_fields={
                    "channel": channel_name,
                })
                continue
            
            channel = self.channels[channel_name]
            try:
                result = await channel.send(alert)
                success = success or result
            except Exception as e:
                logger.error("Alert channel failed", extra_fields={
                    "channel": channel_name,
                    "error": str(e),
                })
        
        return success
    
    def _check_cooldown(self, rule_name: str, cooldown_minutes: int) -> bool:
        """Check if alert is in cooldown period"""
        if rule_name not in self.last_alert_times:
            return True
        
        last_time = self.last_alert_times[rule_name]
        cooldown = timedelta(minutes=cooldown_minutes)
        
        return datetime.utcnow() - last_time >= cooldown
    
    def _check_rate_limit(self) -> bool:
        """Check if rate limit is exceeded"""
        cutoff = datetime.utcnow() - timedelta(hours=1)
        recent_alerts = [a for a in self.alert_history if a.timestamp >= cutoff]
        
        return len(recent_alerts) < self.max_alerts_per_hour
    
    def get_alert_stats(self) -> Dict[str, Any]:
        """Get alert statistics"""
        return {
            "total_rules": len(self.rules),
            "total_channels": len(self.channels),
            "alert_counts": dict(self.alert_counts),
            "recent_alerts": len([
                a for a in self.alert_history
                if a.timestamp >= datetime.utcnow() - timedelta(hours=1)
            ]),
        }


# Global alert manager instance
_alert_manager: Optional[AlertManager] = None


def get_alert_manager() -> AlertManager:
    """Get the global alert manager instance"""
    global _alert_manager
    
    if _alert_manager is None:
        _alert_manager = AlertManager()
    
    return _alert_manager


# Convenience functions for common alerts
async def alert_circuit_breaker_triggered(symbol: str, reason: str) -> None:
    """Trigger circuit breaker alert"""
    await get_alert_manager().trigger("circuit_breaker_triggered", {
        "symbol": symbol,
        "reason": reason,
    })


async def alert_trade_failed(error_message: str, trade_id: str = "") -> None:
    """Trigger trade failed alert"""
    await get_alert_manager().trigger("trade_failed", {
        "error_message": error_message,
        "trade_id": trade_id,
    })


async def alert_high_drawdown(drawdown: float) -> None:
    """Trigger high drawdown alert"""
    await get_alert_manager().trigger("drawdown_exceeded", {
        "drawdown": f"{drawdown:.2f}",
    })
