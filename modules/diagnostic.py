# modules/diagnostic.py

from rich.console import Console
from modules.hal import adb_wrapper

def run_diagnostics(device_info):
    """
    Runs diagnostics on the device.
    """
    console = Console()
    console.print(f"Running diagnostics for {device_info['model']}...")
    
    # 1. Check for root
    root_status = adb_wrapper.shell(["su", "-c", "echo 'rooted'"])
    if root_status and "rooted" in root_status:
        console.print("[green][✓] Root access: Available[/green]")
    else:
        console.print("[yellow][!] Root access: Not available or su not found[/yellow]")
        
    # 2. Check Battery status
    battery_info = adb_wrapper.shell(["dumpsys", "battery"])
    if battery_info:
        level = [line for line in battery_info.splitlines() if "level:" in line]
        if level:
            console.print(f"[cyan][i] Battery Level: {level[0].split(':')[1].strip()}%[/cyan]")

    # 3. Check Storage
    storage_info = adb_wrapper.shell(["df", "/data"])
    if storage_info:
        lines = storage_info.splitlines()
        if len(lines) > 1:
            console.print(f"[cyan][i] Data Partition: {lines[1]}[/cyan]")

    # 4. Check SELinux status
    selinux = adb_wrapper.shell(["getenforce"])
    if selinux:
        console.print(f"[cyan][i] SELinux Status: {selinux.strip()}[/cyan]")

    # 5. Check for any critical errors in dmesg (AI directed)
    console.print("Checking for critical kernel errors...")
    dmesg = adb_wrapper.shell(["dmesg", "|", "grep", "-i", "error", "|", "tail", "-n", "5"])
    if dmesg:
        console.print(f"[red]Found potential errors in dmesg:[/red]\n{dmesg}")
        # Could use AI here to interpret
