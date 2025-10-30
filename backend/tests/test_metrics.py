"""
Tests for metrics tracking module
"""

import pytest
import time
from datetime import datetime, timedelta

from backend.logging_monitoring.metrics import (
    MetricsTracker,
    Metric,
    MetricsSummary,
    Timer,
    get_metrics_tracker,
)


class TestMetric:
    """Test Metric dataclass"""
    
    def test_metric_creation(self):
        """Test creating a metric"""
        metric = Metric(
            name="test_metric",
            value=42.0,
            timestamp=datetime.utcnow(),
            labels={"env": "test"},
            unit="ms",
        )
        
        assert metric.name == "test_metric"
        assert metric.value == 42.0
        assert metric.labels == {"env": "test"}
        assert metric.unit == "ms"


class TestMetricsTracker:
    """Test MetricsTracker functionality"""
    
    @pytest.fixture
    def tracker(self):
        """Create a fresh metrics tracker for each test"""
        return MetricsTracker(retention_hours=1)
    
    def test_record_metric(self, tracker):
        """Test recording a metric"""
        tracker.record_metric("test_metric", 100.0, labels={"type": "test"})
        
        summary = tracker.get_metric_summary("test_metric")
        assert summary is not None
        assert summary.count == 1
        assert summary.sum == 100.0
        assert summary.mean == 100.0
    
    def test_increment_counter(self, tracker):
        """Test incrementing a counter"""
        tracker.increment_counter("requests_total", 1.0)
        tracker.increment_counter("requests_total", 1.0)
        tracker.increment_counter("requests_total", 3.0)
        
        counter_value = tracker.get_counter("requests_total")
        assert counter_value == 5.0
    
    def test_set_gauge(self, tracker):
        """Test setting a gauge"""
        tracker.set_gauge("memory_usage", 75.5)
        
        gauge_value = tracker.get_gauge("memory_usage")
        assert gauge_value == 75.5
        
        # Update gauge
        tracker.set_gauge("memory_usage", 80.0)
        gauge_value = tracker.get_gauge("memory_usage")
        assert gauge_value == 80.0
    
    def test_record_duration(self, tracker):
        """Test recording duration metrics"""
        tracker.record_duration("request_duration", 1.5, labels={"endpoint": "/api/test"})
        
        summary = tracker.get_metric_summary("request_duration")
        assert summary is not None
        assert summary.mean == 1.5
    
    def test_metric_summary_statistics(self, tracker):
        """Test metric summary calculations"""
        # Record multiple values (need at least 100 for p95/p99)
        values = list(range(1, 101))  # 1 to 100
        for value in values:
            tracker.record_metric("test_metric", float(value))
        
        summary = tracker.get_metric_summary("test_metric")
        
        assert summary.count == 100
        assert summary.sum == 5050.0  # Sum of 1 to 100
        assert summary.min == 1.0
        assert summary.max == 100.0
        assert summary.mean == 50.5
        assert summary.median == 50.5  # Median of 1-100
        assert summary.p95 is not None
        assert summary.p95 >= 90  # P95 should be around 95
        assert summary.p99 is not None
        assert summary.p99 >= 95  # P99 should be around 99
    
    def test_metric_summary_with_time_window(self, tracker):
        """Test metric summary with time window filter"""
        # Record old metric
        old_metric = Metric(
            name="test_metric",
            value=100.0,
            timestamp=datetime.utcnow() - timedelta(hours=2),
            labels={},
        )
        tracker._metrics["test_metric"].append(old_metric)
        
        # Record recent metric
        tracker.record_metric("test_metric", 50.0)
        
        # Get summary for last 60 minutes (should only include recent)
        summary = tracker.get_metric_summary("test_metric", minutes=60)
        assert summary.count == 1
        assert summary.mean == 50.0
    
    def test_get_all_metrics(self, tracker):
        """Test getting all metrics"""
        tracker.record_metric("metric1", 10.0)
        tracker.record_metric("metric2", 20.0)
        tracker.record_metric("metric1", 15.0)
        
        all_metrics = tracker.get_all_metrics()
        
        assert "metric1" in all_metrics
        assert "metric2" in all_metrics
        assert len(all_metrics["metric1"]) == 2
        assert len(all_metrics["metric2"]) == 1
    
    def test_get_dashboard_data(self, tracker):
        """Test getting dashboard data"""
        # Set up some test metrics
        tracker.increment_counter("agent_requests_total", 100)
        tracker.increment_counter("trades_total", 50)
        tracker.increment_counter("trades_successful", 45)
        tracker.set_gauge("memory_usage_percent", 75.0)
        tracker.set_gauge("cpu_usage_percent", 60.0)
        
        dashboard_data = tracker.get_dashboard_data()
        
        assert "agent" in dashboard_data
        assert "trading" in dashboard_data
        assert "system" in dashboard_data
        assert "risk" in dashboard_data
        assert dashboard_data["agent"]["requests_total"] == 100
        assert dashboard_data["trading"]["trades_total"] == 50
        assert dashboard_data["system"]["memory_usage_percent"] == 75.0
    
    def test_reset(self, tracker):
        """Test resetting metrics"""
        tracker.record_metric("test_metric", 100.0)
        tracker.increment_counter("test_counter", 10.0)
        tracker.set_gauge("test_gauge", 50.0)
        
        tracker.reset()
        
        assert tracker.get_metric_summary("test_metric") is None
        assert tracker.get_counter("test_counter") == 0.0
        assert tracker.get_gauge("test_gauge") is None


