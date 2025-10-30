"""CLI tool for inspecting and managing configurations"""

import sys
import json
from pathlib import Path
import argparse
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.config.loader import ConfigLoader


def print_json(data):
    """Pretty print data as JSON"""
    if hasattr(data, "model_dump"):
        data = data.model_dump()
    print(json.dumps(data, indent=2, default=str))


def cmd_info(loader: ConfigLoader):
    """Display configuration loader information"""
    info = loader.get_config_info()
    print_json(info)


def cmd_list(loader: ConfigLoader, resource_type: str):
    """List available configurations"""
    if resource_type == "strategies":
        items = loader.list_strategies()
        print("Available strategies:")
    elif resource_type == "agents":
        items = loader.list_agents()
        print("Available agents:")
    elif resource_type == "risk":
        items = loader.list_risk_profiles()
        print("Available risk profiles:")
    else:
        print(f"Unknown resource type: {resource_type}")
        return
    
    for item in items:
        print(f"  - {item}")


def cmd_show(loader: ConfigLoader, resource_type: str, name: str):
    """Show configuration details"""
    try:
        if resource_type == "main":
            config = loader.load_main_config(use_cache=False)
        elif resource_type == "assets":
            config = loader.load_assets_config(use_cache=False)
        elif resource_type == "strategy":
            config = loader.load_strategy_config(name, use_cache=False)
        elif resource_type == "agent":
            config = loader.load_agent_config(name, use_cache=False)
        elif resource_type == "risk":
            config = loader.load_risk_config(name, use_cache=False)
        else:
            print(f"Unknown resource type: {resource_type}")
            return
        
        print_json(config)
    except Exception as e:
        print(f"Error loading configuration: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_validate(loader: ConfigLoader, resource_type: Optional[str] = None):
    """Validate configurations"""
    errors = []
    
    # Validate main config
    if resource_type is None or resource_type == "main":
        try:
            loader.load_main_config(use_cache=False)
            print("✓ main.yaml is valid")
        except Exception as e:
            errors.append(f"✗ main.yaml: {e}")
    
    # Validate assets config
    if resource_type is None or resource_type == "assets":
        try:
            loader.load_assets_config(use_cache=False)
            print("✓ assets.yaml is valid")
        except Exception as e:
            errors.append(f"✗ assets.yaml: {e}")
    
    # Validate all strategies
    if resource_type is None or resource_type == "strategies":
        strategies = loader.list_strategies()
        for strategy in strategies:
            try:
                loader.load_strategy_config(strategy, use_cache=False)
                print(f"✓ strategies/{strategy}.yaml is valid")
            except Exception as e:
                errors.append(f"✗ strategies/{strategy}.yaml: {e}")
    
    # Validate all agents
    if resource_type is None or resource_type == "agents":
        agents = loader.list_agents()
        for agent in agents:
            try:
                loader.load_agent_config(agent, use_cache=False)
                print(f"✓ agents/{agent}.yaml is valid")
            except Exception as e:
                errors.append(f"✗ agents/{agent}.yaml: {e}")
    
    # Validate all risk profiles
    if resource_type is None or resource_type == "risk":
        profiles = loader.list_risk_profiles()
        for profile in profiles:
            try:
                loader.load_risk_config(profile, use_cache=False)
                print(f"✓ risk/{profile}.yaml is valid")
            except Exception as e:
                errors.append(f"✗ risk/{profile}.yaml: {e}")
    
    # Print errors
    if errors:
        print("\nValidation Errors:")
        for error in errors:
            print(error)
        sys.exit(1)
    else:
        print("\n✓ All configurations are valid!")


def main():
    parser = argparse.ArgumentParser(
        description="SelamAI Configuration Management CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Show configuration loader info
  python -m backend.config.cli info

  # List available resources
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
  python -m backend.config.cli validate agents
        """,
    )
    
    parser.add_argument(
        "--config-dir",
        default="config",
        help="Path to configuration directory (default: config)",
    )
    
    parser.add_argument(
        "--environment",
        default=None,
        help="Environment name (development/staging/production)",
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Info command
    subparsers.add_parser("info", help="Show configuration loader information")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List available configurations")
    list_parser.add_argument(
        "type",
        choices=["strategies", "agents", "risk"],
        help="Type of resources to list",
    )
    
    # Show command
    show_parser = subparsers.add_parser("show", help="Show configuration details")
    show_parser.add_argument(
        "type",
        choices=["main", "assets", "strategy", "agent", "risk"],
        help="Type of configuration to show",
    )
    show_parser.add_argument(
        "name",
        nargs="?",
        help="Name of the configuration (required for strategy/agent/risk)",
    )
    
    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate configurations")
    validate_parser.add_argument(
        "type",
        nargs="?",
        choices=["main", "assets", "strategies", "agents", "risk"],
        help="Type of configurations to validate (default: all)",
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Initialize loader
    try:
        loader = ConfigLoader(
            config_dir=args.config_dir,
            environment=args.environment,
        )
    except Exception as e:
        print(f"Error initializing configuration loader: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Execute command
    try:
        if args.command == "info":
            cmd_info(loader)
        elif args.command == "list":
            cmd_list(loader, args.type)
        elif args.command == "show":
            if args.type in ["strategy", "agent", "risk"] and not args.name:
                print(f"Error: name is required for {args.type}", file=sys.stderr)
                sys.exit(1)
            cmd_show(loader, args.type, args.name)
        elif args.command == "validate":
            cmd_validate(loader, args.type)
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
