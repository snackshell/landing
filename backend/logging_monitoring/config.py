"""
Configuration loader for logging and monitoring
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

from .logger import get_logger

logger = get_logger(__name__)


class LoggingConfig(BaseModel):
    """Logging configuration model"""
    level: str = "INFO"
    format: str = "json"
    enable_correlation_ids: bool = True
    
    class SinkConfig(BaseModel):
        enabled: bool = True
        level: str = "INFO"
        colorize: Optional[bool] = None
        path: Optional[str] = None
        
        class RotationConfig(BaseModel):
            max_size: int = 10485760  # 10MB
            backup_count: int = 10
        
        rotation: Optional[RotationConfig] = None
    
    class SinksConfig(BaseModel):
        console: "LoggingConfig.SinkConfig"
        file: "LoggingConfig.SinkConfig"
        error_file: "LoggingConfig.SinkConfig"
    
    sinks: SinksConfig
    standard_fields: list = Field(default_factory=list)
    trading_fields: list = Field(default_factory=list)
    
    class RetentionConfig(BaseModel):
        days: int = 30
        compress: bool = True
    
    retention: RetentionConfig
    
    class PerformanceConfig(BaseModel):
        enabled: bool = True
        log_slow_requests: bool = True
        slow_threshold_ms: int = 1000
        log_database_queries: bool = True
        log_api_calls: bool = True
    
    performance: PerformanceConfig


class MetricsConfig(BaseModel):
    """Metrics configuration model"""
    enabled: bool = True
    collection_interval: int = 60
    
    class StorageConfig(BaseModel):
        type: str = "memory"
        retention_hours: int = 168
    
    storage: StorageConfig
    
    class MetricGroupConfig(BaseModel):
        enabled: bool = True
        metrics: list = Field(default_factory=list)
    
    agent_metrics: MetricGroupConfig
    strategy_metrics: MetricGroupConfig
    trading_metrics: MetricGroupConfig
    risk_metrics: MetricGroupConfig
    system_metrics: MetricGroupConfig
    custom_metrics: Optional[MetricGroupConfig] = None


class AlertsConfig(BaseModel):
    """Alerts configuration model"""
    enabled: bool = True
    
    class ChannelConfig(BaseModel):
        enabled: bool = False
    
    class EmailConfig(ChannelConfig):
        smtp_host: Optional[str] = None
        smtp_port: Optional[int] = None
        smtp_user: Optional[str] = None
        smtp_password: Optional[str] = None
        from_address: Optional[str] = None
        to_addresses: list = Field(default_factory=list)
        subject_prefix: str = "[SelamAI Alert]"
    
    class SlackConfig(ChannelConfig):
        webhook_url: Optional[str] = None
        channel: Optional[str] = None
        username: str = "SelamAI Alert Bot"
        icon_emoji: str = ":warning:"
    
    class WebhookConfig(ChannelConfig):
        url: Optional[str] = None
        method: str = "POST"
        headers: Dict[str, str] = Field(default_factory=dict)
    
    class ConsoleConfig(ChannelConfig):
        enabled: bool = True
        colorize: bool = True
    
    class ChannelsConfig(BaseModel):
        email: "AlertsConfig.EmailConfig"
        slack: "AlertsConfig.SlackConfig"
        webhook: "AlertsConfig.WebhookConfig"
        console: "AlertsConfig.ConsoleConfig"
    
    channels: ChannelsConfig
    
    class AlertRuleConfig(BaseModel):
        severity: str
        message: str
        channels: list = Field(default_factory=list)
        cooldown_minutes: int = 5
        threshold: Optional[float] = None
        window_minutes: Optional[int] = None
    
    rules: Dict[str, AlertRuleConfig] = Field(default_factory=dict)
    
    class SettingsConfig(BaseModel):
        aggregation_enabled: bool = True
        aggregation_window_seconds: int = 60
        rate_limit_enabled: bool = True
        max_alerts_per_hour: int = 100
        history_enabled: bool = True
        history_retention_days: int = 30
    
    settings: SettingsConfig


class MonitoringConfig(BaseModel):
    """Complete monitoring configuration"""
    logging: LoggingConfig
    exporters: Optional[Dict[str, Any]] = None


def load_monitoring_config(config_dir: str = "config/monitoring") -> Dict[str, Any]:
    """
    Load monitoring configuration from YAML files
    
    Args:
        config_dir: Directory containing monitoring config files
    
    Returns:
        Dictionary with logging, metrics, and alerts configuration
    """
    config_path = Path(config_dir)
    
    configs = {}
    
    # Load logging config
    logging_file = config_path / "logging.yaml"
    if logging_file.exists():
        with open(logging_file) as f:
            data = yaml.safe_load(f)
            # Substitute environment variables
            data = _substitute_env_vars(data)
            configs["logging"] = data.get("logging", {})
            configs["exporters"] = data.get("exporters", {})
    else:
        logger.warning(f"Logging config not found: {logging_file}")
        configs["logging"] = {}
    
    # Load metrics config
    metrics_file = config_path / "metrics.yaml"
    if metrics_file.exists():
        with open(metrics_file) as f:
            data = yaml.safe_load(f)
            configs["metrics"] = data.get("metrics", {})
            if "publishing" in data:
                configs["metrics_publishing"] = data["publishing"]
            if "thresholds" in data:
                configs["metrics_thresholds"] = data["thresholds"]
    else:
        logger.warning(f"Metrics config not found: {metrics_file}")
        configs["metrics"] = {}
    
    # Load alerts config
    alerts_file = config_path / "alerts.yaml"
    if alerts_file.exists():
        with open(alerts_file) as f:
            data = yaml.safe_load(f)
            data = _substitute_env_vars(data)
            configs["alerts"] = data.get("alerts", {})
    else:
        logger.warning(f"Alerts config not found: {alerts_file}")
        configs["alerts"] = {}
    
    return configs


def _substitute_env_vars(data: Any) -> Any:
    """Recursively substitute environment variables in config"""
    if isinstance(data, dict):
        return {k: _substitute_env_vars(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [_substitute_env_vars(item) for item in data]
    elif isinstance(data, str):
        # Handle ${VAR:default} syntax
        if data.startswith("${") and data.endswith("}"):
            var_expr = data[2:-1]
            if ":" in var_expr:
                var_name, default = var_expr.split(":", 1)
                return os.getenv(var_name, default)
            else:
                return os.getenv(var_expr, data)
    return data
