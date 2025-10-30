"""
Setup and initialization for logging and monitoring system

This module provides convenience functions to initialize the entire
logging and monitoring system from configuration files.
"""

import os
from typing import Optional

from .logger import setup_logging, get_logger
from .metrics import get_metrics_tracker
from .alerting import get_alert_manager, AlertRule, AlertSeverity, ConsoleChannel
from .config import load_monitoring_config

logger = get_logger(__name__)


def initialize_monitoring(
    config_dir: str = "config/monitoring",
    environment: Optional[str] = None,
) -> None:
    """
    Initialize the complete monitoring system from configuration files
    
    This function:
    1. Loads monitoring configuration
    2. Sets up structured logging
    3. Initializes metrics tracker
    4. Configures alert manager with rules and channels
    
    Args:
        config_dir: Directory containing monitoring configuration
        environment: Environment name (development, staging, production)
    
    Example:
        from backend.logging_monitoring.setup import initialize_monitoring
        
        initialize_monitoring()
    """
    if environment is None:
        environment = os.getenv("ENVIRONMENT", "development")
    
    print(f"🚀 Initializing SelamAI Monitoring System...")
    print(f"   Environment: {environment}")
    print(f"   Config Dir: {config_dir}")
    
    # Load configuration
    try:
        config = load_monitoring_config(config_dir)
    except Exception as e:
        print(f"⚠️  Warning: Could not load monitoring config: {e}")
        print("   Using default configuration")
        config = {}
    
    # Setup logging
    logging_config = config.get("logging", {})
    setup_logging(
        level=logging_config.get("level", "INFO"),
        log_format=logging_config.get("format", "json"),
        console_enabled=logging_config.get("sinks", {}).get("console", {}).get("enabled", True),
        file_enabled=logging_config.get("sinks", {}).get("file", {}).get("enabled", True),
        log_file=logging_config.get("sinks", {}).get("file", {}).get("path", "logs/selamai.log"),
        error_log_file=logging_config.get("sinks", {}).get("error_file", {}).get("path", "logs/errors.log"),
        service="selamai",
        environment=environment,
    )
    
    print("   ✅ Logging configured")
    logger.info("Logging system initialized", extra_fields={
        "environment": environment,
        "format": logging_config.get("format", "json"),
    })
    
    # Initialize metrics tracker
    metrics_config = config.get("metrics", {})
    if metrics_config.get("enabled", True):
        tracker = get_metrics_tracker()
        logger.info("Metrics tracker initialized", extra_fields={
            "retention_hours": metrics_config.get("storage", {}).get("retention_hours", 168),
        })
        print("   ✅ Metrics tracker initialized")
    else:
        print("   ⏭️  Metrics tracking disabled")
    
    # Setup alert manager
    alerts_config = config.get("alerts", {})
    if alerts_config.get("enabled", True):
        alert_manager = get_alert_manager()
        
        # Add channels
        channels_config = alerts_config.get("channels", {})
        
        # Console channel
        console_config = channels_config.get("console", {})
        if console_config.get("enabled", True):
            alert_manager.add_channel(
                "console",
                ConsoleChannel(colorize=console_config.get("colorize", True))
            )
            print("   ✅ Console alert channel added")
        
        # Email channel
        email_config = channels_config.get("email", {})
        if email_config.get("enabled", False):
            try:
                from .alerting import EmailChannel
                alert_manager.add_channel(
                    "email",
                    EmailChannel(
                        smtp_host=email_config.get("smtp_host"),
                        smtp_port=email_config.get("smtp_port", 587),
                        smtp_user=email_config.get("smtp_user"),
                        smtp_password=email_config.get("smtp_password"),
                        from_address=email_config.get("from_address"),
                        to_addresses=email_config.get("to_addresses", []),
                        subject_prefix=email_config.get("subject_prefix", "[SelamAI Alert]"),
                    )
                )
                print("   ✅ Email alert channel added")
            except Exception as e:
                logger.warning("Failed to setup email channel", extra_fields={"error": str(e)})
                print(f"   ⚠️  Email channel setup failed: {e}")
        
        # Slack channel
        slack_config = channels_config.get("slack", {})
        if slack_config.get("enabled", False):
            try:
                from .alerting import SlackChannel
                alert_manager.add_channel(
                    "slack",
                    SlackChannel(
                        webhook_url=slack_config.get("webhook_url"),
                        channel=slack_config.get("channel"),
                        username=slack_config.get("username", "SelamAI Alert Bot"),
                        icon_emoji=slack_config.get("icon_emoji", ":warning:"),
                    )
                )
                print("   ✅ Slack alert channel added")
            except Exception as e:
                logger.warning("Failed to setup Slack channel", extra_fields={"error": str(e)})
                print(f"   ⚠️  Slack channel setup failed: {e}")
        
        # Webhook channel
        webhook_config = channels_config.get("webhook", {})
        if webhook_config.get("enabled", False):
            try:
                from .alerting import WebhookChannel
                alert_manager.add_channel(
                    "webhook",
                    WebhookChannel(
                        url=webhook_config.get("url"),
                        method=webhook_config.get("method", "POST"),
                        headers=webhook_config.get("headers", {}),
                    )
                )
                print("   ✅ Webhook alert channel added")
            except Exception as e:
                logger.warning("Failed to setup webhook channel", extra_fields={"error": str(e)})
                print(f"   ⚠️  Webhook channel setup failed: {e}")
        
        # Add alert rules
        rules_config = alerts_config.get("rules", {})
        for rule_name, rule_config in rules_config.items():
            try:
                severity_str = rule_config.get("severity", "info")
                severity = AlertSeverity[severity_str.upper()] if hasattr(AlertSeverity, severity_str.upper()) else AlertSeverity.INFO
                
                alert_manager.add_rule(
                    AlertRule(
                        name=rule_name,
                        severity=severity,
                        message_template=rule_config.get("message", f"{rule_name}: {{details}}"),
                        channels=rule_config.get("channels", ["console"]),
                        cooldown_minutes=rule_config.get("cooldown_minutes", 5),
                        threshold=rule_config.get("threshold"),
                        window_minutes=rule_config.get("window_minutes"),
                    )
                )
            except Exception as e:
                logger.warning(f"Failed to add alert rule: {rule_name}", extra_fields={"error": str(e)})
        
        print(f"   ✅ Alert manager configured with {len(rules_config)} rules")
        logger.info("Alert manager initialized", extra_fields={
            "rules_count": len(rules_config),
            "channels_count": len(alert_manager.channels),
        })
    else:
        print("   ⏭️  Alerting disabled")
    
    print("✅ Monitoring system initialized successfully!\n")
    
    # Log system info
    logger.info("SelamAI Trading Platform started", extra_fields={
        "environment": environment,
        "logging_enabled": True,
        "metrics_enabled": metrics_config.get("enabled", True),
        "alerts_enabled": alerts_config.get("enabled", True),
    })


def get_monitoring_status() -> dict:
    """
    Get the current status of the monitoring system
    
    Returns:
        Dictionary with monitoring system status
    """
    status = {
        "logging": {
            "enabled": True,
            "configured": True,
        },
        "metrics": {
            "enabled": True,
            "tracker": get_metrics_tracker() is not None,
        },
        "alerts": {
            "enabled": True,
            "manager": get_alert_manager() is not None,
        },
    }
    
    # Get alert manager stats
    try:
        alert_manager = get_alert_manager()
        stats = alert_manager.get_alert_stats()
        status["alerts"]["rules"] = stats["total_rules"]
        status["alerts"]["channels"] = stats["total_channels"]
    except:
        pass
    
    # Get metrics tracker stats
    try:
        metrics = get_metrics_tracker()
        dashboard = metrics.get_dashboard_data()
        status["metrics"]["data_available"] = True
    except:
        status["metrics"]["data_available"] = False
    
    return status
