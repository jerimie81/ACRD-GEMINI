# modules/validator.py

import os
import config
from rich.console import Console

console = Console()

def validate_config():
    """
    Validate the configuration in config.py.
    Checks for API keys and tool paths.
    """
    valid = True
    
    # Check Gemini API Key
    if not config.GEMINI_API_KEY or config.GEMINI_API_KEY == 'your_api_key_here':
        console.print("[yellow]Warning: GEMINI_API_KEY is not set. AI features will be disabled.[/yellow]")
        # We don't mark as invalid because the tool can still work without AI, but with limited functionality
    
    # Check Tool Paths
    tool_paths = {
        "ADB": config.ADB_PATH,
        "Fastboot": config.FASTBOOT_PATH,
        "Heimdall": config.HEIMDALL_PATH,
        "Payload Dumper": config.PAYLOAD_DUMPER_GO_PATH,
        "Lpunpack": config.LPUNPACK_PATH,
        "Apktool": config.APKTOOL_PATH,
        "Jadx": config.JADX_PATH,
        "Avbtool": config.AVBTOOL_PATH,
        "Abootimg": config.ABOOTIMG_PATH,
        "Lpmake": config.LPMAKE_PATH,
    }

    missing_tools = []
    for name, path in tool_paths.items():
        if not os.path.exists(path):
            missing_tools.append(name)
    
    if missing_tools:
        console.print(f"[red]Error: The following tools are missing: {', '.join(missing_tools)}[/red]")
        console.print("[cyan]Please run 'python3 setup.py' to download and configure missing tools.[/cyan]")
        valid = False

    return valid

def validate_environment():
    """
    Perform general environment validation.
    """
    # Check for database directory
    db_dir = os.path.dirname(config.DB_PATH)
    if not os.path.exists(db_dir):
        try:
            os.makedirs(db_dir)
            console.print(f"[green]Created database directory: {db_dir}[/green]")
        except Exception as e:
            console.print(f"[red]Error creating database directory: {str(e)}[/red]")
            return False
    
    return True
