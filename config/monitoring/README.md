# Monitoring Configuration

This directory contains configuration files for the SelamAI logging, metrics, and alerting system.

## Files

### logging.yaml
Logging configuration including:
- Log levels and formats
- Output sinks (console, file, external)
- Rotation policies
- Retention settings
- Performance logging options

### metrics.yaml
Metrics collection configuration including:
- Metric categories (agent, trading, risk, system)
- Collection intervals
- Storage settings
- Publishing targets (database, WebSocket, Prometheus)
- Alert thresholds

### alerts.yaml
Alert configuration including:
- Alert channels (email, Slack, webhook, console)
- Alert rules with severity levels
- Cooldown periods
- Rate limiting
- Alert history retention

## Directories

### prometheus/
Prometheus configuration files:
- `prometheus.yml`: Prometheus scrape configuration
- `alerts.yml`: Prometheus alert rules

### grafana/dashboards/
Grafana dashboard templates:
- `selamai-overview.json`: Main dashboard with trading, system, and agent metrics

## Quick Start

### 1. Basic Setup (Development)

The default configuration works out of the box for development:

```bash
# Start the API server
python backend/api.py
```

Logs will be written to:
- Console (colored, human-readable)
- `logs/selamai.log` (JSON format)
- `logs/errors.log` (errors only)

### 2. Enable Email Alerts

1. Edit `alerts.yaml`:
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

### 3. Enable Slack Alerts

1. Create a Slack webhook: https://api.slack.com/messaging/webhooks

2. Edit `alerts.yaml`:
```yaml
alerts:
  channels:
    slack:
      enabled: true
```

3. Set environment variable:
```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
export SLACK_CHANNEL="#alerts"
```

### 4. Enable Prometheus

1. Install Prometheus: https://prometheus.io/download/

2. Configure Prometheus to scrape metrics:
```bash
# Use the provided configuration
prometheus --config.file=config/monitoring/prometheus/prometheus.yml
```

3. Access Prometheus UI: http://localhost:9090

### 5. Setup Grafana

1. Install Grafana: https://grafana.com/grafana/download

2. Add Prometheus data source:
   - URL: http://localhost:9090
   - Access: Server

3. Import dashboard:
   - Go to: Dashboards → Import
   - Upload: `grafana/dashboards/selamai-overview.json`

4. Access Grafana: http://localhost:3000

## Environment Variables

All configuration files support environment variable substitution using the syntax: `${VAR_NAME:default_value}`

Common environment variables:

```bash
# Logging
export LOG_LEVEL="INFO"
export LOG_FORMAT="json"

# Email alerts
export SMTP_HOST="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USER="alerts@example.com"
export SMTP_PASSWORD="your-password"
export ALERT_FROM_EMAIL="alerts@selamai.com"
export ALERT_TO_EMAIL="admin@selamai.com"

# Slack alerts
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
export SLACK_CHANNEL="#alerts"

# OpenTelemetry
export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4317"
export OTEL_AUTH_HEADER="Bearer your-token"

# Webhook alerts
export ALERT_WEBHOOK_URL="https://your-webhook.com/alerts"
export ALERT_WEBHOOK_AUTH="Bearer your-token"
```

## Production Setup

### 1. Centralized Logging

For production, consider using a centralized logging solution:

**Option A: ELK Stack (Elasticsearch, Logstash, Kibana)**

```yaml
# logging.yaml
exporters:
  elasticsearch:
    enabled: true
    hosts: ["http://elasticsearch:9200"]
    index: "selamai-logs"
```

**Option B: Grafana Loki**

```yaml
# logging.yaml
exporters:
  loki:
    enabled: true
    url: "http://loki:3100/loki/api/v1/push"
```

### 2. Metrics Storage

For long-term metrics storage:

```yaml
# metrics.yaml
metrics:
  storage:
    type: database  # Instead of memory
    retention_hours: 2160  # 90 days
```

### 3. High Availability

For production environments:

1. **Multiple Instances**: Run multiple API servers behind a load balancer
2. **Shared Storage**: Use centralized logging and metrics storage
3. **Alert Aggregation**: Configure alert manager to deduplicate alerts
4. **Backup**: Regular backups of logs and metrics

### 4. Security

1. **TLS**: Enable TLS for external exporters
2. **Authentication**: Add authentication to metrics endpoints
3. **Rate Limiting**: Configure rate limits to prevent abuse
4. **Access Control**: Restrict access to sensitive endpoints

## Testing

Test your monitoring setup:

```bash
# Test logging
python -c "
from backend.logging_monitoring import get_logger
logger = get_logger('test')
logger.info('Test log message')
"

# Test metrics
curl http://localhost:8000/api/metrics/dashboard

# Test alerts
curl -X POST http://localhost:8000/api/alerts/test/trade_failed

# Test Prometheus metrics
curl http://localhost:8000/api/metrics/prometheus
```

## Troubleshooting

### Issue: Logs not appearing

**Solution**:
1. Check log directory exists: `mkdir -p logs`
2. Verify permissions: `chmod 755 logs`
3. Check disk space: `df -h`
4. Review log level configuration

### Issue: Metrics endpoint returns empty

**Solution**:
1. Ensure middleware is installed in FastAPI app
2. Generate some traffic to create metrics
3. Check retention period hasn't expired old metrics

### Issue: Alerts not firing

**Solution**:
1. Verify channel configuration (email/Slack credentials)
2. Check cooldown period settings
3. Test alert rule: `POST /api/alerts/test/{rule_name}`
4. Review alert manager logs

### Issue: Prometheus not scraping

**Solution**:
1. Verify Prometheus configuration
2. Check API server is accessible from Prometheus
3. Ensure metrics endpoint is responding: `curl http://localhost:8000/api/metrics/prometheus`
4. Review Prometheus logs

## Performance Tuning

### High-Volume Environments

For high-throughput scenarios:

```yaml
# logging.yaml
logging:
  format: text  # Faster than JSON
  performance:
    log_slow_requests: false  # Reduce overhead
    slow_threshold_ms: 5000   # Higher threshold

# metrics.yaml
metrics:
  collection_interval: 300  # Less frequent collection
  storage:
    retention_hours: 24     # Shorter retention
```

### Resource-Constrained Environments

For limited resources:

```yaml
# logging.yaml
logging:
  sinks:
    file:
      rotation:
        max_size: 5242880  # 5MB (smaller files)
        backup_count: 5    # Fewer backups

# metrics.yaml
metrics:
  storage:
    retention_hours: 24  # 1 day only
```

## Monitoring the Monitor

Monitor the monitoring system itself:

- Check log file sizes: `du -h logs/`
- Monitor memory usage of metrics tracker
- Track alert rate and volume
- Review cleanup job performance

## Support

For help:

1. Read the documentation: `docs/MONITORING.md`
2. Check API documentation: http://localhost:8000/docs
3. Run tests: `pytest backend/tests/test_logging.py -v`
4. Review configuration: This directory

## References

- [Full Documentation](../../docs/MONITORING.md)
- [Prometheus Setup](https://prometheus.io/docs/prometheus/latest/getting_started/)
- [Grafana Getting Started](https://grafana.com/docs/grafana/latest/getting-started/)
- [OpenTelemetry](https://opentelemetry.io/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
