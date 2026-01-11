# modules/diagnostic.py

import logging
import config
from rich.console import Console
from modules.hal import AdbWrapper

logger = logging.getLogger("ACRD")

def run_diagnostics(device_info):
    """
    Runs diagnostics on the device.
    """
    console = Console()
    console.print(f"Running diagnostics for {device_info.get('model', 'Unknown')}:")
    
    if device_info.get('boot_mode') != 'adb' or not device_info.get('serial'):
        console.print("[yellow]Diagnostics require an ADB device with a serial. Skipping.[/yellow]")
        return

    adb = AdbWrapper(config.ADB_PATH, serial=device_info['serial'])

    # 1. Check for root
    root_status = adb.shell(["su", "-c", "echo 'rooted'"])
    if root_status and "rooted" in root_status:
        console.print("[green][✓] Root access: Available[/green]")
    else:
        console.print("[yellow][!] Root access: Not available or su not found[/yellow]")
        
    # 2. Check Battery status
    battery_info = adb.shell(["dumpsys", "battery"])
    if battery_info:
        level = [line for line in battery_info.splitlines() if "level:" in line]
        if level:
            console.print(f"[cyan][i] Battery Level: {level[0].split(':')[1].strip()}%[/cyan]")

    # 3. Check Storage
    storage_info = adb.shell(["df", "-h", "/data"])
    if storage_info:
        lines = storage_info.splitlines()
        if len(lines) > 1:
            console.print(f"[cyan][i] Data Partition: {lines[1]}[/cyan]")

    # 4. Check SELinux status
    selinux = adb.shell(["getenforce"])
    if selinux:
        console.print(f"[cyan][i] SELinux Status: {selinux.strip()}[/cyan]")

    # 5. Check for recent app crashes
    console.print("Checking for recent app crashes...")
    crashes = adb.shell(["logcat", "-d", "-b", "crash", "-t", "10"])
    if crashes and len(crashes.strip()) > 0:
        console.print(f"[red]Found recent crashes:[/red]\n{crashes}")
    else:
        console.print("[green][✓] No recent crashes found.[/green]")

    # 6. Check for any critical errors in dmesg (AI directed)
    console.print("Checking for critical kernel errors...")
    dmesg = adb.shell(["dmesg"])
    if dmesg:
        errors = [line for line in dmesg.splitlines() if "error" in line.lower() or "fail" in line.lower()]
        if errors:
            console.print(f"[red]Found {len(errors)} potential errors in dmesg. Showing last 5:[/red]")
            for err in errors[-5:]:
                console.print(f"  - {err}")
        else:
            console.print("[green][✓] No obvious kernel errors found.[/green]")