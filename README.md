# SelamAI - AI-Powered Trading Platform

A modern AI-powered trading platform with comprehensive configuration management, autonomous trading agents, and a professional dashboard landing page.

## Features

### Frontend
- **Modern Design**: Clean, professional aesthetic inspired by OpenAI, ChatGPT, Notion, and Linear
- **Fully Responsive**: Mobile-first design that works beautifully across all screen sizes
- **Interactive Components**: Smooth animations powered by Framer Motion
- **shadcn/ui**: Built with high-quality, accessible UI components
- **TypeScript**: Type-safe development with Next.js 16 and React

### Backend & AI Core
- **Configuration Management**: YAML-based configuration with typed validation using Pydantic
- **AI Trading Agents**: Autonomous trading agents with customizable behavior
- **Risk Management**: Comprehensive risk management profiles (conservative, aggressive)
- **Trading Strategies**: Multiple strategy configurations (momentum, mean reversion)
- **Multi-Asset Support**: Forex, commodities, cryptocurrencies, and indices
- **Hot-Reloading**: Configuration changes without service restart
- **API Endpoints**: RESTful API for configuration inspection and management

### Logging & Monitoring
- **Structured Logging**: JSON-formatted logs with correlation IDs for request tracing
- **Performance Metrics**: Real-time tracking of trading, agent, and system metrics
- **Alerting System**: Multi-channel alerts (email, Slack, webhooks) for critical events
- **Dashboard Integration**: WebSocket streams for real-time frontend visualization
- **External Exporters**: Prometheus and OpenTelemetry support for production monitoring
- **Comprehensive Observability**: Track trades, decisions, performance, and errors for compliance

## Tech Stack

### Frontend
- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS v4
- **UI Components**: shadcn/ui
- **Animations**: Framer Motion
- **Icons**: Lucide React

### Backend
- **Language**: Python 3.10+
- **Validation**: Pydantic 2.0+
- **API Framework**: FastAPI
- **Configuration**: YAML with environment overrides
- **Testing**: pytest
- **Monitoring**: Structured logging, metrics tracking, alerting
- **Observability**: Prometheus, OpenTelemetry, Grafana support

## Sections

1. **Header**: Sticky navigation with smooth scroll effects and mobile menu
2. **Hero Section**: Eye-catching headline with gradient backgrounds and interactive preview cards
3. **Dashboard Preview**: Showcase of API usage metrics, credits, and available AI models
4. **Feature Highlights**: Key product features with hover effects and animations
5. **API Playground Preview**: Code editor simulation with multi-language support
6. **Documentation**: Resources and guides section
7. **Pricing**: Clear pricing tiers with comparison
8. **Early Access**: Call-to-action for sign-up
9. **Footer**: Comprehensive links and social media integration

## Getting Started

### Frontend Setup

Install frontend dependencies:

```bash
npm install
```

Run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the landing page.

### Backend Setup

Install Python dependencies:

```bash
pip install -r backend/requirements.txt
```

Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your configuration
```

Start the configuration API:

```bash
python backend/api.py
```

Or with uvicorn:

```bash
uvicorn backend.api:app --reload --port 8000
```

The API will be available at [http://localhost:8000](http://localhost:8000)

### Configuration Management

See comprehensive documentation: [docs/CONFIGURATION.md](docs/CONFIGURATION.md)

Quick commands:

```bash
# Validate all configurations
python -m backend.config.cli validate

# Show specific configuration
python -m backend.config.cli show main
python -m backend.config.cli show strategy momentum

# List available configurations
python -m backend.config.cli list strategies
python -m backend.config.cli list agents
```

## Build for Production

### Frontend

```bash
npm run build
npm start
```

### Backend

```bash
# Set environment
export ENVIRONMENT=production

