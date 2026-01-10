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
        # 2. Patch using Magisk (would need tool integration)
        # 3. Flash patched boot image
        # fastboot_wrapper.flash("boot", "patched_boot.img")
        console.print("Magisk root complete (placeholder).")
