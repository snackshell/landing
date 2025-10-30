"""
Example usage of the logging and monitoring system

Run this file to see the logging and monitoring system in action:
    python backend/logging_monitoring/examples.py
"""

import asyncio
import time
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.logging_monitoring import (
    setup_logging,
    get_logger,
    get_metrics_tracker,
    get_alert_manager,
    correlation_context,
)
from backend.logging_monitoring.metrics import Timer
from backend.logging_monitoring.alerting import AlertRule, AlertSeverity, ConsoleChannel


def example_logging():
    """Example: Structured logging with correlation IDs"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Structured Logging")
    print("="*60 + "\n")
    
    # Setup logging
    setup_logging(
        level="INFO",
        log_format="text",  # Use text format for console readability
        console_enabled=True,
        file_enabled=False,  # Disable file logging for examples
    )
    
    logger = get_logger("trading.example")
    
    # Basic logging
    logger.info("Trading system initialized")
    
    # Logging with extra fields
    logger.info("Processing trade request", extra_fields={
        "symbol": "EUR/USD",
        "quantity": 1000,
        "order_type": "market",
    })
    
    # Using correlation context
    with correlation_context("trade-123-456"):
        logger.info("Trade validation started")
        logger.info("Checking risk limits")
        logger.info("Trade approved")
    
    # Logging with different levels
    logger.debug("Debug information")
    logger.warning("Price volatility high", extra_fields={"volatility": 2.5})
    logger.error("Order execution failed", extra_fields={
        "error": "Insufficient margin",
        "required_margin": 5000,
        "available_margin": 3000,
    })
    
    print("\n✅ Logging examples completed\n")


def example_metrics():
    """Example: Performance metrics tracking"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Performance Metrics")
    print("="*60 + "\n")
    
    metrics = get_metrics_tracker()
    
    # Simulate trading activity
    print("📊 Simulating trading activity...\n")
    
    # Counter: Track total trades
    for i in range(10):
        metrics.increment_counter("trades_total", 1)
        if i < 8:  # 80% success rate
            metrics.increment_counter("trades_successful", 1)
        else:
            metrics.increment_counter("trades_failed", 1)
    
    # Gauge: Track portfolio value
    metrics.set_gauge("portfolio_value", 100000.0)
    metrics.set_gauge("risk_exposure_percent", 25.0)
    metrics.set_gauge("drawdown_percent", 5.0)
    
    # Duration: Track execution times
    for _ in range(5):
        with Timer("order_execution_time_seconds"):
            time.sleep(0.1)  # Simulate order execution
    
    # Agent metrics
    for i in range(20):
        metrics.increment_counter("agent_requests_total", 1)
        metrics.record_duration("agent_requests_duration_seconds", 0.5 + (i * 0.01))
    
    # System metrics
    metrics.set_gauge("memory_usage_percent", 75.0)
    metrics.set_gauge("cpu_usage_percent", 60.0)
    metrics.increment_counter("api_requests_total", 100)
    metrics.increment_counter("api_errors_total", 5)
    
    # Get metrics summary
    print("\n📈 Metrics Summary:")
    print("-" * 60)
    
    trade_summary = metrics.get_metric_summary("order_execution_time_seconds")
    if trade_summary:
        print(f"Order Execution Time:")
        print(f"  Count: {trade_summary.count}")
        print(f"  Mean: {trade_summary.mean:.3f}s")
        print(f"  Min: {trade_summary.min:.3f}s")
        print(f"  Max: {trade_summary.max:.3f}s")
    
    # Get dashboard data
    dashboard = metrics.get_dashboard_data()
    print(f"\nTrading Metrics:")
    print(f"  Total Trades: {dashboard['trading']['trades_total']}")
    print(f"  Successful: {dashboard['trading']['trades_successful']}")
    print(f"  Failed: {dashboard['trading']['trades_failed']}")
    print(f"  Win Rate: {dashboard['trading']['win_rate']:.1f}%")
    
    print(f"\nAgent Metrics:")
    print(f"  Total Requests: {dashboard['agent']['requests_total']}")
    
    print(f"\nSystem Metrics:")
    print(f"  API Requests: {dashboard['system']['api_requests_total']}")
    print(f"  API Errors: {dashboard['system']['api_errors_total']}")
    print(f"  Memory Usage: {dashboard['system']['memory_usage_percent']}%")
    print(f"  CPU Usage: {dashboard['system']['cpu_usage_percent']}%")
    
    print(f"\nRisk Metrics:")
    print(f"  Portfolio Value: ${dashboard['risk']['portfolio_value']:,.2f}")
    print(f"  Risk Exposure: {dashboard['risk']['risk_exposure_percent']}%")
    print(f"  Drawdown: {dashboard['risk']['drawdown_percent']}%")
    
    print("\n✅ Metrics examples completed\n")


