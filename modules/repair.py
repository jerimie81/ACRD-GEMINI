# modules/repair.py

import config
from rich.console import Console
from rich.prompt import Confirm
from modules.hal import AdbWrapper, FastbootWrapper, HeimdallWrapper
from modules import ai_integration
import os

def repair_device(device_info):
    """
    Main repair entry point. 
    Handles flash/soft-brick/hard-brick/SoC/IMEI subsections.
    """
    console = Console()
    console.print(f"[bold red]Repairing Device: {device_info.get('brand', '')} {device_info.get('model', 'Unknown')}[/bold red]")
    
    options = ["Soft-brick Recovery", "Flash Factory Image", "IMEI Repair (Diagnostic)", "Hard-brick (EDL/Download)"]
    for i, opt in enumerate(options):
        console.print(f"{i+1}. {opt}")
    
    choice = console.input("Select repair option: ")
    
    if choice == '1':
        recover_soft_brick(device_info)
    elif choice == '2':
        rom_path = console.input("Enter path to factory image folder: ")
        flash_stock_rom(device_info, rom_path)
    # ... other options

def recover_soft_brick(device_info):
    console = Console()
    console.print("Attempting soft-brick recovery...")
    # AI-driven recovery suggestion
    with open('templates/error_recovery_prompt.txt', 'r') as f:
        template = f.read()
    
    prompt = template.format(log="Device stuck at boot logo", issue="Soft-brick", AGENT_TOOL_DOCS_md="AGENT_TOOL_DOCS.md")
    ai_integration.initialize_gemini()
    suggestion = ai_integration.gemini_generate_content(prompt)
    console.print(f"AI Suggestion: {suggestion}")

def check_battery(device_info):
    """Checks battery level if possible."""
    console = Console()
    if device_info.get('boot_mode') == 'adb' and device_info.get('serial'):
        adb = AdbWrapper(config.ADB_PATH, serial=device_info['serial'])
        # Dumpsys is more reliable for battery info
        battery_info = adb.shell(["dumpsys", "battery"])
        if battery_info:
            level_line = [line for line in battery_info.splitlines() if "level:" in line]
            if level_line:
                level = int(level_line[0].split(':')[1].strip())
                console.print(f"Current battery level: {level}%")
                if level < 20:
                    console.print("[red]Battery level is critically low.[/red]")
                    return Confirm.ask("Continue anyway?", default=False)
                return True
        console.print("[yellow]Could not determine battery level.[/yellow]")
        return Confirm.ask("Continue anyway?", default=True)
    elif device_info.get('boot_mode') in ['fastboot', 'fastbootd']:
        # Fastboot doesn't reliably report battery level, so we have to warn the user
        console.print("[yellow]Cannot check battery in fastboot mode. Please ensure it's adequately charged.[/yellow]")
        return Confirm.ask("Continue anyway?", default=True)
    return True # For other modes, we can't check, so we proceed with caution

def flash_stock_rom(device_info, rom_path):
    """
    Flashes a stock ROM to the device with safety checks.
    """
    console = Console()
    
    # Safety Checks
    if not Confirm.ask("[bold red]WARNING: This operation will wipe data and potentially brick the device. Continue?[/bold red]"):
        console.print("Operation cancelled.")
        return

    if not check_battery(device_info):
        console.print("[red]Battery check failed or user cancelled. Aborting.[/red]")
        return

    console.print(f"Flashing stock ROM from {rom_path}...")
    
    try:
        if device_info.get('boot_mode') in ['fastboot', 'fastbootd'] and device_info.get('serial'):
            fastboot = FastbootWrapper(config.FASTBOOT_PATH, serial=device_info['serial'])
            # Check for flash-all script first
            flash_all_sh = os.path.join(rom_path, "flash-all.sh")
            flash_all_bat = os.path.join(rom_path, "flash-all.bat")
            
            if os.path.exists(flash_all_sh): # Linux/Mac
                 console.print("Executing flash-all.sh... (This is a placeholder, script will not be run)")
                 # subprocess.run(['bash', flash_all_sh], check=True, cwd=rom_path)
            else:
                # Manual flashing of common partitions
                images = {
                    "boot": "boot.img",
                    "system": "system.img",
                    "vendor": "vendor.img",
                    "recovery": "recovery.img",
                    "vbmeta": "vbmeta.img",
                    "dtbo": "dtbo.img"
                }
                
                for partition, img_name in images.items():
                    img_path = os.path.join(rom_path, img_name)
                    if os.path.exists(img_path):
                        console.print(f"Flashing {partition}...")
                        fastboot.flash(partition, img_path)
                    else:
                        console.print(f"[yellow]Skipping {partition} (not found)[/yellow]")
                        
        elif device_info.get('boot_mode') == 'download': # Samsung
            heimdall = HeimdallWrapper(config.HEIMDALL_PATH)
            console.print("Heimdall flashing is not yet implemented.")
            # Heimdall logic to be implemented here
            pass
            
        console.print("[green]Stock ROM flashing complete.[/green]")
        
    except Exception as e:
        console.print(f"[red]Flashing failed: {e}[/red]")