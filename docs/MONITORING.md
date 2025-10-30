# Monitoring, Logging, and Alerting Documentation

## Overview

SelamAI Trading Platform includes a comprehensive monitoring, logging, and alerting system designed for:

- **Observability**: Track system behavior, performance, and errors
- **Compliance**: Maintain audit trails for trading decisions and actions
- **Performance**: Identify bottlenecks and optimize system performance
- **Reliability**: Detect and respond to critical events in real-time

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Application Code                         │
│  (Backend API, AI Agents, Trading Engine, Data Services)   │
└───────────────┬─────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────┐
│              Logging & Monitoring Module                    │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Logger     │  │   Metrics    │  │   Alerts     │     │
│  │  (Structured)│  │   Tracker    │  │   Manager    │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                  │                  │              │
└─────────┼──────────────────┼──────────────────┼──────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
    ┌─────────┐        ┌─────────┐       ┌─────────┐
    │ Console │        │ Database│       │ Channels│
    │  Files  │        │ WebSocket│      │Email/Slack│
    │ External│        │Prometheus│      │ Webhook │
    └─────────┘        └─────────┘       └─────────┘
```

## Components

### 1. Structured Logging

#### Features

- **JSON Format**: Structured logs for easy parsing and analysis
- **Correlation IDs**: Track requests/trades across services
- **Multiple Sinks**: Console, file rotation, external services
- **Context Fields**: Automatically include relevant trading context

#### Usage

```python
from backend.logging_monitoring import get_logger, correlation_context

logger = get_logger(__name__)

# Basic logging
logger.info("Trade executed successfully")

# With extra fields
logger.info("Trade executed", extra_fields={
    "trade_id": "ABC123",
    "symbol": "EUR/USD",
    "quantity": 1000,
    "price": 1.0850,
})

# With correlation context
with correlation_context("trade-123"):
    logger.info("Processing trade")
    # All logs in this context will have correlation_id="trade-123"
```

#### Configuration

Located in `config/monitoring/logging.yaml`:

```yaml
logging:
  level: INFO                    # Log level
  format: json                   # json or text
  enable_correlation_ids: true   # Enable correlation tracking
  
  sinks:
    console:
      enabled: true
      level: INFO
      colorize: true
      
    file:
      enabled: true
      level: DEBUG
      path: logs/selamai.log
      rotation:
        max_size: 10485760  # 10MB
        backup_count: 10
```

### 2. Performance Metrics

#### Features

- **Counters**: Track cumulative values (total requests, trades)
- **Gauges**: Track point-in-time values (memory usage, portfolio value)
- **Histograms**: Track distributions (request latency, trade size)
- **Time Windows**: Filter metrics by time range
- **Summary Statistics**: Min, max, mean, median, percentiles

#### Metric Categories

**Agent Metrics**:
- `agent_requests_total`: Total AI agent requests
- `agent_requests_duration_seconds`: Agent response time
- `agent_decisions_total`: Total trading decisions made
- `agent_errors_total`: Total agent errors

**Trading Metrics**:
- `trades_total`: Total trades executed
- `trades_successful`: Successful trades
- `trades_failed`: Failed trades
- `order_execution_time_seconds`: Order execution latency
- `profit_loss_total`: Total profit/loss
- `win_rate_percent`: Win rate percentage

**Risk Metrics**:
- `risk_exposure_percent`: Current risk exposure
- `drawdown_percent`: Portfolio drawdown
- `portfolio_value`: Current portfolio value
- `circuit_breakers_triggered`: Circuit breaker activations

**System Metrics**:
- `api_requests_total`: Total API requests
- `api_request_duration_seconds`: API latency
- `api_errors_total`: API errors
- `memory_usage_percent`: Memory usage
- `cpu_usage_percent`: CPU usage

#### Usage

```python
from backend.logging_monitoring import get_metrics_tracker, Timer

metrics = get_metrics_tracker()

# Counter
metrics.increment_counter("trades_total", 1)

# Gauge
metrics.set_gauge("portfolio_value", 100000.0)

# Duration with Timer
with Timer("order_execution_time_seconds"):
    # Execute order
    execute_trade(order)

# Manual duration
metrics.record_duration("api_request", 0.5, labels={
    "endpoint": "/api/trades",
    "method": "POST",
})

