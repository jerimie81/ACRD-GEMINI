# modules/device_quarry.py

import config
from modules.hal import AdbWrapper, FastbootWrapper, HeimdallWrapper
from modules.exceptions import ToolError
from modules import ai_integration
import os
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def quarry_device():
    """
    Detects connected devices and quarries them for information.
    Supports multiple devices and user selection.
    """
    try:
        adb_devices = AdbWrapper.list_devices(config.ADB_PATH)
    except ToolError as e:
        console.print(f"[yellow]Could not list adb devices: {e}[/yellow]")
        adb_devices = []
        
    try:
        fastboot_devices = FastbootWrapper.list_devices(config.FASTBOOT_PATH)
    except ToolError as e:
        console.print(f"[yellow]Could not list fastboot devices: {e}[/yellow]")
        fastboot_devices = []

    all_devices = []
    for d in adb_devices:
        all_devices.append({'serial': d, 'mode': 'adb'})
    for d in fastboot_devices:
        all_devices.append({'serial': d, 'mode': 'fastboot'})

    if not all_devices:
        # Check for Heimdall or EDL as fallback
        try:
            heimdall_wrapper = HeimdallWrapper(config.HEIMDALL_PATH)
            if heimdall_wrapper.detect():
                return quarry_heimdall(heimdall_wrapper)
        except (FileNotFoundError, ToolError) as e:
             console.print(f"[yellow]Heimdall not found or failed: {e}[/yellow]")
        if detect_edl():
            return quarry_edl()
        
        console.print("[red]No device detected.[/red]")
        return None

    selected_device = None
    if len(all_devices) > 1:
        console.print("[yellow]Multiple devices detected:[/yellow]")
        for i, dev in enumerate(all_devices):
            console.print(f"{i+1}. {dev['serial']} ({dev['mode']})")
        
        choice = Prompt.ask("Select a device", choices=[str(i+1) for i in range(len(all_devices))])
        selected_device = all_devices[int(choice)-1]
    else:
        selected_device = all_devices[0]

    if selected_device['mode'] == 'adb':
        try:
            adb_wrapper = AdbWrapper(config.ADB_PATH, serial=selected_device['serial'])
            return quarry_adb(adb_wrapper)
        except (FileNotFoundError, ToolError) as e:
            handle_quarry_error("ADB", e)
    elif selected_device['mode'] == 'fastboot':
        try:
            fastboot_wrapper = FastbootWrapper(config.FASTBOOT_PATH, serial=selected_device['serial'])
            return quarry_fastboot(fastboot_wrapper)
        except (FileNotFoundError, ToolError) as e:
            handle_quarry_error("Fastboot", e)

    return None

def quarry_adb(adb_wrapper):
    """Quarries a device via ADB."""
    try:
        model = adb_wrapper.get_prop("ro.product.model")
        if model:
            return {
                'model': model,
                'brand': adb_wrapper.get_prop("ro.product.brand"),
                'os_version': adb_wrapper.get_prop("ro.product.version.release"),
                'firmware': adb_wrapper.get_prop("ro.build.version.incremental"),
                'security_patch': adb_wrapper.get_prop("ro.build.version.security_patch"),
                'boot_mode': 'adb',
                'serial': adb_wrapper.serial
            }
    except ToolError as e:
        handle_quarry_error("ADB", e)
    return None

def quarry_fastboot(fastboot_wrapper):
    """Quarries a device via Fastboot."""
    try:
        model = fastboot_wrapper.getvar("product")
        if model:
            # Check if it's fastbootd
            is_fastbootd = "yes" in (fastboot_wrapper.getvar("is-userspace") or "")
            return {
                'model': model,
                'brand': fastboot_wrapper.getvar("product"), 
                'os_version': fastboot_wrapper.getvar("os-version"),
                'firmware': fastboot_wrapper.getvar("version-bootloader"),
                'security_patch': None,
                'boot_mode': 'fastbootd' if is_fastbootd else 'fastboot',
                'serial': fastboot_wrapper.serial
            }
    except ToolError as e:
        handle_quarry_error("Fastboot", e)
    return None

def quarry_heimdall(heimdall_wrapper):
    """Quarries a device via Heimdall."""
    try:
        pit_data = heimdall_wrapper.print_pit()
        return {
            'model': 'Samsung Device',
            'brand': 'Samsung',
            'os_version': 'Unknown (Download Mode)',
            'firmware': 'Unknown',
            'security_patch': None,
            'boot_mode': 'download'
        }
    except ToolError as e:
        handle_quarry_error("Heimdall", e)
    return None

def quarry_edl():
    """Quarries a device via EDL."""
    return {
        'model': 'Qualcomm Device',
        'brand': 'Qualcomm',
        'os_version': 'Unknown (EDL Mode)',
        'firmware': 'Unknown',
        'security_patch': None,
        'boot_mode': 'edl'
    }

def detect_edl():
    """Heuristic to detect Qualcomm EDL mode via lsusb."""
    try:
        import subprocess
        result = subprocess.run(['lsusb'], capture_output=True, text=True)
        return "05c6:9008" in result.stdout
    except Exception:
        return False

def handle_quarry_error(tool, error):
    """Handles errors during device quarry using AI diagnostics."""
    console.print(f"[red]{tool} quarry failed: {error}[/red]")
    
    # Read the error recovery prompt template
    template_path = 'templates/error_recovery_prompt.txt'
    if os.path.exists(template_path):
        with open(template_path, 'r') as f:
            template = f.read()
        
        prompt = template.format(log=str(error), issue=f"{tool} device detection/quarry failed", AGENT_TOOL_DOCS_md="AGENT_TOOL_DOCS.md")
        
        # Use Gemini to suggest a fix
        suggestion = ai_integration.gemini_generate_content(prompt)
        console.print(f"[cyan]AI Suggestion for {tool}: {suggestion}[/cyan]")