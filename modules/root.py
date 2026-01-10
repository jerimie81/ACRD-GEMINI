# modules/root.py

from modules import db_manager
from modules import ai_integration
from modules.hal import adb_wrapper, fastboot_wrapper
from rich.console import Console
import json

def get_root_warnings(brand, model):
    """Gets rooting warnings for a specific device."""
    with open('templates/root_warning_prompt.txt', 'r') as f:
        prompt_template = f.read()

    prompt = prompt_template.format(brand=brand, model=model)
    ai_integration.initialize_gemini()
    return ai_integration.gemini_generate_content(prompt)

def get_root_methods(os_version):
    """Gets available rooting methods for a given OS version."""
    return db_manager.query_methods(os_version)

def root_device(device_info):
    """Roots a device."""
    console = Console()
    warnings = get_root_warnings(device_info['brand'], device_info['model'])
    console.print(f"[bold red]WARNINGS:[/bold red]\n{warnings}")
    
    methods = get_root_methods(device_info['os_version'])
    if not methods:
        console.print("No root methods found for this OS version.")
        return

    console.print("Available root methods:")
    for i, method in enumerate(methods):
        console.print(f"{i+1}. {method[0]} - {method[1]}")

    choice = console.input("Select a method: ")
    try:
        choice = int(choice) - 1
        if 0 <= choice < len(methods):
            selected_method = methods[choice]
            execute_root_method(selected_method, device_info)
        else:
            console.print("Invalid selection.")
    except ValueError:
        console.print("Invalid input.")

def execute_root_method(method, device_info):
    """Executes a tailored root method."""
    console = Console()
    name, description, pros, cons, compatibility, requirements = method
    console.print(f"Executing {name}...")
    
    reqs = json.loads(requirements)
    if reqs.get('bootloader_unlock') and not device_info.get('bootloader_unlocked'):
        console.print("[red]Error: Bootloader must be unlocked for this method.[/red]")
        return

    if name == 'Magisk':
        # Magisk patching logic
        console.print("Magisk selected. Patching boot image...")
        # 1. Pull boot image
        console.print("[i] Pulling boot.img from device...")
        # adb_wrapper.shell(["dd", "if=/dev/block/by-name/boot", "of=/sdcard/boot.img"])
        # adb_wrapper.run_adb_command(["pull", "/sdcard/boot.img", "devices/boot.img"])
        
        console.print("[i] In a real scenario, you would now patch this image via Magisk app or a script.")
        console.print("[i] Once patched, flash it back via fastboot:")
        console.print("    fastboot flash boot magisk_patched.img")
        
        db_manager.log_operation(device_info['model'], "Root", "Magisk patching initiated (instructions provided)", "INFO")
        console.print("Magisk root instructions complete.")
    elif name == 'KernelSU':
        console.print("KernelSU selected. Requires a GKI-compatible kernel.")
        console.print("[i] Check if your device supports GKI (Android 12+ usually).")
        # Logic to check GKI could be added to diagnostic.py
        console.print("KernelSU root complete (placeholder).")
    else:
        console.print(f"Method {name} selected. Please follow tailored instructions.")