# Get metrics summary
summary = metrics.get_metric_summary("api_request_duration_seconds", minutes=60)
print(f"P95 latency: {summary.p95}s")

# Get dashboard data
dashboard = metrics.get_dashboard_data()
print(f"Win rate: {dashboard['trading']['win_rate']}%")
```

#### Configuration

Located in `config/monitoring/metrics.yaml`:

```yaml
metrics:
  enabled: true
  collection_interval: 60  # seconds
  
  storage:
    type: memory           # memory, database, or both
    retention_hours: 168   # 7 days
    
  publishing:
    database:
      enabled: true
      batch_size: 100
      
    websocket:
      enabled: true
      channel: metrics
      throttle_ms: 1000
```

### 3. Alerting

#### Features

- **Multiple Channels**: Console, email, Slack, webhooks
- **Severity Levels**: Debug, Info, Warning, Error, Critical
- **Cooldown Periods**: Prevent alert spam
- **Rate Limiting**: Limit alerts per hour
- **Context Data**: Include relevant data in alerts

#### Alert Rules

Pre-configured alert rules in `config/monitoring/alerts.yaml`:

- **Trading**: Circuit breakers, trade failures, high failure rate
- **Risk**: Drawdown exceeded, margin calls, position limits
- **System**: High latency, error rate, database failures
- **Agent**: AI agent errors, timeouts

#### Usage

```python
from backend.logging_monitoring import get_alert_manager, AlertSeverity
from backend.logging_monitoring.alerting import AlertRule, ConsoleChannel

alert_manager = get_alert_manager()

# Add a rule
rule = AlertRule(
    name="high_latency",
    severity=AlertSeverity.WARNING,
    message_template="API latency high: {latency_ms}ms",
    channels=["console", "slack"],
    cooldown_minutes=10,
)
alert_manager.add_rule(rule)

# Add channels
alert_manager.add_channel("console", ConsoleChannel())

# Trigger an alert
await alert_manager.trigger("high_latency", {
    "latency_ms": 5000,
    "endpoint": "/api/trades",
})

# Convenience functions
from backend.logging_monitoring.alerting import (
    alert_circuit_breaker_triggered,
    alert_trade_failed,
    alert_high_drawdown,
)

await alert_circuit_breaker_triggered("BTC/USD", "Volatility exceeded threshold")
await alert_trade_failed("Network timeout", trade_id="123")
await alert_high_drawdown(25.5)
```

#### Configuration

Located in `config/monitoring/alerts.yaml`:

```yaml
alerts:
  enabled: true
  
  channels:
    email:
      enabled: false
      smtp_host: ${SMTP_HOST}
      smtp_port: 587
      from_address: alerts@selamai.com
      to_addresses:
        - admin@selamai.com
        
    slack:
      enabled: false
      webhook_url: ${SLACK_WEBHOOK_URL}
      channel: "#alerts"
      
    console:
      enabled: true
      colorize: true
      
  rules:
    circuit_breaker_triggered:
      severity: critical
      message: "Circuit breaker triggered for {symbol}"
      channels: [email, slack, console]
      cooldown_minutes: 5
