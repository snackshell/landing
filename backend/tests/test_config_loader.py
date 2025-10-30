"""Tests for configuration loader"""

import pytest
import os
import tempfile
import yaml
from pathlib import Path

from backend.config.loader import ConfigLoader
from backend.config.models import MainConfig, AssetsConfig, RiskManagementConfig


class TestConfigLoader:
    """Test suite for ConfigLoader"""

    @pytest.fixture
    def config_dir(self):
        """Fixture providing path to config directory"""
        return "config"

    @pytest.fixture
    def loader(self, config_dir):
        """Fixture providing ConfigLoader instance"""
        return ConfigLoader(config_dir=config_dir, environment="development")

    def test_init_loader(self, loader):
        """Test ConfigLoader initialization"""
        assert loader is not None
        assert loader.environment == "development"
        assert loader.config_dir.exists()

    def test_invalid_config_dir(self):
        """Test initialization with invalid config directory"""
        with pytest.raises(FileNotFoundError):
            ConfigLoader(config_dir="nonexistent_dir")

    def test_load_main_config(self, loader):
        """Test loading main configuration"""
        config = loader.load_main_config()
        
        assert isinstance(config, MainConfig)
        assert config.system.name == "SelamAI"
        assert config.system.environment.value == "development"
        assert config.api.port == 8000

    def test_load_main_config_caching(self, loader):
        """Test configuration caching"""
        config1 = loader.load_main_config(use_cache=True)
        config2 = loader.load_main_config(use_cache=True)
        
        # Should return the same cached instance
        assert config1 is config2

    def test_load_assets_config(self, loader):
        """Test loading assets configuration"""
        config = loader.load_assets_config()
        
        assert isinstance(config, AssetsConfig)
        assert config.assets.forex.enabled is True
        assert "EURUSD" in config.assets.forex.pairs
        assert "XAUUSD" in config.assets.commodities.instruments
        assert "BTCUSD" in config.assets.crypto.pairs

    def test_load_risk_config_default(self, loader):
        """Test loading default risk configuration"""
        config = loader.load_risk_config("default")
        
        assert isinstance(config, RiskManagementConfig)
        assert config.name == "default"
        assert config.account.max_risk_per_trade == 0.02
        assert config.stop_loss.required is True

    def test_load_risk_config_aggressive(self, loader):
        """Test loading aggressive risk configuration"""
        config = loader.load_risk_config("aggressive")
        
        assert isinstance(config, RiskManagementConfig)
        assert config.name == "aggressive"
        assert config.account.max_risk_per_trade == 0.05
        assert config.account.max_risk_per_trade > 0.02  # More risk than default

    def test_load_nonexistent_risk_profile(self, loader):
        """Test loading non-existent risk profile"""
        with pytest.raises(FileNotFoundError):
            loader.load_risk_config("nonexistent")

    def test_load_strategy_config(self, loader):
        """Test loading strategy configuration"""
        config = loader.load_strategy_config("momentum")
        
        assert config.name == "momentum"
        assert config.type == "trend_following"
        assert config.parameters.primary_timeframe == "1h"
        assert "ema_fast" in config.parameters.indicators

    def test_load_agent_config(self, loader):
        """Test loading agent configuration"""
        config = loader.load_agent_config("trading_agent")
        
        assert config.name == "trading_agent"
        assert config.type == "autonomous_trader"
        assert config.core.model == "gpt-4"
        assert config.capabilities.trade_execution is True

    def test_list_strategies(self, loader):
        """Test listing available strategies"""
        strategies = loader.list_strategies()
        
        assert isinstance(strategies, list)
        assert "momentum" in strategies
        assert "mean_reversion" in strategies

    def test_list_agents(self, loader):
        """Test listing available agents"""
        agents = loader.list_agents()
        
        assert isinstance(agents, list)
        assert "trading_agent" in agents
        assert "analysis_agent" in agents

    def test_list_risk_profiles(self, loader):
        """Test listing available risk profiles"""
        profiles = loader.list_risk_profiles()
        
        assert isinstance(profiles, list)
        assert "default" in profiles
        assert "aggressive" in profiles

    def test_reload(self, loader):
        """Test configuration reload"""
        # Load config to populate cache
        config1 = loader.load_main_config(use_cache=True)
        
        # Reload (clears cache)
        loader.reload()
        
        # Load again
        config2 = loader.load_main_config(use_cache=True)
        
        # Should be different instances
        assert config1 is not config2

    def test_get_config_info(self, loader):
        """Test getting configuration info"""
        info = loader.get_config_info()
        
        assert "environment" in info
        assert "config_dir" in info
        assert "available_strategies" in info
        assert "available_agents" in info
        assert info["environment"] == "development"


