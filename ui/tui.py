# ui/tui.py (minimal stub for POC)

from rich.console import Console

def launch_tui(device_info):
    console = Console()
    console.print("TUI Launched with device info:", device_info)
    # In full, use Rich for menus
    console.print("Prototype: Select option (download, root, etc.) - not implemented.")