async def example_alerts():
    """Example: Alert system"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Alert System")
    print("="*60 + "\n")
    
    alert_manager = get_alert_manager()
    
    # Add alert channel
    alert_manager.add_channel("console", ConsoleChannel(colorize=True))
    
    # Define alert rules
    rules = [
        AlertRule(
            name="trade_failed",
            severity=AlertSeverity.ERROR,
            message_template="Trade execution failed: {error}",
            channels=["console"],
            cooldown_minutes=0,  # No cooldown for demo
        ),
        AlertRule(
            name="circuit_breaker",
            severity=AlertSeverity.CRITICAL,
            message_template="Circuit breaker triggered for {symbol}: {reason}",
            channels=["console"],
            cooldown_minutes=0,
        ),
        AlertRule(
            name="high_drawdown",
            severity=AlertSeverity.WARNING,
            message_template="Portfolio drawdown high: {drawdown}%",
            channels=["console"],
            cooldown_minutes=0,
        ),
    ]
    
    for rule in rules:
        alert_manager.add_rule(rule)
    
    print("🚨 Triggering example alerts...\n")
    
    # Trigger alerts
    await alert_manager.trigger("trade_failed", {
        "error": "Network timeout",
        "order_id": "ORD-123",
        "symbol": "BTC/USD",
    })
    
    time.sleep(0.5)
    
    await alert_manager.trigger("circuit_breaker", {
        "symbol": "EUR/USD",
        "reason": "Volatility exceeded threshold (3.5%)",
    })
    
    time.sleep(0.5)
    
    await alert_manager.trigger("high_drawdown", {
        "drawdown": 15.5,
        "portfolio_value": 85000,
    })
    
    # Get alert statistics
    print("\n" + "-" * 60)
    stats = alert_manager.get_alert_stats()
    print(f"\nAlert Statistics:")
    print(f"  Total Rules: {stats['total_rules']}")
    print(f"  Total Channels: {stats['total_channels']}")
    print(f"  Alerts Triggered:")
    for rule, count in stats['alert_counts'].items():
        print(f"    - {rule}: {count}")
    
    print("\n✅ Alert examples completed\n")


async def example_integrated():
    """Example: Integrated logging, metrics, and alerts"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Integrated Trading Workflow")
    print("="*60 + "\n")
    
    logger = get_logger("trading.workflow")
    metrics = get_metrics_tracker()
    alert_manager = get_alert_manager()
    
    # Setup alert manager
    alert_manager.add_channel("console", ConsoleChannel(colorize=True))
    alert_manager.add_rule(AlertRule(
        name="trade_failed",
        severity=AlertSeverity.ERROR,
        message_template="Trade failed: {error}",
        channels=["console"],
        cooldown_minutes=0,
    ))
    
    print("🔄 Simulating integrated trading workflow...\n")
    
    # Simulate a trade lifecycle
    trade_id = "TRD-789-XYZ"
    
    with correlation_context(trade_id):
        # 1. Trade request received
        logger.info("Trade request received", extra_fields={
            "trade_id": trade_id,
            "symbol": "EUR/USD",
            "quantity": 10000,
        })
        metrics.increment_counter("api_requests_total", 1)
        
        # 2. Validate trade
        with Timer("trade_validation_duration_seconds"):
            time.sleep(0.05)  # Simulate validation
            logger.info("Trade validation completed")
        
        # 3. Risk check
        logger.info("Performing risk check")
        metrics.set_gauge("risk_exposure_percent", 28.5)
        
        # 4. Execute trade
        logger.info("Executing trade")
        with Timer("order_execution_time_seconds"):
            time.sleep(0.1)  # Simulate execution
            
            # Simulate success
            success = True
            if success:
                logger.info("Trade executed successfully", extra_fields={
                    "execution_price": 1.0850,
                    "execution_time_ms": 100,
                })
                metrics.increment_counter("trades_total", 1)
                metrics.increment_counter("trades_successful", 1)
            else:
                logger.error("Trade execution failed", extra_fields={
                    "error": "Insufficient liquidity",
                })
                metrics.increment_counter("trades_total", 1)
                metrics.increment_counter("trades_failed", 1)
                await alert_manager.trigger("trade_failed", {
                    "error": "Insufficient liquidity",
                    "trade_id": trade_id,
                })
        
        # 5. Update portfolio
        metrics.set_gauge("portfolio_value", 102500.0)
        logger.info("Portfolio updated", extra_fields={
            "new_value": 102500.0,
            "pnl": 2500.0,
        })
    
    print("\n✅ Integrated workflow completed\n")


async def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("SelamAI Logging & Monitoring System - Examples")
    print("="*60)
    
    try:
        # Run examples
        example_logging()
        example_metrics()
        await example_alerts()
        await example_integrated()
        
        print("\n" + "="*60)
        print("All examples completed successfully! ✅")
        print("="*60)
        print("\nNext steps:")
        print("  1. View API documentation: http://localhost:8000/docs")
        print("  2. Check metrics endpoint: http://localhost:8000/api/metrics/dashboard")
        print("  3. Read full documentation: docs/MONITORING.md")
        print("  4. Configure alerts: config/monitoring/alerts.yaml")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
