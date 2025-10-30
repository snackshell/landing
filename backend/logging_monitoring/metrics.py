"""
Performance metrics tracker for monitoring trading system health
"""

import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
from threading import Lock
import statistics

from .logger import get_logger

logger = get_logger(__name__)


@dataclass
class Metric:
    """Represents a single metric data point"""
    name: str
    value: float
    timestamp: datetime
    labels: Dict[str, str]
    unit: Optional[str] = None


@dataclass
class MetricsSummary:
    """Summary statistics for a metric"""
    name: str
    count: int
    sum: float
    min: float
    max: float
    mean: float
    median: Optional[float] = None
    p95: Optional[float] = None
    p99: Optional[float] = None


class MetricsTracker:
    """
    Centralized metrics tracker for performance monitoring
    
    Tracks various metrics including:
    - Agent performance (requests, decisions, errors)
    - Strategy statistics (signals, accuracy, P&L)
    - Trading metrics (trades, execution time, success rate)
    - System health (API latency, DB queries, connections)
    """
    
    def __init__(self, retention_hours: int = 168):  # 7 days
        self.retention_hours = retention_hours
        self._metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=10000))
        self._counters: Dict[str, float] = defaultdict(float)
        self._gauges: Dict[str, float] = defaultdict(float)
        self._lock = Lock()
        
        logger.info("MetricsTracker initialized", extra_fields={
            "retention_hours": retention_hours,
        })
    
    def record_metric(
        self,
        name: str,
        value: float,
        labels: Optional[Dict[str, str]] = None,
        unit: Optional[str] = None,
    ) -> None:
        """
        Record a metric value
        
        Args:
            name: Metric name
            value: Metric value
            labels: Optional labels for metric dimensions
            unit: Optional unit (e.g., "ms", "bytes", "percent")
        """
        if labels is None:
            labels = {}
        
        metric = Metric(
            name=name,
            value=value,
            timestamp=datetime.utcnow(),
            labels=labels,
            unit=unit,
        )
        
        with self._lock:
            self._metrics[name].append(metric)
            self._cleanup_old_metrics()
    
    def increment_counter(self, name: str, value: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        """Increment a counter metric"""
        with self._lock:
            self._counters[name] += value
        
        self.record_metric(name, value, labels=labels)
    
    def set_gauge(self, name: str, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        """Set a gauge metric (point-in-time value)"""
        with self._lock:
            self._gauges[name] = value
        
        self.record_metric(name, value, labels=labels)
    
    def record_duration(self, name: str, duration_seconds: float, labels: Optional[Dict[str, str]] = None) -> None:
        """Record a duration metric"""
        self.record_metric(name, duration_seconds, labels=labels, unit="seconds")
    
    def get_metric_summary(self, name: str, minutes: Optional[int] = None) -> Optional[MetricsSummary]:
        """
        Get summary statistics for a metric
        
        Args:
            name: Metric name
            minutes: Only include metrics from last N minutes (None for all)
        
        Returns:
            MetricsSummary or None if no data
        """
        with self._lock:
            if name not in self._metrics or not self._metrics[name]:
                return None
            
            metrics = list(self._metrics[name])
        
        # Filter by time window if specified
        if minutes:
            cutoff = datetime.utcnow() - timedelta(minutes=minutes)
            metrics = [m for m in metrics if m.timestamp >= cutoff]
        
        if not metrics:
            return None
        
        values = [m.value for m in metrics]
        
        summary = MetricsSummary(
            name=name,
            count=len(values),
            sum=sum(values),
            min=min(values),
            max=max(values),
            mean=statistics.mean(values),
        )
        
        # Calculate percentiles if enough data
        if len(values) >= 2:
            summary.median = statistics.median(values)
        
        if len(values) >= 20:
            sorted_values = sorted(values)
            summary.p95 = sorted_values[int(len(sorted_values) * 0.95)]
            summary.p99 = sorted_values[int(len(sorted_values) * 0.99)]
        
        return summary
    
    def get_counter(self, name: str) -> float:
        """Get current counter value"""
        with self._lock:
            return self._counters.get(name, 0.0)
    
    def get_gauge(self, name: str) -> Optional[float]:
        """Get current gauge value"""
        with self._lock:
            return self._gauges.get(name)
    
    def get_all_metrics(self, minutes: Optional[int] = None) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get all metrics
        
        Args:
            minutes: Only include metrics from last N minutes (None for all)
        
        Returns:
            Dictionary of metric name to list of metric data points
        """
        result = {}
        
        with self._lock:
            metric_names = list(self._metrics.keys())
        
        for name in metric_names:
            with self._lock:
                metrics = list(self._metrics[name])
            
            if minutes:
                cutoff = datetime.utcnow() - timedelta(minutes=minutes)
                metrics = [m for m in metrics if m.timestamp >= cutoff]
            
            result[name] = [
                {
                    "value": m.value,
                    "timestamp": m.timestamp.isoformat(),
                    "labels": m.labels,
                    "unit": m.unit,
                }
                for m in metrics
            ]
        
        return result
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """
        Get formatted data for dashboard visualization
        
        Returns:
            Dictionary containing current metrics and summaries
        """
        # Agent metrics
        agent_data = {
            "requests_total": self.get_counter("agent_requests_total"),
            "decisions_total": self.get_counter("agent_decisions_total"),
            "errors_total": self.get_counter("agent_errors_total"),
            "avg_duration": None,
        }
        
        duration_summary = self.get_metric_summary("agent_requests_duration_seconds", minutes=60)
        if duration_summary:
            agent_data["avg_duration"] = duration_summary.mean
        
        # Trading metrics
        trading_data = {
            "trades_total": self.get_counter("trades_total"),
            "trades_successful": self.get_counter("trades_successful"),
            "trades_failed": self.get_counter("trades_failed"),
            "profit_loss_total": self.get_gauge("profit_loss_total"),
            "win_rate": 0.0,
        }
        
        if trading_data["trades_total"] > 0:
            trading_data["win_rate"] = (
                trading_data["trades_successful"] / trading_data["trades_total"] * 100
            )
        
        # System metrics
        system_data = {
            "api_requests_total": self.get_counter("api_requests_total"),
            "api_errors_total": self.get_counter("api_errors_total"),
            "websocket_connections": self.get_gauge("websocket_connections"),
            "memory_usage_percent": self.get_gauge("memory_usage_percent"),
            "cpu_usage_percent": self.get_gauge("cpu_usage_percent"),
        }
        
        # Risk metrics
        risk_data = {
            "risk_exposure_percent": self.get_gauge("risk_exposure_percent"),
            "drawdown_percent": self.get_gauge("drawdown_percent"),
            "portfolio_value": self.get_gauge("portfolio_value"),
            "circuit_breakers_triggered": self.get_counter("circuit_breakers_triggered"),
        }
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "agent": agent_data,
            "trading": trading_data,
            "system": system_data,
            "risk": risk_data,
        }
    
    def _cleanup_old_metrics(self) -> None:
        """Remove metrics older than retention period"""
        cutoff = datetime.utcnow() - timedelta(hours=self.retention_hours)
        
        for name in list(self._metrics.keys()):
            metrics = self._metrics[name]
            # Remove old metrics from the front of deque
            while metrics and metrics[0].timestamp < cutoff:
                metrics.popleft()
    
    def reset(self) -> None:
        """Reset all metrics (useful for testing)"""
        with self._lock:
            self._metrics.clear()
            self._counters.clear()
            self._gauges.clear()
        
        logger.info("Metrics reset")


# Global metrics tracker instance
_metrics_tracker: Optional[MetricsTracker] = None


def get_metrics_tracker() -> MetricsTracker:
    """Get the global metrics tracker instance"""
    global _metrics_tracker
    
    if _metrics_tracker is None:
        _metrics_tracker = MetricsTracker()
    
    return _metrics_tracker


class Timer:
    """Context manager for timing operations"""
    
    def __init__(self, metric_name: str, labels: Optional[Dict[str, str]] = None):
        self.metric_name = metric_name
        self.labels = labels or {}
        self.start_time: Optional[float] = None
        self.duration: Optional[float] = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.duration = time.time() - self.start_time
        get_metrics_tracker().record_duration(
            self.metric_name,
            self.duration,
            labels=self.labels,
        )
