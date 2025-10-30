"""Pydantic models for configuration validation"""

from typing import Dict, List, Optional, Any, Literal
from pydantic import BaseModel, Field, validator, field_validator
from enum import Enum


# Enums
class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class OrderType(str, Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"
    TRAILING_STOP = "trailing_stop"


# System Configuration
class SystemConfig(BaseModel):
    name: str = "SelamAI"
    version: str = "1.0.0"
    environment: Environment = Environment.DEVELOPMENT
    debug: bool = True
    log_level: LogLevel = LogLevel.INFO


class RateLimitConfig(BaseModel):
    enabled: bool = True
    requests_per_minute: int = 60
    requests_per_hour: int = 1000


class APIConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = Field(default=8000, ge=1, le=65535)
    cors_origins: List[str] = Field(default_factory=list)
    rate_limit: RateLimitConfig = Field(default_factory=RateLimitConfig)


class AIEndpoints(BaseModel):
    openai: str = "https://api.openai.com/v1"
    anthropic: str = "https://api.anthropic.com/v1"


class AIFeatures(BaseModel):
    sentiment_analysis: bool = True
    signal_generation: bool = True
    risk_assessment: bool = True
    market_commentary: bool = True


class AIConfig(BaseModel):
    provider: str = "openai"
    model: str = "gpt-4"
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=2000, ge=1)
    timeout: int = Field(default=30, ge=1)
    retry_attempts: int = Field(default=3, ge=0)
    endpoints: AIEndpoints = Field(default_factory=AIEndpoints)
    features: AIFeatures = Field(default_factory=AIFeatures)


class DatabaseConfig(BaseModel):
    type: str = "postgresql"
    host: str = "localhost"
    port: int = Field(default=5432, ge=1, le=65535)
    name: str = "selamai_db"
    pool_size: int = Field(default=10, ge=1)
    pool_timeout: int = Field(default=30, ge=1)
    echo: bool = False


class CacheConfig(BaseModel):
    enabled: bool = True
    type: str = "redis"
    host: str = "localhost"
    port: int = Field(default=6379, ge=1, le=65535)
    ttl: int = Field(default=3600, ge=0)
    max_size: int = Field(default=1000, ge=0)


class BrokerProviderConfig(BaseModel):
    enabled: bool = True
    timeout: int = Field(default=30, ge=1)


class MT5Config(BrokerProviderConfig):
    server: str = ""
    account: str = ""
    password: str = ""


class InteractiveBrokersConfig(BrokerProviderConfig):
    host: str = "127.0.0.1"
    port: int = Field(default=7497, ge=1, le=65535)
    client_id: int = 1


class AlpacaConfig(BrokerProviderConfig):
    base_url: str = "https://paper-api.alpaca.markets"
    api_version: str = "v2"


class BrokerConfig(BaseModel):
    default_provider: str = "mt5"
    mt5: MT5Config = Field(default_factory=MT5Config)
    interactive_brokers: InteractiveBrokersConfig = Field(default_factory=InteractiveBrokersConfig)
    alpaca: AlpacaConfig = Field(default_factory=AlpacaConfig)


class DataProviderConfig(BaseModel):
    enabled: bool = True
    websocket: bool = False
    rate_limit: Optional[int] = None
    fallback: bool = False


class DataFeedConfig(BaseModel):
    primary_provider: str = "polygon"
    update_interval: int = Field(default=60, ge=1)
    historical_data_days: int = Field(default=365, ge=1)
    providers: Dict[str, DataProviderConfig] = Field(default_factory=dict)


class MonitoringConfig(BaseModel):
    enabled: bool = True
    metrics_interval: int = Field(default=60, ge=1)
    alert_channels: List[str] = Field(default_factory=list)
    health_check_interval: int = Field(default=30, ge=1)
    performance_tracking: bool = True


class SecurityConfig(BaseModel):
    jwt_secret: str = ""
    jwt_expiry: int = Field(default=86400, ge=1)
    api_key_rotation_days: int = Field(default=90, ge=1)
    encryption_algorithm: str = "AES-256"
    require_https: bool = False


class FeaturesConfig(BaseModel):
    paper_trading: bool = True
    live_trading: bool = False
    backtesting: bool = True
    portfolio_optimization: bool = True
    social_trading: bool = False
    copy_trading: bool = False
    automated_rebalancing: bool = True
    tax_loss_harvesting: bool = False