# Start with production settings
uvicorn backend.api:app --host 0.0.0.0 --port 8000
```

## Project Structure

```
├── app/                    # Next.js frontend
│   ├── layout.tsx          # Root layout with metadata
│   ├── page.tsx            # Main landing page
│   └── globals.css         # Global styles and theme
├── backend/                # Python backend
│   ├── config/             # Configuration management
│   │   ├── loader.py       # Config loader with Pydantic validation
│   │   ├── models.py       # Pydantic models for validation
│   │   └── cli.py          # CLI tool for config management
│   ├── logging_monitoring/ # Logging and monitoring system
│   │   ├── logger.py       # Structured logging with JSON format
│   │   ├── correlation.py  # Correlation ID management
│   │   ├── metrics.py      # Performance metrics tracker
│   │   ├── alerting.py     # Alert manager for critical events
│   │   ├── middleware.py   # FastAPI middleware for logging/metrics
│   │   ├── config.py       # Monitoring configuration loader
│   │   └── exporters/      # External system exporters
│   │       ├── prometheus.py
│   │       └── opentelemetry.py
│   ├── tests/              # Test suite
│   │   ├── test_config_loader.py
│   │   ├── test_logging.py
│   │   ├── test_metrics.py
│   │   └── test_alerting.py
│   ├── api.py              # FastAPI application
│   └── requirements.txt    # Python dependencies
├── config/                 # YAML configuration files
│   ├── main.yaml           # Main system configuration
│   ├── assets.yaml         # Trading assets definitions
│   ├── agents/             # AI agent configurations
│   │   ├── trading_agent.yaml
│   │   └── analysis_agent.yaml
│   ├── strategies/         # Trading strategy configurations
│   │   ├── momentum.yaml
│   │   └── mean_reversion.yaml
│   ├── risk/               # Risk management profiles
│   │   ├── default.yaml
│   │   └── aggressive.yaml
│   ├── monitoring/         # Monitoring configuration
│   │   ├── logging.yaml    # Logging configuration
│   │   ├── metrics.yaml    # Metrics configuration
│   │   ├── alerts.yaml     # Alert rules and channels
│   │   ├── prometheus/     # Prometheus configs
│   │   └── grafana/        # Grafana dashboards
│   └── environments/       # Environment-specific overrides
│       ├── development.yaml
│       ├── staging.yaml
│       └── production.yaml
├── components/
│   ├── landing/            # Landing page sections
│   │   ├── header.tsx
│   │   ├── hero.tsx
│   │   ├── dashboard-preview.tsx
│   │   ├── feature-highlights.tsx
│   │   ├── playground-preview.tsx
│   │   ├── documentation.tsx
│   │   ├── pricing.tsx
│   │   ├── early-access.tsx
│   │   └── footer.tsx
│   └── ui/                 # shadcn/ui components
├── docs/                   # Documentation
│   ├── CONFIGURATION.md    # Configuration guide
│   └── MONITORING.md       # Logging and monitoring guide
├── lib/
│   └── utils.ts            # Utility functions
├── logs/                   # Log files (auto-created)
│   ├── selamai.log         # Main log file (JSON format)
│   └── errors.log          # Error log file
├── .env.example            # Environment variables template
└── .gitignore              # Git ignore rules
```

## Design System

- **Color Palette**: Neutral grays with blue and purple accents
- **Typography**: Clean, modern fonts (Geist Sans)
- **Spacing**: Consistent spacing scale
- **Shadows**: Subtle elevation with soft shadows
- **Radius**: Rounded corners for a modern feel
- **Animations**: Smooth transitions and micro-interactions

## Accessibility

- Semantic HTML structure
- ARIA labels where appropriate
- Keyboard navigation support
- Focus indicators
- Screen reader friendly

## Configuration

SelamAI uses a comprehensive YAML-based configuration system with typed validation. Key features:

- **Environment-Specific Overrides**: Separate configs for development, staging, and production
- **Typed Validation**: Pydantic models ensure configuration correctness
- **Hot-Reloading**: Update configs without restarting (in development)
- **CLI Tools**: Inspect and validate configurations from command line
- **API Endpoints**: RESTful API for configuration management
- **Security**: Environment variable substitution for sensitive values

See [docs/CONFIGURATION.md](docs/CONFIGURATION.md) for detailed documentation.

## Logging and Monitoring

SelamAI includes a comprehensive logging, metrics, and alerting system:

- **Structured Logging**: JSON-formatted logs with correlation IDs for tracing
- **Performance Metrics**: Track trading, agent, and system performance
- **Alerting**: Multi-channel alerts for critical events (email, Slack, webhooks)
- **Dashboards**: Pre-configured Grafana dashboards for visualization
- **Exporters**: Prometheus and OpenTelemetry support

### Quick Start

```bash
# Logs are automatically enabled and written to logs/ directory
python backend/api.py

# View metrics
curl http://localhost:8000/api/metrics/dashboard

# Test an alert
curl -X POST http://localhost:8000/api/alerts/test/trade_failed
```

### API Endpoints

- `GET /api/metrics` - Get all metrics
- `GET /api/metrics/dashboard` - Get dashboard-formatted metrics
- `GET /api/metrics/{metric_name}` - Get specific metric summary
- `GET /api/metrics/prometheus` - Get metrics in Prometheus format
- `GET /api/alerts/stats` - Get alert statistics
- `POST /api/alerts/test/{rule_name}` - Test an alert rule

### Configuration

Monitoring configuration is in `config/monitoring/`:
- `logging.yaml` - Logging configuration
- `metrics.yaml` - Metrics collection settings
- `alerts.yaml` - Alert rules and channels
- `prometheus/` - Prometheus configuration
- `grafana/` - Grafana dashboard templates

See [docs/MONITORING.md](docs/MONITORING.md) for detailed documentation.

## Testing

### Backend Tests

```bash
# Install test dependencies
pip install -r backend/requirements.txt

# Run all tests
pytest backend/tests/

# Run with coverage
pytest backend/tests/ --cov=backend --cov-report=html

# Run specific test file
pytest backend/tests/test_config_loader.py -v
```

### Test Coverage

The test suite covers:
- Configuration loading and parsing
- Pydantic model validation
- Environment-specific overrides
- Configuration precedence rules
- Error handling and validation errors
- Deep merge functionality
- Logging and correlation IDs
- Metrics tracking and aggregation
- Alert triggering and cooldowns
- Middleware integration

## API Documentation

Once the backend server is running, access the interactive API documentation:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Security Best Practices

1. **Never commit secrets**: Use `.env` file for sensitive values
2. **Use .env.example**: Provide template with placeholder values
3. **Environment variables**: Reference sensitive values using `${VAR_NAME}` syntax
4. **Rotate credentials**: Regular rotation of API keys and passwords
5. **HTTPS in production**: Always use HTTPS for production deployments

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest backend/tests/`)
5. Validate configurations (`python -m backend.config.cli validate`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

MIT
