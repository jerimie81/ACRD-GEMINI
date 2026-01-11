# modules/root.py

import config
from modules import db_manager, ai_integration
from modules.hal import AdbWrapper, FastbootWrapper
from rich.console import Console
import logging
import json
import os

logger = logging.getLogger("ACRD")

def get_root_warnings(brand, model):
    """Gets rooting warnings for a specific device."""
    with open('templates/root_warning_prompt.txt', 'r') as f:
        prompt_template = f.read()

    prompt = prompt_template.format(brand=brand, model=model)
    return ai_integration.gemini_generate_content(prompt)

def get_root_methods(os_version):
    """Gets available rooting methods for a given OS version."""
    return db_manager.query_methods(os_version)

def root_device(device_info):
    """Roots a device."""
    console = Console()
    logger.info(f"Starting rooting process for {device_info.get('model')}")
    warnings = get_root_warnings(device_info.get('brand'), device_info.get('model'))
    console.print(f"[bold red]WARNINGS:[/bold red]\n{warnings}")
    
    methods = db_manager.query_methods(device_info.get('os_version'))
    if not methods:
        # Fallback to general methods
        methods = db_manager.query_methods("") 
    
    if not methods:
        console.print("No root methods found.")
        return

    console.print("\n[bold]Available Root Methods:[/bold]")
    for i, method in enumerate(methods):
        console.print(f"{i+1}. [bold cyan]{method['name']}[/bold cyan] - {method['description']}")
        if method.get('pros'):
            console.print(f"   [green]Pros:[/green] {method['pros']}")
        if method.get('cons'):
            console.print(f"   [red]Cons:[/red] {method['cons']}")
        if method.get('compatibility'):
            console.print(f"   [blue]Compatibility:[/blue] {method['compatibility']}")

    console.print(f"{len(methods)+1}. [bold yellow]Show Root Evasion Techniques[/bold yellow]")

    choice = console.input("\nSelect an option: ")
    try:
        choice = int(choice)
        if 1 <= choice <= len(methods):
            selected_method = methods[choice - 1]
            execute_root_method(selected_method, device_info)
        elif choice == len(methods) + 1:
            show_evasion_techniques()
        else:
            console.print("Invalid selection.")
    except ValueError:
        console.print("Invalid input.")

def show_evasion_techniques():
    """Displays common root evasion techniques."""
    console = Console()
    console.print("\n[bold underline]Top Root Evasion Techniques[/bold underline]")
    techniques = [
        {"name": "Magisk DenyList/Zygisk", "desc": "Hides root from specific apps via process isolation.", "success": "85-90%", "comp": "Android 8+"},
        {"name": "Shamiko Module", "desc": "Advanced hiding for Magisk/Zygisk; obfuscates mounts and props.", "success": "90-95%", "comp": "Android 12+ (GKI kernels)"},
        {"name": "Play Integrity Fixes", "desc": "Modules to spoof attestation (e.g., for banking apps).", "success": "80-90%", "comp": "Android 14+"},
        {"name": "Frida Hooking", "desc": "Runtime injection to alter detection functions.", "success": "80-95%", "comp": "Android 7+"},
        {"name": "Smali Code Tampering", "desc": "Modify app's bytecode to bypass checks.", "success": "70-80%", "comp": "Any"},
    ]
    
    for tech in techniques:
        console.print(f"- [bold]{tech['name']}[/bold]: {tech['desc']}")
        console.print(f"  Success Rate: {tech['success']} | Compatibility: {tech['comp']}")
    console.print("\n[i]Note: Many of these require a specific root method (like Magisk) and additional modules.[/i]")

def execute_root_method(method, device_info):
    """Executes a tailored root method."""
    console = Console()
    console.print(f"\n[bold]Executing {method['name']}...[/bold]")
    
    reqs = {}
    if method.get('requirements'):
        try:
            reqs = json.loads(method['requirements'])
        except json.JSONDecodeError:
            pass

    # Improved bootloader unlock check
    bootloader_unlocked = False
    if device_info.get('boot_mode') in ['fastboot', 'fastbootd'] and device_info.get('serial'):
        fb = FastbootWrapper(config.FASTBOOT_PATH, serial=device_info['serial'])
        unlocked_var = fb.getvar('unlocked')
        if unlocked_var and 'yes' in unlocked_var.lower():
            bootloader_unlocked = True
    
    if reqs.get('bootloader_unlock') and not bootloader_unlocked:
        console.print("[red]Error: Bootloader must be unlocked for this method.[/red]")
        console.print("[i]General Unlock Steps:[/i]")
        console.print("1. Enable USB debugging and OEM unlocking in Developer Options.")
        console.print("2. Reboot to bootloader: `adb reboot bootloader` or use hardware buttons.")
        console.print("3. Run: `fastboot flashing unlock` or `fastboot oem unlock` (WIPES DATA!)")
        if device_info.get('brand') == 'Samsung':
            console.print("[yellow]Samsung note: Bootloader unlock often requires long-pressing VolUp in the bootloader menu.[/yellow]")
        return

    # General Implementation Steps
    console.print("\n[bold]Implementation Steps:[/bold]")
    console.print("1. Obtain stock ROM/boot image from official sources (e.g., SamFW for Samsung).")
    console.print(f"2. Download {method['name']} app/APK from official GitHub releases.")
    
    if method['name'] in ['Magisk', 'Kitsune Mask']:
        console.print(f"3. Patch boot.img (or init_boot.img) using the {method['name']} app.")
        console.print("4. Flash patched image: `fastboot flash boot patched_boot.img`")
    elif method['name'] in ['KernelSU', 'APatch']:
        console.print(f"3. Extract and patch kernel image (or boot.img for GKI) using the {method['name']} app.")
        console.print("4. Flash patched image via fastboot.")
    elif 'Samsung' in method['name']:
        console.print(f"3. Extract AP file from firmware and patch via Magisk/{method['name']} app.")
        console.print("4. Flash patched AP tar file via Odin in AP slot.")
    
    console.print("5. Reboot and grant root permissions in the app.")
    
    if method['name'] in ['Magisk', 'Kitsune Mask']:
        # Legacy logic for boot image pulling if possible
        if device_info.get('boot_mode') == 'adb' and device_info.get('serial'):
            console.print("\n[i]Attempting automated boot image pull (Requires existing root or specific exploit)...[/i]")
            adb = AdbWrapper(config.ADB_PATH, serial=device_info['serial'])
            if not os.path.exists('devices'):
                os.makedirs('devices')
            console.print("[yellow]Automated pull is often restricted on modern Android without prior root.[/yellow]")
            console.print("[yellow]It is safer to manually extract boot.img from your device's stock firmware.[/yellow]")

    db_manager.log_operation(device_info.get('model'), "Root", f"{method['name']} instructions provided", "INFO")
    console.print(f"\n{method['name']} root instructions complete.")