```

## API Endpoints

### Metrics Endpoints

#### GET /api/metrics
Get all metrics (optionally filtered by time window)

**Query Parameters**:
- `minutes` (optional): Filter last N minutes

**Response**:
```json
{
  "trades_total": [
    {
      "value": 1.0,
      "timestamp": "2024-01-01T12:00:00Z",
      "labels": {"symbol": "EUR/USD"},
      "unit": null
    }
  ],
  ...
}
```

#### GET /api/metrics/dashboard
Get formatted metrics for dashboard visualization

**Response**:
```json
{
  "timestamp": "2024-01-01T12:00:00Z",
  "agent": {
    "requests_total": 100,
    "decisions_total": 80,
    "errors_total": 2,
    "avg_duration": 0.5
  },
  "trading": {
    "trades_total": 50,
    "trades_successful": 45,
    "trades_failed": 5,
    "win_rate": 90.0,
    "profit_loss_total": 1500.0
  },
  "system": {
    "api_requests_total": 500,
    "api_errors_total": 10,
    "memory_usage_percent": 75.0,
    "cpu_usage_percent": 60.0
  },
  "risk": {
    "risk_exposure_percent": 30.0,
    "drawdown_percent": 5.0,
    "portfolio_value": 100000.0
  }
}
```

#### GET /api/metrics/{metric_name}
Get summary statistics for a specific metric

**Response**:
```json
{
  "name": "api_request_duration_seconds",
  "count": 1000,
  "sum": 500.0,
  "min": 0.1,
  "max": 2.5,
  "mean": 0.5,
  "median": 0.45,
  "p95": 1.2,
  "p99": 1.8
}
```

#### GET /api/metrics/prometheus
Get metrics in Prometheus format

**Response** (text/plain):
```
# HELP api_requests_total Total API requests
# TYPE api_requests_total counter
api_requests_total 1000
```

### Alert Endpoints

#### GET /api/alerts/stats
Get alert statistics

**Response**:
```json
{
  "total_rules": 15,
  "total_channels": 3,
  "alert_counts": {
    "trade_failed": 5,
    "circuit_breaker_triggered": 1
  },
  "recent_alerts": 6
}
```

#### POST /api/alerts/test/{rule_name}
Test an alert rule (development only)

**Response**:
```json
{
  "rule": "trade_failed",
  "triggered": true,
  "message": "Alert triggered successfully"
}
```

## Integration with Frontend

### WebSocket Metrics Stream

Real-time metrics can be streamed to the frontend via WebSocket:

```javascript
// Frontend code
const ws = new WebSocket('ws://localhost:8000/ws/metrics');

ws.onmessage = (event) => {
  const metrics = JSON.parse(event.data);
  updateDashboard(metrics);
};
```

### Dashboard Integration

Fetch metrics for dashboard charts:

```javascript
// Fetch dashboard metrics
const response = await fetch('/api/metrics/dashboard');
const data = await response.json();

// Update charts
updateTradeChart(data.trading);
updateSystemChart(data.system);
updateRiskChart(data.risk);
```

## External Integrations

### Prometheus

1. **Configure Prometheus** (see `config/monitoring/prometheus/prometheus.yml`)

```yaml
scrape_configs:
  - job_name: 'selamai-backend'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/api/metrics/prometheus'
```

2. **Enable in configuration**:

```yaml
# config/monitoring/logging.yaml
exporters:
  prometheus:
    enabled: true
    port: 9090
```

3. **Install dependencies** (for production):

```bash
pip install prometheus-client
```

### Grafana

1. **Import dashboard** from `config/monitoring/grafana/dashboards/selamai-overview.json`

2. **Configure data source**: Point Grafana to your Prometheus instance

3. **View metrics**: Access pre-configured dashboard with:
   - Trading metrics (trades, win rate, P&L)
   - System metrics (API latency, error rate)
   - Agent metrics (request rate, response time)
   - Resource usage (CPU, memory)

### OpenTelemetry

1. **Configure OpenTelemetry**:

```yaml
# config/monitoring/logging.yaml
exporters:
  opentelemetry:
    enabled: true
    endpoint: http://localhost:4317
    service_name: selamai-trading
```

2. **Install dependencies** (for production):

```bash
pip install opentelemetry-api opentelemetry-sdk
pip install opentelemetry-exporter-otlp
```

### Email Alerts

Configure SMTP settings:

```yaml
# config/monitoring/alerts.yaml
alerts:
  channels:
    email:
      enabled: true
      smtp_host: smtp.gmail.com
      smtp_port: 587
      smtp_user: ${SMTP_USER}
      smtp_password: ${SMTP_PASSWORD}
      from_address: alerts@selamai.com
      to_addresses:
        - admin@selamai.com
```

Set environment variables:

```bash
export SMTP_USER="your-email@gmail.com"
export SMTP_PASSWORD="your-app-password"
```

### Slack Alerts

1. **Create Slack webhook**: https://api.slack.com/messaging/webhooks

2. **Configure webhook**:

```yaml
# config/monitoring/alerts.yaml
alerts:
  channels:
    slack:
      enabled: true
      webhook_url: ${SLACK_WEBHOOK_URL}
      channel: "#alerts"
```

3. **Set environment variable**:

```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

## Log Retention

### File Rotation

Logs are automatically rotated based on size:

