# modules/diagnostic.py

from rich.console import Console
from modules.hal import adb_wrapper

def run_diagnostics(device_info):
    """
    Runs diagnostics on the device.
    """
    console = Console()
    console.print("Running diagnostics...")
    
    # Example diagnostic: check for root
    root_status = adb_wrapper.shell(["su", "-c", "echo 'rooted'"])
    if root_status and "rooted" in root_status:
        console.print("[green]Device is rooted.[/green]")
    else:
        console.print("[yellow]Device is not rooted.[/yellow]")
        
    # TODO: Add more diagnostic checks
