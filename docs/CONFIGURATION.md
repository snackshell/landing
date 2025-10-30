# Configuration Management Guide

## Overview

SelamAI uses a comprehensive YAML-based configuration system with typed validation using Pydantic models. This ensures type safety, helpful error messages, and consistent configuration across all modules.

## Table of Contents

- [Directory Structure](#directory-structure)
- [Configuration Files](#configuration-files)
- [Environment-Specific Overrides](#environment-specific-overrides)
- [Configuration Precedence](#configuration-precedence)
- [Loading Configurations](#loading-configurations)
- [Environment Variables](#environment-variables)
- [Hot-Reloading](#hot-reloading)
- [CLI Tools](#cli-tools)
- [API Endpoints](#api-endpoints)
- [Validation](#validation)
- [Security Best Practices](#security-best-practices)
- [Examples](#examples)

## Directory Structure

```
config/
├── main.yaml                    # Main system configuration
├── assets.yaml                  # Trading assets definitions
├── agents/                      # AI agent configurations
│   ├── trading_agent.yaml
│   └── analysis_agent.yaml
├── strategies/                  # Trading strategy configurations
│   ├── momentum.yaml
│   └── mean_reversion.yaml
├── risk/                        # Risk management profiles
│   ├── default.yaml
│   └── aggressive.yaml
└── environments/                # Environment-specific overrides
    ├── development.yaml
    ├── staging.yaml
    └── production.yaml
```

## Configuration Files

### Main Configuration (`config/main.yaml`)

The main configuration file contains system-wide settings:

```yaml
system:
  name: "SelamAI"
  version: "1.0.0"
  environment: "development"
  debug: true
  log_level: "INFO"

api:
  host: "0.0.0.0"
  port: 8000
  cors_origins:
    - "http://localhost:3000"

ai:
  provider: "openai"
  model: "gpt-4"
  temperature: 0.7
  max_tokens: 2000
```

### Assets Configuration (`config/assets.yaml`)

Defines all tradable assets with their specifications:

```yaml
assets:
  forex:
    enabled: true
    pairs:
      EURUSD:
        name: "Euro/US Dollar"
        pip_value: 0.0001
        min_lot_size: 0.01
        max_lot_size: 100
        margin_requirement: 0.02
        enabled: true
```

### Strategy Configuration (`config/strategies/*.yaml`)

Each strategy has its own configuration file:

```yaml
strategy:
  name: "momentum"
  type: "trend_following"
  parameters:
    primary_timeframe: "1h"
    indicators:
      ema_fast:
        period: 20
        type: "exponential"
```

### Risk Management Configuration (`config/risk/*.yaml`)

Risk profiles define risk management rules:

```yaml
risk_management:
  name: "default"
  account:
    max_risk_per_trade: 0.02
    max_daily_loss: 0.05
  position:
    max_position_size: 0.10
    max_positions_total: 10
```

### Agent Configuration (`config/agents/*.yaml`)

AI agent configurations:

```yaml
agent:
  name: "trading_agent"
  type: "autonomous_trader"
  core:
    model: "gpt-4"
    temperature: 0.3
  capabilities:
    market_analysis: true
    trade_execution: true
```

## Environment-Specific Overrides

The system supports three environments:

- **Development**: Local development with debug enabled
- **Staging**: Pre-production testing environment
- **Production**: Live production environment

### Setting the Environment

```bash
export ENVIRONMENT=production
```

Or in `.env` file:

```
ENVIRONMENT=production
```

### Override Files

Environment-specific settings are in `config/environments/{environment}.yaml`:

**development.yaml**:
```yaml
system:
  debug: true
  log_level: "DEBUG"

security:
  require_https: false
```

**production.yaml**:
```yaml
system:
  debug: false
  log_level: "WARNING"

security:
  require_https: true
```

## Configuration Precedence

Configuration values are loaded with the following precedence (later overrides earlier):

1. Base configuration file (e.g., `config/main.yaml`)
2. Environment-specific overrides (`config/environments/{environment}.yaml`)
3. Environment variables (for sensitive values)

### Example Precedence

**Base config** (`main.yaml`):
```yaml
api:
  port: 8000
  debug: true
```

**Production override** (`environments/production.yaml`):
```yaml
api:
  debug: false
```

**Result in production**:
```yaml
api:
  port: 8000      # From base
  debug: false    # Overridden by production
```

## Loading Configurations

### Python Usage

```python
from backend.config.loader import ConfigLoader

# Initialize loader
loader = ConfigLoader(
    config_dir="config",
    environment="production",
    enable_hot_reload=False
)

# Load main configuration
main_config = loader.load_main_config()
print(f"API Port: {main_config.api.port}")

# Load assets configuration
assets_config = loader.load_assets_config()
for pair_name, pair_config in assets_config.assets.forex.pairs.items():
    print(f"{pair_name}: {pair_config.name}")

# Load strategy configuration
momentum_strategy = loader.load_strategy_config("momentum")
print(f"Strategy: {momentum_strategy.name}")

# Load risk profile
risk_config = loader.load_risk_config("default")
print(f"Max risk per trade: {risk_config.account.max_risk_per_trade}")

# Load agent configuration
agent_config = loader.load_agent_config("trading_agent")
print(f"Agent model: {agent_config.core.model}")
```

### TypeScript/Next.js Usage

```typescript
import fs from 'fs';
import yaml from 'js-yaml';
import path from 'path';

// Load configuration
export function loadConfig<T>(filePath: string): T {
  const fullPath = path.join(process.cwd(), 'config', filePath);
  const fileContents = fs.readFileSync(fullPath, 'utf8');
  return yaml.load(fileContents) as T;
}

// Usage
const mainConfig = loadConfig('main.yaml');
const assetsConfig = loadConfig('assets.yaml');
```

## Environment Variables

Sensitive values should never be hardcoded in YAML files. Use environment variable substitution:

### In YAML Files

```yaml
database:
  host: "${DATABASE_HOST:-localhost}"
  password: "${DATABASE_PASSWORD}"

broker:
  mt5:
    account: "${MT5_ACCOUNT}"
    password: "${MT5_PASSWORD}"
```

### Environment Variable Syntax

- `${VAR_NAME}`: Substitute variable, keep original if not found
- `${VAR_NAME:-default}`: Substitute variable, use default if not found

### Setting Environment Variables

**Using .env file**:

```bash
# Copy example file
cp .env.example .env

# Edit .env with your values
DATABASE_PASSWORD=secure_password
MT5_ACCOUNT=12345678
MT5_PASSWORD=trading_password
```

**Using export**:

```bash
export DATABASE_PASSWORD=secure_password
export MT5_ACCOUNT=12345678
```

## Hot-Reloading

Enable automatic configuration reloading when files change:

```python
loader = ConfigLoader(
    config_dir="config",
    environment="development",
    enable_hot_reload=True  # Enable hot-reload
)
```

**Note**: Hot-reloading is recommended for development only. In production, restart the application to load new configurations.

## CLI Tools

### Configuration CLI

Inspect and validate configurations from the command line:

```bash
# Show configuration info
python -m backend.config.cli info

# List available configurations
python -m backend.config.cli list strategies
python -m backend.config.cli list agents
python -m backend.config.cli list risk

# Show specific configuration
python -m backend.config.cli show main
python -m backend.config.cli show assets
python -m backend.config.cli show strategy momentum
python -m backend.config.cli show agent trading_agent
python -m backend.config.cli show risk default

# Validate configurations
python -m backend.config.cli validate
python -m backend.config.cli validate strategies

# Use different environment
python -m backend.config.cli --environment production show main
```

## API Endpoints

Start the configuration API server:

```bash
# Install dependencies
pip install -r backend/requirements.txt

# Start server
python backend/api.py

# Or with uvicorn
uvicorn backend.api:app --reload
```

### Available Endpoints

```
GET  /                              # API info
GET  /health                        # Health check
GET  /api/config/info               # Loader information
GET  /api/config/main               # Main configuration
GET  /api/config/assets             # Assets configuration
GET  /api/config/strategies         # List strategies
GET  /api/config/strategies/{name}  # Get strategy
GET  /api/config/agents             # List agents
GET  /api/config/agents/{name}      # Get agent
GET  /api/config/risk               # List risk profiles
GET  /api/config/risk/{name}        # Get risk profile
POST /api/config/reload             # Reload all configs
GET  /api/config/validate           # Validate all configs
```

### Example API Usage

```bash
# Get main configuration
curl http://localhost:8000/api/config/main

# Get strategy configuration
curl http://localhost:8000/api/config/strategies/momentum

# Reload configurations
curl -X POST http://localhost:8000/api/config/reload

# Validate all configurations
curl http://localhost:8000/api/config/validate
```

## Validation

All configurations are validated using Pydantic models with helpful error messages.

### Example Validation Error

```yaml
# Invalid configuration
api:
  port: 99999  # Port number too high
```

**Error message**:
```
Configuration validation failed for main.yaml:
  - api.port: Input should be less than or equal to 65535
```

### Validation Rules

- **Ports**: Must be between 1 and 65535
- **Percentages**: Risk percentages must be between 0 and 1
- **Required fields**: Cannot be empty
- **Type checking**: Values must match expected types
- **Constraints**: Custom validation rules (e.g., min/max values)

## Security Best Practices

### 1. Never Commit Secrets

**DO NOT** commit sensitive values to version control:

```yaml
# ❌ BAD - Hardcoded secret
database:
  password: "my_secret_password"

# ✅ GOOD - Use environment variable
database:
  password: "${DATABASE_PASSWORD}"
```

### 2. Use .gitignore

Ensure `.env` is in `.gitignore`:

```gitignore
# Environment variables
.env
.env.local
.env.*.local

# Sensitive configs (if any)
config/secrets.yaml
```

### 3. Use .env.example

Provide `.env.example` with placeholder values:

```bash
# .env.example
DATABASE_PASSWORD=your-password-here
MT5_PASSWORD=your-mt5-password-here
```

### 4. Rotate Credentials Regularly

- API keys should be rotated every 90 days
- Use strong, unique passwords
- Enable 2FA where possible

### 5. Environment-Specific Secrets

Use different credentials for each environment:

```bash
# Development
DATABASE_PASSWORD=dev_password

# Production
DATABASE_PASSWORD=prod_strong_password_xyz
```

## Examples

### Example 1: Load and Use Configuration

```python
from backend.config.loader import ConfigLoader

# Initialize
loader = ConfigLoader(config_dir="config")

# Load configurations
main_config = loader.load_main_config()
risk_config = loader.load_risk_config("default")

# Use configuration values
if main_config.features.paper_trading:
    print("Paper trading is enabled")

max_risk = risk_config.account.max_risk_per_trade
print(f"Maximum risk per trade: {max_risk * 100}%")
```

### Example 2: Environment Override

**Base config** (`main.yaml`):
```yaml
database:
  host: "localhost"
  pool_size: 10
```

**Production override** (`environments/production.yaml`):
```yaml
database:
  host: "prod-db.example.com"
  pool_size: 50
```

**Code**:
```python
# In production
loader = ConfigLoader(environment="production")
config = loader.load_main_config()

print(config.database.host)        # prod-db.example.com
print(config.database.pool_size)   # 50
```

### Example 3: Custom Strategy Configuration

```python
# Load multiple strategies
loader = ConfigLoader()

strategies = []
for strategy_name in loader.list_strategies():
    strategy_config = loader.load_strategy_config(strategy_name)
    strategies.append(strategy_config)
    print(f"Loaded: {strategy_config.name} ({strategy_config.type})")
```

### Example 4: Validation and Error Handling

```python
from backend.config.loader import ConfigLoader

try:
    loader = ConfigLoader(config_dir="config")
    config = loader.load_main_config()
    print("✓ Configuration is valid")
except FileNotFoundError as e:
    print(f"✗ Configuration file not found: {e}")
except ValueError as e:
    print(f"✗ Validation error: {e}")
except Exception as e:
    print(f"✗ Unexpected error: {e}")
```

## Troubleshooting

### Configuration Not Found

```
FileNotFoundError: Configuration file not found: config/main.yaml
```

**Solution**: Ensure you're running from the project root directory where `config/` exists.

### Validation Errors

```
ValidationError: api.port - Input should be less than or equal to 65535
```

**Solution**: Check the YAML file and fix invalid values according to the error message.

### Environment Variable Not Substituted

```yaml
database:
  password: "${DATABASE_PASSWORD}"  # Still showing variable syntax
```

**Solution**: Ensure the environment variable is set:
```bash
export DATABASE_PASSWORD=your_password
```

### Hot-Reload Not Working

**Solution**: 
1. Ensure `enable_hot_reload=True` when initializing loader
2. Check file system permissions
3. Verify watchdog is installed: `pip install watchdog`

## Additional Resources

- [Pydantic Documentation](https://docs.pydantic.dev/)
- [YAML Syntax Guide](https://yaml.org/spec/1.2/spec.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## Support

For issues or questions about configuration:
1. Check this documentation
2. Run `python -m backend.config.cli validate` to check for errors
3. Review logs for detailed error messages
4. Contact the development team