```yaml
logging:
  sinks:
    file:
      rotation:
        max_size: 10485760  # 10MB
        backup_count: 10    # Keep 10 backups
```

### Cleanup

Old logs are automatically cleaned up based on retention policy:

```yaml
logging:
  retention:
    days: 30        # Keep logs for 30 days
    compress: true  # Compress old logs
```

### Manual Cleanup

```bash
# Remove logs older than 30 days
find logs/ -name "*.log.*" -mtime +30 -delete

# Compress old logs
find logs/ -name "*.log.*" -mtime +7 -exec gzip {} \;
```

## Best Practices

### 1. Use Correlation IDs

Always use correlation IDs for tracking requests/trades:

```python
from backend.logging_monitoring import correlation_context

with correlation_context(trade_id):
    process_trade(trade)
    # All logs, metrics, and alerts will include this correlation ID
```

### 2. Log at Appropriate Levels

- **DEBUG**: Detailed diagnostic information
- **INFO**: General informational messages
- **WARNING**: Warning messages for non-critical issues
- **ERROR**: Error messages for failures
- **CRITICAL**: Critical failures requiring immediate attention

### 3. Include Context

Always include relevant context in logs and alerts:

```python
logger.info("Trade executed", extra_fields={
    "trade_id": trade.id,
    "symbol": trade.symbol,
    "quantity": trade.quantity,
    "execution_time_ms": execution_time,
})
```

### 4. Monitor Key Metrics

Essential metrics to monitor:

- **Trading**: Win rate, P&L, trade execution time
- **Risk**: Drawdown, exposure, margin usage
- **System**: API latency, error rate, resource usage
- **Agents**: Response time, decision accuracy

### 5. Set Up Alerts

Configure alerts for critical events:

- Circuit breaker triggers
- High trade failure rate
- Excessive drawdown
- System errors
- Resource exhaustion

## Testing

Run the test suite:

```bash
# All tests
pytest backend/tests/test_logging.py backend/tests/test_metrics.py backend/tests/test_alerting.py -v

# With coverage
pytest backend/tests/test_logging.py backend/tests/test_metrics.py backend/tests/test_alerting.py --cov=backend.logging_monitoring --cov-report=html

# Specific test
pytest backend/tests/test_logging.py::TestCorrelationID -v
```

## Troubleshooting

### Logs Not Appearing

1. Check log level configuration
2. Verify log directory permissions
3. Check disk space
4. Ensure logging is initialized: `setup_logging()`

### Metrics Not Recording

1. Verify metrics are being recorded: `metrics.increment_counter()`
2. Check retention period - old metrics may have been cleaned up
3. Ensure middleware is installed in FastAPI app

### Alerts Not Firing

1. Check alert cooldown period
2. Verify rate limiting settings
3. Ensure channels are configured correctly
4. Test alert: `POST /api/alerts/test/{rule_name}`

### High Memory Usage

1. Reduce metrics retention period
2. Increase cleanup frequency
3. Limit deque maxlen in MetricsTracker
4. Enable database storage instead of memory

## Performance Considerations

- **Logging**: JSON formatting is slightly slower than text; use text format for high-throughput scenarios
- **Metrics**: Memory-based storage is fastest but limited; use database for long-term storage
- **Alerts**: Cooldown periods prevent alert storms and reduce overhead
- **Middleware**: Minimal overhead (~1-2ms per request)

## Security

- **Sensitive Data**: Never log sensitive data (passwords, API keys, PII)
- **Access Control**: Restrict access to logs and metrics endpoints
- **Encryption**: Use TLS for external exporters
- **Rotation**: Regular log rotation prevents disk exhaustion
- **Retention**: Comply with data retention regulations

## Support

For issues or questions:

1. Check logs: `logs/selamai.log`
2. Review configuration: `config/monitoring/`
3. Test endpoints: `/api/metrics`, `/api/alerts/stats`
4. Run tests: `pytest backend/tests/`

## Future Enhancements

- [ ] Database persistence for metrics
- [ ] Real-time WebSocket streaming
- [ ] Advanced alerting rules with ML
- [ ] Distributed tracing
- [ ] Log aggregation (ELK stack)
- [ ] Custom dashboard builder
- [ ] Mobile alerts (push notifications)
- [ ] Anomaly detection
