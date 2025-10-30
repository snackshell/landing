"""FastAPI endpoints for configuration management"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Optional, List
import os

from backend.config.loader import get_config_loader

app = FastAPI(
    title="SelamAI Configuration API",
    description="API for inspecting and managing configurations",
    version="1.0.0",
)

# Initialize configuration loader
config_loader = get_config_loader(
    config_dir=os.getenv("CONFIG_DIR", "config"),
    environment=os.getenv("ENVIRONMENT", "development"),
    enable_hot_reload=os.getenv("ENABLE_HOT_RELOAD", "false").lower() == "true",
)


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "SelamAI Configuration API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/api/config/info")
async def get_config_info():
    """Get configuration loader information"""
    return config_loader.get_config_info()


@app.get("/api/config/main")
async def get_main_config(reload: bool = Query(False, description="Force reload from disk")):
    """Get main configuration"""
    try:
        config = config_loader.load_main_config(use_cache=not reload)
        return config.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/config/assets")
async def get_assets_config(reload: bool = Query(False, description="Force reload from disk")):
    """Get assets configuration"""
    try:
        config = config_loader.load_assets_config(use_cache=not reload)
        return config.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/config/strategies")
async def list_strategies():
    """List available strategy configurations"""
    return {"strategies": config_loader.list_strategies()}


@app.get("/api/config/strategies/{strategy_name}")
async def get_strategy_config(
    strategy_name: str,
    reload: bool = Query(False, description="Force reload from disk"),
):
    """Get specific strategy configuration"""
    try:
        config = config_loader.load_strategy_config(strategy_name, use_cache=not reload)
        return config.model_dump()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Strategy '{strategy_name}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/config/agents")
async def list_agents():
    """List available agent configurations"""
    return {"agents": config_loader.list_agents()}


@app.get("/api/config/agents/{agent_name}")
async def get_agent_config(
    agent_name: str,
    reload: bool = Query(False, description="Force reload from disk"),
):
    """Get specific agent configuration"""
    try:
        config = config_loader.load_agent_config(agent_name, use_cache=not reload)
        return config.model_dump()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/config/risk")
async def list_risk_profiles():
    """List available risk profiles"""
    return {"risk_profiles": config_loader.list_risk_profiles()}


@app.get("/api/config/risk/{profile_name}")
async def get_risk_config(
    profile_name: str,
    reload: bool = Query(False, description="Force reload from disk"),
):
    """Get specific risk profile configuration"""
    try:
        config = config_loader.load_risk_config(profile_name, use_cache=not reload)
        return config.model_dump()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Risk profile '{profile_name}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/config/reload")
async def reload_configs():
    """Reload all configurations (clear cache)"""
    try:
        config_loader.reload()
        return {"message": "Configurations reloaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/config/validate")
async def validate_configs():
    """Validate all configurations"""
    errors = []
    results = {
        "valid": [],
        "invalid": [],
    }
    
    # Validate main
    try:
        config_loader.load_main_config(use_cache=False)
        results["valid"].append("main.yaml")
    except Exception as e:
        results["invalid"].append({"file": "main.yaml", "error": str(e)})
    
    # Validate assets
    try:
        config_loader.load_assets_config(use_cache=False)
        results["valid"].append("assets.yaml")
    except Exception as e:
        results["invalid"].append({"file": "assets.yaml", "error": str(e)})
    
    # Validate strategies
    for strategy in config_loader.list_strategies():
        try:
            config_loader.load_strategy_config(strategy, use_cache=False)
            results["valid"].append(f"strategies/{strategy}.yaml")
        except Exception as e:
            results["invalid"].append({"file": f"strategies/{strategy}.yaml", "error": str(e)})
    
    # Validate agents
    for agent in config_loader.list_agents():
        try:
            config_loader.load_agent_config(agent, use_cache=False)
            results["valid"].append(f"agents/{agent}.yaml")
        except Exception as e:
            results["invalid"].append({"file": f"agents/{agent}.yaml", "error": str(e)})
    
    # Validate risk profiles
    for profile in config_loader.list_risk_profiles():
        try:
            config_loader.load_risk_config(profile, use_cache=False)
            results["valid"].append(f"risk/{profile}.yaml")
        except Exception as e:
            results["invalid"].append({"file": f"risk/{profile}.yaml", "error": str(e)})
    
    return {
        "total": len(results["valid"]) + len(results["invalid"]),
        "valid_count": len(results["valid"]),
        "invalid_count": len(results["invalid"]),
        "results": results,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=os.getenv("ENVIRONMENT", "development") == "development",
    )
