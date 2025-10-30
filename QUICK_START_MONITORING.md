# Quick Start: Monitoring System

## 🚀 Get Started in 5 Minutes

### 1. Start the API
```bash
# Install dependencies
pip install -r backend/requirements.txt

# Start server (monitoring auto-initializes)
python backend/api.py
```

You'll see:
```
🚀 Initializing SelamAI Monitoring System...
   ✅ Logging configured
   ✅ Metrics tracker initialized
   ✅ Console alert channel added
   ✅ Alert manager configured with 14 rules
✅ Monitoring system initialized successfully!
```

### 2. View Metrics
```bash
# Get dashboard metrics
curl http://localhost:8000/api/metrics/dashboard

# Get monitoring status
curl http://localhost:8000/api/monitoring/status

# Get all metrics
curl http://localhost:8000/api/metrics
```

### 3. Test Alerts
```bash
# Trigger a test alert
curl -X POST http://localhost:8000/api/alerts/test/trade_failed

# View alert statistics
curl http://localhost:8000/api/alerts/stats
```

### 4. View Logs
```bash
# Logs are automatically written to:
tail -f logs/selamai.log      # All logs (JSON format)
tail -f logs/errors.log       # Errors only
```

### 5. Explore API Documentation
```
Open: http://localhost:8000/docs
```

## 📝 Basic Usage Examples

### Logging
```python
from backend.logging_monitoring import get_logger, correlation_context

logger = get_logger(__name__)

# Simple log
logger.info("Operation completed")

# With extra data
logger.info("Trade executed", extra_fields={
    "symbol": "EUR/USD",
    "profit": 150.50
})

# With correlation tracking
with correlation_context("trade-123"):
    logger.info("Step 1")
    logger.info("Step 2")  # Both have same correlation_id
```

### Metrics
```python
from backend.logging_monitoring import get_metrics_tracker, Timer

metrics = get_metrics_tracker()

# Count something
metrics.increment_counter("trades_total", 1)

# Track a value
metrics.set_gauge("portfolio_value", 100000.0)

# Time an operation
with Timer("order_execution_time_seconds"):
    execute_order()
```

### Alerts
```python
from backend.logging_monitoring import get_alert_manager

alert_manager = get_alert_manager()

# Trigger an alert
await alert_manager.trigger("circuit_breaker_triggered", {
    "symbol": "BTC/USD",
    "reason": "High volatility"
})
```

## 🎯 Key Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/metrics/dashboard` | Dashboard metrics (trading, system, agent, risk) |
| `GET /api/metrics/{name}` | Specific metric with statistics |
| `GET /api/monitoring/status` | Monitoring system status |
| `GET /api/alerts/stats` | Alert statistics |
| `POST /api/alerts/test/{rule}` | Test an alert rule |

## 📊 Dashboard Metrics Format

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

## ⚙️ Configuration

### Enable Email Alerts

1. Edit `config/monitoring/alerts.yaml`:
```yaml
alerts:
  channels:
    email:
      enabled: true
```

2. Set environment variables:
```bash
export SMTP_HOST="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USER="your-email@gmail.com"
export SMTP_PASSWORD="your-app-password"
export ALERT_FROM_EMAIL="alerts@selamai.com"
export ALERT_TO_EMAIL="admin@selamai.com"
```

### Enable Slack Alerts

1. Create Slack webhook: https://api.slack.com/messaging/webhooks

2. Set environment variable:
```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

3. Enable in `config/monitoring/alerts.yaml`:
```yaml
alerts:
  channels:
    slack:
      enabled: true
```

### Customize Log Level

Edit `config/monitoring/logging.yaml`:
```yaml
logging:
  level: DEBUG  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

## 🧪 Run Tests

```bash
# All monitoring tests
pytest backend/tests/test_logging.py backend/tests/test_metrics.py backend/tests/test_alerting.py -v

# Run examples
python backend/logging_monitoring/examples.py
```

## 📚 Learn More

- **Full Documentation**: [docs/MONITORING.md](docs/MONITORING.md)
- **Configuration Guide**: [config/monitoring/README.md](config/monitoring/README.md)
- **API Docs**: http://localhost:8000/docs (when server is running)
- **Examples**: [backend/logging_monitoring/examples.py](backend/logging_monitoring/examples.py)

## 🐛 Troubleshooting

**Logs not appearing?**
- Check `logs/` directory exists and is writable
- Verify log level in `config/monitoring/logging.yaml`

**Metrics not showing?**
- Generate some API traffic first
- Check `/api/monitoring/status`

**Alerts not firing?**
- Check cooldown period hasn't been triggered recently
- Test with: `curl -X POST http://localhost:8000/api/alerts/test/trade_failed`
- Verify channel configuration (SMTP/Slack credentials)

## 💡 Tips

1. **Use correlation IDs** for tracking related operations
2. **Check dashboard endpoint** for ready-to-use metrics
3. **Monitor slow requests** - automatically logged when > 1 second
4. **Review alert stats** to tune cooldown periods
5. **Enable JSON logs** in production for easy parsing

## 🎉 That's It!

You now have enterprise-grade monitoring for your trading platform!

For more details, see the full documentation at [docs/MONITORING.md](docs/MONITORING.md).
