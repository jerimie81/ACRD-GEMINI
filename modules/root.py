# modules/root.py

import config
from modules import db_manager
from modules import ai_integration
from modules.hal import AdbWrapper, FastbootWrapper
from rich.console import Console
import json
import os

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
    warnings = get_root_warnings(device_info.get('brand'), device_info.get('model'))
    console.print(f"[bold red]WARNINGS:[/bold red]\n{warnings}")
    
    methods = get_root_methods(device_info.get('os_version'))
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
    # This check needs to be improved. We should get the unlocked status from fastboot.
    # For now, we'll assume it's unlocked if we are in fastboot mode.
    bootloader_unlocked = device_info.get('boot_mode') in ['fastboot', 'fastbootd']
    
    if reqs.get('bootloader_unlock') and not bootloader_unlocked:
        console.print("[red]Error: Bootloader must be unlocked for this method. Please boot into fastboot to check.[/red]")
        return

    if name == 'Magisk':
        # Magisk patching logic
        console.print("Magisk selected. Patching boot image...")
        if device_info.get('boot_mode') == 'adb' and device_info.get('serial'):
            adb = AdbWrapper(config.ADB_PATH, serial=device_info['serial'])
            # 1. Pull boot image
            console.print("[i] Pulling boot.img from device...")
            
            # Create devices directory if it doesn't exist
            if not os.path.exists('devices'):
                os.makedirs('devices')
            
            # Use dd to copy the boot image to sdcard, then pull it
            # Note: This is a risky operation and should be handled with care.
            # The actual block path might differ.
            # adb.shell(["dd", "if=/dev/block/by-name/boot", "of=/sdcard/boot.img"])
            # adb.pull("/sdcard/boot.img", f"devices/{device_info.get('model', 'device')}_boot.img")
            console.print("[yellow]Copying and pulling boot image is a critical step and is not yet automated.[/yellow]")
            console.print("[yellow]You would typically find the boot image in your firmware files.[/yellow]")

        console.print("[i] In a real scenario, you would now patch this image via Magisk app or a script.")
        console.print("[i] Once patched, flash it back via fastboot:")
        console.print("    fastboot flash boot magisk_patched.img")
        
        db_manager.log_operation(device_info.get('model'), "Root", "Magisk patching initiated (instructions provided)", "INFO")
        console.print("Magisk root instructions complete.")
    elif name == 'KernelSU':
        console.print("KernelSU selected. Requires a GKI-compatible kernel.")
        console.print("[i] Check if your device supports GKI (Android 12+ usually).")
        # Logic to check GKI could be added to diagnostic.py
        console.print("KernelSU root complete (placeholder).")
    else:
        console.print(f"Method {name} selected. Please follow tailored instructions.")