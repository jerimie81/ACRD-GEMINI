# config.py

import os
import sys
from rich.console import Console

console = Console()

# Gemini API Key
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'your_api_key_here')

# Database Path
DB_PATH = 'db/acrd.db'

# Tool Paths
ADB_PATH = 'tools/adb'
FASTBOOT_PATH = 'tools/fastboot'
HEIMDALL_PATH = 'tools/heimdall'
PAYLOAD_DUMPER_GO_PATH = 'tools/payload-dumper-go'
LPUNPACK_PATH = 'tools/lpunpack'
APKTOOL_PATH = 'tools/apktool.jar'
JADX_PATH = 'tools/jadx'
AVBTOOL_PATH = 'tools/avbtool.py'
ABOOTIMG_PATH = 'tools/abootimg'
LPMAKE_PATH = 'tools/lpmake'

def validate_config():
    """
    Validate the configuration in config.py.
    Checks for API keys and tool paths.
    """
    errors = []
    
    # Check Gemini API Key
    if not GEMINI_API_KEY or GEMINI_API_KEY == 'your_api_key_here':
        console.print("[yellow]Warning: GEMINI_API_KEY is not set. AI features will be disabled.[/yellow]")
    
    # Check Tool Paths
    tool_paths = {
        "ADB": ADB_PATH,
        "Fastboot": FASTBOOT_PATH,
        "Heimdall": HEIMDALL_PATH,
        "Payload Dumper": PAYLOAD_DUMPER_GO_PATH,
        "Lpunpack": LPUNPACK_PATH,
        "Apktool": APKTOOL_PATH,
        "Jadx": JADX_PATH,
        "Avbtool": AVBTOOL_PATH,
        "Abootimg": ABOOTIMG_PATH,
        "Lpmake": LPMAKE_PATH,
    }

    missing_tools = []
    for name, path in tool_paths.items():
        if not os.path.exists(path):
            missing_tools.append(name)
    
    if missing_tools:
        errors.append(f"The following tools are missing: {', '.join(missing_tools)}")
        errors.append("Please run 'python3 setup.py' to download and configure missing tools.")

    # Check for database directory
    db_dir = os.path.dirname(DB_PATH)
    if not os.path.exists(db_dir):
        try:
            os.makedirs(db_dir)
            console.print(f"[green]Created database directory: {db_dir}[/green]")
        except Exception as e:
            errors.append(f"Error creating database directory: {str(e)}")
            
    if errors:
        console.print("[red]Configuration Errors:[/red]")
        for error in errors:
            console.print(f"  - {error}")
        return False
        
    return True