# Main Configuration
class MainConfig(BaseModel):
    system: SystemConfig = Field(default_factory=SystemConfig)
    api: APIConfig = Field(default_factory=APIConfig)
    ai: AIConfig = Field(default_factory=AIConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    cache: CacheConfig = Field(default_factory=CacheConfig)
    broker: BrokerConfig = Field(default_factory=BrokerConfig)
    data_feed: DataFeedConfig = Field(default_factory=DataFeedConfig)
    monitoring: MonitoringConfig = Field(default_factory=MonitoringConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    features: FeaturesConfig = Field(default_factory=FeaturesConfig)
    imports: List[str] = Field(default_factory=list)


# Asset Configuration Models
class ForexPairConfig(BaseModel):
    name: str
    pip_value: float = Field(gt=0)
    min_lot_size: float = Field(gt=0)
    max_lot_size: float = Field(gt=0)
    margin_requirement: float = Field(ge=0, le=1)
    trading_hours: str
    spread_typical: float = Field(ge=0)
    commission: float = Field(ge=0)
    enabled: bool = True


class CommodityConfig(BaseModel):
    name: str
    symbol: str
    type: str
    min_lot_size: float = Field(gt=0)
    max_lot_size: float = Field(gt=0)
    margin_requirement: float = Field(ge=0, le=1)
    trading_hours: str
    spread_typical: float = Field(ge=0)
    tick_size: float = Field(gt=0)
    contract_size: float = Field(gt=0)
    enabled: bool = True


class CryptoPairConfig(BaseModel):
    name: str
    min_lot_size: float = Field(gt=0)
    max_lot_size: float = Field(gt=0)
    margin_requirement: float = Field(ge=0, le=1)
    trading_hours: str
    spread_typical: float = Field(ge=0)
    maker_fee: float = Field(ge=0)
    taker_fee: float = Field(ge=0)
    enabled: bool = True


class IndexConfig(BaseModel):
    name: str
    min_lot_size: float = Field(gt=0)
    max_lot_size: float = Field(gt=0)
    margin_requirement: float = Field(ge=0, le=1)
    trading_hours: str
    spread_typical: float = Field(ge=0)
    enabled: bool = True


class ForexAssets(BaseModel):
    enabled: bool = True
    pairs: Dict[str, ForexPairConfig] = Field(default_factory=dict)


class CommodityAssets(BaseModel):
    enabled: bool = True
    instruments: Dict[str, CommodityConfig] = Field(default_factory=dict)


class CryptoAssets(BaseModel):
    enabled: bool = True
    pairs: Dict[str, CryptoPairConfig] = Field(default_factory=dict)


class IndexAssets(BaseModel):
    enabled: bool = True
    instruments: Dict[str, IndexConfig] = Field(default_factory=dict)


class GlobalAssetSettings(BaseModel):
    default_slippage: float = Field(ge=0)
    max_slippage_percent: float = Field(ge=0)
    order_execution_timeout: int = Field(ge=1)
    price_update_frequency: int = Field(ge=1)
    historical_data_retention: int = Field(ge=1)


class AssetClasses(BaseModel):
    forex: ForexAssets = Field(default_factory=ForexAssets)
    commodities: CommodityAssets = Field(default_factory=CommodityAssets)
    crypto: CryptoAssets = Field(default_factory=CryptoAssets)
    indices: IndexAssets = Field(default_factory=IndexAssets)


class AssetsConfig(BaseModel):
    assets: AssetClasses = Field(default_factory=AssetClasses)
    global_settings: GlobalAssetSettings
    watchlists: Dict[str, List[str]] = Field(default_factory=dict)


# Risk Management Configuration Models
class AccountRiskConfig(BaseModel):
    max_risk_per_trade: float = Field(ge=0, le=1)
    max_daily_loss: float = Field(ge=0, le=1)
    max_weekly_loss: float = Field(ge=0, le=1)
    max_monthly_loss: float = Field(ge=0, le=1)
    max_total_exposure: float = Field(ge=0, le=1)


class PositionRiskConfig(BaseModel):
    max_position_size: float = Field(ge=0, le=1)
    max_positions_total: int = Field(ge=1)
    max_positions_per_asset: int = Field(ge=1)
    max_positions_per_asset_class: int = Field(ge=1)
    max_correlation_exposure: float = Field(ge=0, le=1)


class LeverageConfig(BaseModel):
    default: int = Field(ge=1)
    max: int = Field(ge=1)
    forex: int = Field(ge=1)
    commodities: int = Field(ge=1)
    crypto: int = Field(ge=1)
    indices: int = Field(ge=1)
    use_dynamic_leverage: bool = True


class StopLossConfig(BaseModel):
    required: bool = True
    default_percent: float = Field(ge=0, le=1)
    trailing_stop: bool = False
    trailing_step: float = Field(ge=0)
    max_stop_distance: float = Field(ge=0)
    use_atr_stops: bool = True
    atr_multiplier: float = Field(gt=0)


class PartialExitLevel(BaseModel):
    percent: float = Field(ge=0, le=1)
    ratio: float = Field(gt=0)


class TakeProfitConfig(BaseModel):
    required: bool = False
    default_reward_risk_ratio: float = Field(gt=0)
    use_partial_exits: bool = False
    partial_exit_levels: List[PartialExitLevel] = Field(default_factory=list)


class VolatilityConfig(BaseModel):
    measure: str = "atr"
    adjustment_enabled: bool = True
    high_volatility_threshold: float = Field(gt=0)
    low_volatility_threshold: float = Field(gt=0)
    position_size_multiplier_high: float = Field(gt=0)
    position_size_multiplier_low: float = Field(gt=0)


class DrawdownThreshold(BaseModel):
    level: float = Field(ge=0, le=1)
    action: str
    multiplier: Optional[float] = Field(default=None, gt=0)
    duration: Optional[int] = Field(default=None, ge=0)


class DrawdownConfig(BaseModel):
    protection_enabled: bool = True
    thresholds: List[DrawdownThreshold] = Field(default_factory=list)
    recovery_threshold: float = Field(ge=0, le=1)


class TimeControlsConfig(BaseModel):
    trading_hours: Dict[str, str] = Field(default_factory=dict)
    avoid_high_impact_news: bool = True
    news_blackout_minutes: int = Field(ge=0)
    avoid_market_open_minutes: int = Field(ge=0)
    avoid_market_close_minutes: int = Field(ge=0)
    max_trades_per_day: int = Field(ge=1)
    max_trades_per_hour: int = Field(ge=1)


class AssetClassLimit(BaseModel):
    max_exposure: float = Field(ge=0, le=1)
    max_positions: int = Field(ge=1)


class RiskManagementConfig(BaseModel):
    name: str
    description: str
    account: AccountRiskConfig
    position: PositionRiskConfig
    leverage: LeverageConfig
    stop_loss: StopLossConfig
    take_profit: TakeProfitConfig
    volatility: VolatilityConfig
    drawdown: DrawdownConfig
    time_controls: TimeControlsConfig
    asset_class_limits: Dict[str, AssetClassLimit] = Field(default_factory=dict)


# Strategy Configuration Models
class IndicatorConfig(BaseModel):
    period: int = Field(ge=1)
    type: Optional[str] = None
    apply_to: Optional[str] = None
    std_dev: Optional[float] = None
    fast_period: Optional[int] = None
    slow_period: Optional[int] = None
    signal_period: Optional[int] = None
    multiplier: Optional[float] = None
    overbought: Optional[float] = None
    oversold: Optional[float] = None
    extreme_overbought: Optional[float] = None
    extreme_oversold: Optional[float] = None
    k_period: Optional[int] = None
    d_period: Optional[int] = None
    slowing: Optional[int] = None


class EntryConditions(BaseModel):
    conditions: List[str] = Field(default_factory=list)
    confirmation_required: int = Field(ge=1)


class EntryConfig(BaseModel):
    long: EntryConditions
    short: EntryConditions


class ExitTPConfig(BaseModel):
    enabled: bool = True
    method: str = "fixed"
    atr_multiple: Optional[float] = None
    target: Optional[str] = None


class ExitSLConfig(BaseModel):
    enabled: bool = True
    method: str = "fixed"
    atr_multiple: Optional[float] = None


class ExitTrailingConfig(BaseModel):
    enabled: bool = False
    activation_profit: Optional[float] = None
    trail_distance: Optional[float] = None


class ExitConfig(BaseModel):
    take_profit: ExitTPConfig
    stop_loss: ExitSLConfig
    trailing_stop: Optional[ExitTrailingConfig] = None
    exit_signals: List[str] = Field(default_factory=list)


class PositionSizingConfig(BaseModel):
    method: str = "risk_based"
    risk_per_trade: float = Field(ge=0, le=1)
    min_position_size: float = Field(gt=0)
    max_position_size: float = Field(gt=0)
    scale_in_enabled: bool = False
    scale_in_levels: Optional[int] = None
    scale_out_enabled: bool = False
    scale_out_levels: Optional[int] = None


class FilterConfig(BaseModel):
    enabled: bool = True


class TrendFilterConfig(FilterConfig):
    only_trade_with_trend: bool = True
    trend_strength_min: Optional[float] = None


class VolatilityFilterConfig(FilterConfig):
    min_atr: Optional[float] = None
    max_atr: Optional[float] = None


class TradingSession(BaseModel):
    name: str
    start: str
    end: str
    weight: float = Field(ge=0)


class TimeFilterConfig(FilterConfig):
    trading_sessions: List[TradingSession] = Field(default_factory=list)
    avoid_weekends: bool = True
    avoid_holidays: bool = True


class SpreadFilterConfig(FilterConfig):
    max_spread: float = Field(ge=0)


class NewsFilterConfig(FilterConfig):
    avoid_high_impact: bool = True
    blackout_minutes: int = Field(ge=0)


class RangeFilterConfig(FilterConfig):
    only_trade_ranging_markets: bool = False
    range_threshold: Optional[float] = None


class FiltersConfig(BaseModel):
    trend_filter: Optional[TrendFilterConfig] = None
    volatility_filter: Optional[VolatilityFilterConfig] = None
    time_filter: Optional[TimeFilterConfig] = None
    spread_filter: Optional[SpreadFilterConfig] = None
    news_filter: Optional[NewsFilterConfig] = None
    range_filter: Optional[RangeFilterConfig] = None


class AssetSpecificConfig(BaseModel):
    enabled: bool = True
    pairs: Optional[List[str]] = None
    instruments: Optional[List[str]] = None
    min_pip_move: Optional[int] = None


class StrategyAssetSettings(BaseModel):
    forex: Optional[AssetSpecificConfig] = None
    commodities: Optional[AssetSpecificConfig] = None
    crypto: Optional[AssetSpecificConfig] = None
    indices: Optional[AssetSpecificConfig] = None


class StrategyParameters(BaseModel):
    primary_timeframe: str
    confirmation_timeframes: List[str] = Field(default_factory=list)
    indicators: Dict[str, IndicatorConfig] = Field(default_factory=dict)
    entry: EntryConfig
    exit: ExitConfig
    position_sizing: PositionSizingConfig
    filters: Optional[FiltersConfig] = None


class StrategyConfig(BaseModel):
    name: str
    type: str
    description: str
    version: str = "1.0.0"
    parameters: StrategyParameters
    asset_settings: Optional[StrategyAssetSettings] = None


# Agent Configuration Models
class AgentCoreConfig(BaseModel):
    model: str = "gpt-4"
    temperature: float = Field(ge=0, le=2)
    max_tokens: int = Field(ge=1)
    context_window: int = Field(ge=1)
    reasoning_mode: str = "chain_of_thought"


class AgentCapabilities(BaseModel):
    market_analysis: bool = True
    signal_generation: bool = True
    risk_assessment: bool = True
    portfolio_management: bool = False
    trade_execution: bool = False
    learning: bool = False
    backtesting: bool = False
    research: bool = False
    reporting: bool = False


class DecisionFactor(BaseModel):
    technical_analysis: float = Field(ge=0, le=1)
    fundamental_analysis: float = Field(ge=0, le=1)
    sentiment_analysis: float = Field(ge=0, le=1)
    risk_metrics: float = Field(ge=0, le=1)


class VotingSystem(BaseModel):
    enabled: bool = True
    min_votes: int = Field(ge=1)
    strategies: List[str] = Field(default_factory=list)


class DecisionMakingConfig(BaseModel):
    mode: str = "hybrid"
    confidence_threshold: float = Field(ge=0, le=1)
    multi_factor_analysis: bool = True
    factors: Optional[DecisionFactor] = None
    voting_system: Optional[VotingSystem] = None


class ExecutionStrategyConfig(BaseModel):
    slippage_tolerance: float = Field(ge=0)
    partial_fills_allowed: bool = True
    timeout: int = Field(ge=1)
    retry_attempts: int = Field(ge=0)
    smart_routing: bool = True


class ExecutionConfig(BaseModel):
    mode: str = "automated"
    order_types: List[OrderType] = Field(default_factory=list)
    execution_strategy: ExecutionStrategyConfig
    pre_trade_checks: List[str] = Field(default_factory=list)


class PortfolioAllocation(BaseModel):
    forex: float = Field(ge=0, le=1)
    commodities: float = Field(ge=0, le=1)
    crypto: float = Field(ge=0, le=1)
    indices: float = Field(ge=0, le=1)


class RebalancingConfig(BaseModel):
    enabled: bool = True
    frequency: str = "daily"
    threshold: float = Field(ge=0)
    method: str = "threshold"


class PortfolioConfig(BaseModel):
    strategy: str = "diversified"
    allocation: PortfolioAllocation
    rebalancing: RebalancingConfig


class OutputConfig(BaseModel):
    format: str = "structured"
    include_charts: bool = False
    include_reasoning: bool = True
    confidence_scores: bool = True


class ReportingConfig(BaseModel):
    frequency: str = "hourly"
    distribution: List[str] = Field(default_factory=list)


class AgentConfig(BaseModel):
    name: str
    type: str
    version: str = "1.0.0"
    description: str
    core: AgentCoreConfig
    capabilities: AgentCapabilities
    decision_making: Optional[DecisionMakingConfig] = None
    execution: Optional[ExecutionConfig] = None
    portfolio: Optional[PortfolioConfig] = None
    output: Optional[OutputConfig] = None
    reporting: Optional[ReportingConfig] = None
    analysis_focus: Optional[List[str]] = None
    integration: Optional[Dict[str, Any]] = None
