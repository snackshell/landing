"""FastAPI endpoints for configuration management"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse, PlainTextResponse
from typing import Optional, List
import os

from backend.config.loader import get_config_loader
from backend.logging_monitoring import (
    get_logger,
    get_metrics_tracker,
    get_alert_manager,
)
from backend.logging_monitoring.middleware import LoggingMiddleware, MetricsMiddleware
from backend.logging_monitoring.setup import initialize_monitoring

# Initialize the complete monitoring system
initialize_monitoring()

logger = get_logger(__name__)

app = FastAPI(
    title="SelamAI Configuration API",
    description="API for inspecting and managing configurations",
    version="1.0.0",
)

# Add logging and metrics middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(MetricsMiddleware)

# Initialize configuration loader
config_loader = get_config_loader(
    config_dir=os.getenv("CONFIG_DIR", "config"),
    environment=os.getenv("ENVIRONMENT", "development"),
    enable_hot_reload=os.getenv("ENABLE_HOT_RELOAD", "false").lower() == "true",
)

logger.info("SelamAI API initialized", extra_fields={
    "environment": os.getenv("ENVIRONMENT", "development"),
    "config_dir": os.getenv("CONFIG_DIR", "config"),
})


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


@app.get("/api/monitoring/status")
async def get_monitoring_status():
    """Get monitoring system status"""
    try:
        from backend.logging_monitoring.setup import get_monitoring_status
        return get_monitoring_status()
    except Exception as e:
        logger.error("Failed to get monitoring status", extra_fields={"error": str(e)})
        raise HTTPException(status_code=500, detail=str(e))


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


# Monitoring and Metrics Endpoints

@app.get("/api/metrics")
async def get_metrics(minutes: Optional[int] = Query(None, description="Filter last N minutes")):
    """Get all metrics"""
    try:
        metrics = get_metrics_tracker()
        return metrics.get_all_metrics(minutes=minutes)
    except Exception as e:
        logger.error("Failed to get metrics", extra_fields={"error": str(e)})
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/metrics/dashboard")
async def get_dashboard_metrics():
    """Get formatted metrics for dashboard visualization"""
    try:
        metrics = get_metrics_tracker()
        return metrics.get_dashboard_data()
    except Exception as e:
        logger.error("Failed to get dashboard metrics", extra_fields={"error": str(e)})
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/metrics/{metric_name}")
async def get_metric_summary(
    metric_name: str,
    minutes: Optional[int] = Query(None, description="Filter last N minutes")
):
    """Get summary statistics for a specific metric"""
    try:
        metrics = get_metrics_tracker()
        summary = metrics.get_metric_summary(metric_name, minutes=minutes)
        
        if summary is None:
            raise HTTPException(status_code=404, detail=f"Metric '{metric_name}' not found or has no data")
        
        return {
            "name": summary.name,
            "count": summary.count,
            "sum": summary.sum,
            "min": summary.min,
            "max": summary.max,
            "mean": summary.mean,
            "median": summary.median,
            "p95": summary.p95,
            "p99": summary.p99,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get metric summary", extra_fields={
            "metric": metric_name,
            "error": str(e),
        })
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/metrics/prometheus", response_class=PlainTextResponse)
async def get_prometheus_metrics():
    """Get metrics in Prometheus format (mock)"""
    try:
        from backend.logging_monitoring.exporters.prometheus import PrometheusExporter
        
        exporter = PrometheusExporter()
        
        # Register some basic metrics (in production, these would be auto-populated)
        metrics = get_metrics_tracker()
        
        exporter.register_counter("api_requests_total", "Total API requests")
        exporter.register_counter("api_errors_total", "Total API errors")
        exporter.register_counter("trades_total", "Total trades")
        exporter.register_gauge("memory_usage_percent", "Memory usage percentage")
        
        # Set values from metrics tracker
        exporter.increment("api_requests_total", metrics.get_counter("api_requests_total"))
        exporter.increment("api_errors_total", metrics.get_counter("api_errors_total"))
        exporter.increment("trades_total", metrics.get_counter("trades_total"))
        
        memory = metrics.get_gauge("memory_usage_percent")
        if memory:
            exporter.set_gauge("memory_usage_percent", memory)
        
        return exporter.generate_metrics()
    except Exception as e:
        logger.error("Failed to generate Prometheus metrics", extra_fields={"error": str(e)})
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/alerts/stats")
async def get_alert_stats():
    """Get alert statistics"""
    try:
        alert_manager = get_alert_manager()
        return alert_manager.get_alert_stats()
    except Exception as e:
        logger.error("Failed to get alert stats", extra_fields={"error": str(e)})
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/alerts/test/{rule_name}")
async def test_alert(rule_name: str):
    """Test an alert rule (development only)"""
    try:
        alert_manager = get_alert_manager()
        success = await alert_manager.trigger(rule_name, {"test": True})
        
        return {
            "rule": rule_name,
            "triggered": success,
            "message": "Alert triggered successfully" if success else "Alert not triggered (check cooldown or configuration)",
        }
    except Exception as e:
        logger.error("Failed to test alert", extra_fields={
            "rule": rule_name,
            "error": str(e),
        })
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=os.getenv("ENVIRONMENT", "development") == "development",
    )