class TestTimer:
    """Test Timer context manager"""
    
    def test_timer_records_duration(self):
        """Test that Timer records duration correctly"""
        # Reset the global tracker to ensure clean state
        from backend.logging_monitoring.metrics import _metrics_tracker
        import backend.logging_monitoring.metrics as metrics_module
        metrics_module._metrics_tracker = None
        
        tracker = get_metrics_tracker()
        
        with Timer("test_operation"):
            time.sleep(0.1)  # Sleep for 100ms
        
        summary = tracker.get_metric_summary("test_operation")
        assert summary is not None
        assert summary.count == 1
        assert summary.mean >= 0.1  # At least 100ms
        assert summary.mean < 0.2   # But less than 200ms (with some tolerance)
    
    def test_timer_with_labels(self):
        """Test Timer with labels"""
        # Reset the global tracker to ensure clean state
        from backend.logging_monitoring.metrics import _metrics_tracker
        import backend.logging_monitoring.metrics as metrics_module
        metrics_module._metrics_tracker = None
        
        tracker = get_metrics_tracker()
        
        with Timer("api_request", labels={"endpoint": "/api/test", "method": "GET"}):
            time.sleep(0.05)
        
        summary = tracker.get_metric_summary("api_request")
        assert summary is not None
        assert summary.count == 1


class TestMetricsIntegration:
    """Integration tests for metrics system"""
    
    def test_global_metrics_tracker(self):
        """Test global metrics tracker singleton"""
        tracker1 = get_metrics_tracker()
        tracker2 = get_metrics_tracker()
        
        assert tracker1 is tracker2
        
        # Metrics should be shared
        tracker1.increment_counter("shared_counter", 5)
        assert tracker2.get_counter("shared_counter") == 5
    
    def test_trading_metrics_workflow(self):
        """Test a realistic trading metrics workflow"""
        tracker = MetricsTracker()
        
        # Simulate trade execution
        tracker.increment_counter("trades_total", 1)
        tracker.record_duration("order_execution_time_seconds", 0.5)
        tracker.increment_counter("trades_successful", 1)
        
        # Update portfolio
        tracker.set_gauge("portfolio_value", 100000.0)
        tracker.set_gauge("risk_exposure_percent", 25.0)
        
        # Simulate another trade
        tracker.increment_counter("trades_total", 1)
        tracker.record_duration("order_execution_time_seconds", 0.3)
        tracker.increment_counter("trades_successful", 1)
        
        # Check results
        assert tracker.get_counter("trades_total") == 2.0
        assert tracker.get_counter("trades_successful") == 2.0
        
        duration_summary = tracker.get_metric_summary("order_execution_time_seconds")
        assert duration_summary.count == 2
        assert duration_summary.mean == 0.4  # Average of 0.5 and 0.3
        
        dashboard = tracker.get_dashboard_data()
        assert dashboard["trading"]["trades_total"] == 2.0
        assert dashboard["trading"]["win_rate"] == 100.0  # All successful
    
    def test_agent_metrics_workflow(self):
        """Test AI agent metrics workflow"""
        tracker = MetricsTracker()
        
        # Simulate agent requests
        for i in range(10):
            tracker.increment_counter("agent_requests_total", 1)
            tracker.record_duration("agent_requests_duration_seconds", 0.1 + (i * 0.01))
            tracker.increment_counter("agent_decisions_total", 1)
        
        # Simulate some errors
        tracker.increment_counter("agent_errors_total", 2)
        
        # Check results
        dashboard = tracker.get_dashboard_data()
        assert dashboard["agent"]["requests_total"] == 10
        assert dashboard["agent"]["decisions_total"] == 10
        assert dashboard["agent"]["errors_total"] == 2
        
        duration_summary = tracker.get_metric_summary("agent_requests_duration_seconds")
        assert duration_summary.count == 10
