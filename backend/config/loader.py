"""Configuration loader with YAML parsing, validation, and hot-reloading"""

import os
import yaml
import glob
from pathlib import Path
from typing import Dict, Any, Optional, Type, TypeVar, List
from pydantic import ValidationError
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv

from .models import (
    MainConfig,
    AssetsConfig,
    RiskManagementConfig,
    StrategyConfig,
    AgentConfig,
)

logger = logging.getLogger(__name__)

T = TypeVar("T")


class ConfigFileHandler(FileSystemEventHandler):
    """File system event handler for configuration hot-reloading"""

    def __init__(self, loader: "ConfigLoader"):
        self.loader = loader

    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".yaml"):
            logger.info(f"Configuration file changed: {event.src_path}")
            try:
                self.loader.reload()
                logger.info("Configuration reloaded successfully")
            except Exception as e:
                logger.error(f"Failed to reload configuration: {e}")


class ConfigLoader:
    """
    Configuration loader with YAML parsing, Pydantic validation, and hot-reloading.
    
    Features:
    - Load and validate YAML configurations
    - Environment-specific overrides (dev/staging/prod)
    - Environment variable substitution
    - Configuration merging with precedence rules
    - Hot-reloading support
    - Helpful error messages for validation failures
    """

    def __init__(
        self,
        config_dir: str = "config",
        environment: Optional[str] = None,
        enable_hot_reload: bool = False,
    ):
        """
        Initialize the configuration loader.
        
        Args:
            config_dir: Path to configuration directory
            environment: Environment name (development/staging/production)
            enable_hot_reload: Enable automatic reloading on config changes
        """
        self.config_dir = Path(config_dir)
        self.environment = environment or os.getenv("ENVIRONMENT", "development")
        self.enable_hot_reload = enable_hot_reload
        
        # Load environment variables from .env file
        load_dotenv()
        
        # Configuration cache
        self._cache: Dict[str, Any] = {}
        
        # File watcher for hot reload
        self._observer: Optional[Observer] = None
        
        if not self.config_dir.exists():
            raise FileNotFoundError(f"Configuration directory not found: {self.config_dir}")
        
        logger.info(f"ConfigLoader initialized for environment: {self.environment}")
        
        if enable_hot_reload:
            self._setup_hot_reload()

    def _setup_hot_reload(self):
        """Setup file system watcher for hot-reloading"""
        self._observer = Observer()
        event_handler = ConfigFileHandler(self)
        self._observer.schedule(event_handler, str(self.config_dir), recursive=True)
        self._observer.start()
        logger.info("Hot-reload enabled for configuration files")

    def _substitute_env_vars(self, data: Any) -> Any:
        """
        Recursively substitute environment variables in configuration data.
        Supports ${VAR_NAME} and ${VAR_NAME:-default_value} syntax.
        """
        if isinstance(data, dict):
            return {key: self._substitute_env_vars(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self._substitute_env_vars(item) for item in data]
        elif isinstance(data, str):
            # Handle ${VAR_NAME:-default} syntax
            if data.startswith("${") and data.endswith("}"):
                var_expr = data[2:-1]
                if ":-" in var_expr:
                    var_name, default = var_expr.split(":-", 1)
                    return os.getenv(var_name, default)
                else:
                    return os.getenv(var_expr, data)
        return data

    def _load_yaml_file(self, file_path: Path) -> Dict[str, Any]:
        """Load and parse a YAML file with error handling"""
        try:
            with open(file_path, "r") as f:
                data = yaml.safe_load(f)
                if data is None:
                    return {}
                return self._substitute_env_vars(data)
        except yaml.YAMLError as e:
            raise ValueError(f"Failed to parse YAML file {file_path}: {e}")
        except Exception as e:
            raise IOError(f"Failed to read file {file_path}: {e}")

    def _deep_merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deep merge two dictionaries with override taking precedence.
        
        Precedence rules:
        1. Environment-specific config overrides base config
        2. Nested dictionaries are merged recursively
        3. Lists and primitive values are replaced, not merged
        """
        result = base.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result

    def _load_with_overrides(self, base_file: str) -> Dict[str, Any]:
        """
        Load configuration file with environment-specific overrides.
        
        Loading order (later files override earlier):
        1. Base configuration file
        2. Environment-specific override file
        """
        base_path = self.config_dir / base_file
        
        if not base_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {base_path}")
        
        # Load base configuration
        config = self._load_yaml_file(base_path)
        
        # Load environment-specific overrides
        env_file = self.config_dir / "environments" / f"{self.environment}.yaml"
        if env_file.exists():
            env_config = self._load_yaml_file(env_file)
            config = self._deep_merge(config, env_config)
            logger.debug(f"Applied environment overrides from {env_file}")
        
        return config

    def _validate_config(
        self,
        data: Dict[str, Any],
        model: Type[T],
        config_name: str,
    ) -> T:
        """
        Validate configuration data against Pydantic model.
        Provides helpful error messages on validation failure.
        """
        try:
            return model(**data)
        except ValidationError as e:
            error_msg = f"Configuration validation failed for {config_name}:\n"
            for error in e.errors():
                field = ".".join(str(loc) for loc in error["loc"])
                error_msg += f"  - {field}: {error['msg']}\n"
            logger.error(error_msg)
            raise ValueError(error_msg)

    def load_main_config(self, use_cache: bool = True) -> MainConfig:
        """
        Load and validate main configuration.
        
        Args:
            use_cache: Use cached config if available
            
        Returns:
            Validated MainConfig instance
        """
        cache_key = "main"
        
        if use_cache and cache_key in self._cache:
            return self._cache[cache_key]
        
        logger.info("Loading main configuration...")
        data = self._load_with_overrides("main.yaml")
        
        config = self._validate_config(data, MainConfig, "main.yaml")
        self._cache[cache_key] = config
        
        logger.info("Main configuration loaded successfully")
        return config

    def load_assets_config(self, use_cache: bool = True) -> AssetsConfig:
        """Load and validate assets configuration"""
        cache_key = "assets"
        
        if use_cache and cache_key in self._cache:
            return self._cache[cache_key]
        
        logger.info("Loading assets configuration...")
        data = self._load_yaml_file(self.config_dir / "assets.yaml")
        
        config = self._validate_config(data, AssetsConfig, "assets.yaml")
        self._cache[cache_key] = config
        
        logger.info("Assets configuration loaded successfully")
        return config

    def load_risk_config(
        self,
        profile: str = "default",
        use_cache: bool = True,
    ) -> RiskManagementConfig:
        """
        Load and validate risk management configuration.
        
        Args:
            profile: Risk profile name (default, aggressive, etc.)
            use_cache: Use cached config if available
            
        Returns:
            Validated RiskManagementConfig instance
        """
        cache_key = f"risk_{profile}"
        
        if use_cache and cache_key in self._cache:
            return self._cache[cache_key]
        
        logger.info(f"Loading risk configuration: {profile}...")
        file_path = self.config_dir / "risk" / f"{profile}.yaml"
        
        if not file_path.exists():
            raise FileNotFoundError(f"Risk profile not found: {file_path}")
        
        data = self._load_yaml_file(file_path)
        
        # Extract risk_management section
        if "risk_management" in data:
            data = data["risk_management"]
        
        config = self._validate_config(data, RiskManagementConfig, f"risk/{profile}.yaml")
        self._cache[cache_key] = config
        
        logger.info(f"Risk configuration '{profile}' loaded successfully")
        return config

    def load_strategy_config(
        self,
        strategy_name: str,
        use_cache: bool = True,
    ) -> StrategyConfig:
        """
        Load and validate strategy configuration.
        
        Args:
            strategy_name: Strategy name (momentum, mean_reversion, etc.)
            use_cache: Use cached config if available
            
        Returns:
            Validated StrategyConfig instance
        """
        cache_key = f"strategy_{strategy_name}"
        
        if use_cache and cache_key in self._cache:
            return self._cache[cache_key]
        
        logger.info(f"Loading strategy configuration: {strategy_name}...")
        file_path = self.config_dir / "strategies" / f"{strategy_name}.yaml"
        
        if not file_path.exists():
            raise FileNotFoundError(f"Strategy not found: {file_path}")
        
        data = self._load_yaml_file(file_path)
        
        # Extract strategy section
        if "strategy" in data:
            data = data["strategy"]
        
        config = self._validate_config(data, StrategyConfig, f"strategies/{strategy_name}.yaml")
        self._cache[cache_key] = config
        
        logger.info(f"Strategy configuration '{strategy_name}' loaded successfully")
        return config

    def load_agent_config(
        self,
        agent_name: str,
        use_cache: bool = True,
    ) -> AgentConfig:
        """
        Load and validate agent configuration.
        
        Args:
            agent_name: Agent name (trading_agent, analysis_agent, etc.)
            use_cache: Use cached config if available
            
        Returns:
            Validated AgentConfig instance
        """
        cache_key = f"agent_{agent_name}"
        
        if use_cache and cache_key in self._cache:
            return self._cache[cache_key]
        
        logger.info(f"Loading agent configuration: {agent_name}...")
        file_path = self.config_dir / "agents" / f"{agent_name}.yaml"
        
        if not file_path.exists():
            raise FileNotFoundError(f"Agent not found: {file_path}")
        
        data = self._load_yaml_file(file_path)
        
        # Extract agent section
        if "agent" in data:
            data = data["agent"]
        
        config = self._validate_config(data, AgentConfig, f"agents/{agent_name}.yaml")
        self._cache[cache_key] = config
        
        logger.info(f"Agent configuration '{agent_name}' loaded successfully")
        return config

    def list_strategies(self) -> List[str]:
        """List all available strategy configurations"""
        strategies_dir = self.config_dir / "strategies"
        if not strategies_dir.exists():
            return []
        
        strategies = []
        for file_path in strategies_dir.glob("*.yaml"):
            strategies.append(file_path.stem)
        
        return sorted(strategies)

    def list_agents(self) -> List[str]:
        """List all available agent configurations"""
        agents_dir = self.config_dir / "agents"
        if not agents_dir.exists():
            return []
        
        agents = []
        for file_path in agents_dir.glob("*.yaml"):
            agents.append(file_path.stem)
        
        return sorted(agents)

    def list_risk_profiles(self) -> List[str]:
        """List all available risk profiles"""
        risk_dir = self.config_dir / "risk"
        if not risk_dir.exists():
            return []
        
        profiles = []
        for file_path in risk_dir.glob("*.yaml"):
            profiles.append(file_path.stem)
        
        return sorted(profiles)

    def reload(self):
        """Reload all configurations (clears cache)"""
        logger.info("Reloading configurations...")
        self._cache.clear()
        logger.info("Configuration cache cleared")

    def get_config_info(self) -> Dict[str, Any]:
        """Get information about loaded configurations"""
        return {
            "environment": self.environment,
            "config_dir": str(self.config_dir),
            "hot_reload_enabled": self.enable_hot_reload,
            "cached_configs": list(self._cache.keys()),
            "available_strategies": self.list_strategies(),
            "available_agents": self.list_agents(),
            "available_risk_profiles": self.list_risk_profiles(),
        }

    def stop(self):
        """Stop the configuration loader and cleanup resources"""
        if self._observer:
            self._observer.stop()
            self._observer.join()
            logger.info("Configuration hot-reload stopped")


# Global configuration loader instance
_global_loader: Optional[ConfigLoader] = None


def get_config_loader(
    config_dir: str = "config",
    environment: Optional[str] = None,
    enable_hot_reload: bool = False,
) -> ConfigLoader:
    """
    Get or create the global configuration loader instance.
    
    Args:
        config_dir: Path to configuration directory
        environment: Environment name (development/staging/production)
        enable_hot_reload: Enable automatic reloading on config changes
        
    Returns:
        ConfigLoader instance
    """
    global _global_loader
    
    if _global_loader is None:
        _global_loader = ConfigLoader(
            config_dir=config_dir,
            environment=environment,
            enable_hot_reload=enable_hot_reload,
        )
    
    return _global_loader
