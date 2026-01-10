# main.py

import argparse
import sys
from modules import db_manager, device_quarry, dir_tree_generator, ai_integration
from ui import tui
import config
from rich.console import Console

console = Console()

def main():
    """Main entry point for the ACRD-GEMINI tool."""
    parser = argparse.ArgumentParser(description="ACRD-GEMINI: Android Custom ROM Development Tool")
    parser.add_argument("--quarry-only", action="store_true", help="Only detect and quarry the device, then exit.")
    parser.add_argument("--check-config", action="store_true", help="Validate configuration and tool paths.")
    parser.add_argument("--no-tui", action="store_true", help="Run without TUI (useful for automation).")
    args = parser.parse_args()

    # 1. Validate Config
    if args.check_config:
        if config.validate_config():
            console.print("[green]Configuration is valid.[/green]")
            sys.exit(0)
        else:
            console.print("[red]Configuration validation failed.[/red]")
            sys.exit(1)

    if not config.validate_config():
        console.print("[yellow]Warning: Configuration issues detected. Some features may not work.[/yellow]")

    # 2. Initialize Core Components
    ai_integration.initialize_gemini(config.GEMINI_API_KEY)
    db_manager.init_db()

    # 3. Detect and quarry the device
    device_info = device_quarry.quarry_device()

    if not device_info:
        console.print("[red]Could not find a device. Please ensure it's connected and in ADB or Fastboot mode.[/red]")
        sys.exit(1)

    # Store device info in the database
    db_manager.insert_device_profile(device_info)

    # Generate the device-specific directory tree
    dir_tree_generator.generate_dir_tree(device_info)

    if args.quarry_only:
        console.print(f"[green]Device detected and quarried:[/green] {device_info.get('model', 'Unknown')}")
        sys.exit(0)

    # 4. Launch Interface
    if args.no_tui:
        console.print("[blue]Running in non-TUI mode.[/blue]")
        console.print(f"Device Info: {device_info}")
    else:
        tui.launch_tui(device_info)


if __name__ == '__main__':
    main()