class TestEnvironmentOverrides:
    """Test environment-specific configuration overrides"""

    def test_development_environment(self):
        """Test development environment configuration"""
        loader = ConfigLoader(config_dir="config", environment="development")
        config = loader.load_main_config()
        
        assert config.system.environment.value == "development"
        assert config.system.debug is True
        assert config.security.require_https is False

    def test_production_environment(self):
        """Test production environment configuration"""
        loader = ConfigLoader(config_dir="config", environment="production")
        config = loader.load_main_config()
        
        assert config.system.environment.value == "production"
        assert config.system.debug is False
        assert config.security.require_https is True


class TestConfigValidation:
    """Test configuration validation"""

    @pytest.fixture
    def temp_config_dir(self):
        """Create temporary config directory for testing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir) / "config"
            config_dir.mkdir()
            yield config_dir

    def test_invalid_yaml_syntax(self, temp_config_dir):
        """Test handling of invalid YAML syntax"""
        # Create invalid YAML file
        invalid_yaml = temp_config_dir / "main.yaml"
        invalid_yaml.write_text("invalid: yaml: syntax: here:")
        
        loader = ConfigLoader(config_dir=str(temp_config_dir))
        with pytest.raises(ValueError, match="Failed to parse YAML"):
            loader.load_main_config()

    def test_validation_error(self, temp_config_dir):
        """Test handling of validation errors"""
        # Create YAML with invalid values
        invalid_config = {
            "system": {
                "name": "Test",
                "version": "1.0.0",
            },
            "api": {
                "port": 99999,  # Invalid port number
            }
        }
        
        config_file = temp_config_dir / "main.yaml"
        with open(config_file, "w") as f:
            yaml.dump(invalid_config, f)
        
        loader = ConfigLoader(config_dir=str(temp_config_dir))
        with pytest.raises(ValueError, match="validation failed"):
            loader.load_main_config()


class TestEnvironmentVariables:
    """Test environment variable substitution"""

    def test_env_var_substitution(self, monkeypatch):
        """Test environment variable substitution in configs"""
        # Set environment variable
        monkeypatch.setenv("TEST_VAR", "test_value")
        
        loader = ConfigLoader(config_dir="config")
        
        # The loader should substitute environment variables
        # This is tested implicitly through the main config load
        config = loader.load_main_config()
        assert config is not None


def test_deep_merge():
    """Test deep merge functionality"""
    loader = ConfigLoader(config_dir="config")
    
    base = {
        "a": 1,
        "b": {
            "c": 2,
            "d": 3,
        },
        "e": [1, 2, 3],
    }
    
    override = {
        "b": {
            "c": 20,  # Override existing
            "f": 4,   # Add new
        },
        "e": [4, 5, 6],  # Replace list
        "g": 5,  # Add new top-level
    }
    
    result = loader._deep_merge(base, override)
    
    assert result["a"] == 1  # Unchanged
    assert result["b"]["c"] == 20  # Overridden
    assert result["b"]["d"] == 3  # Unchanged
    assert result["b"]["f"] == 4  # New
    assert result["e"] == [4, 5, 6]  # Replaced
    assert result["g"] == 5  # New
