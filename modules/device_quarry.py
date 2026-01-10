# modules/device_quarry.py

from modules.hal import adb_wrapper, fastboot_wrapper, heimdall_wrapper
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
    adb_devices = adb_wrapper.list_devices()
    fastboot_devices = fastboot_wrapper.list_devices()
    
    all_devices = []
    for d in adb_devices:
        all_devices.append({'serial': d, 'mode': 'adb'})
    for d in fastboot_devices:
        all_devices.append({'serial': d, 'mode': 'fastboot'})

    if not all_devices:
        # Check for Heimdall or EDL as fallback
        if heimdall_wrapper.detect():
            return quarry_heimdall()
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
        adb_wrapper.set_target_device(selected_device['serial'])
        return quarry_adb()
    elif selected_device['mode'] == 'fastboot':
        fastboot_wrapper.set_target_device(selected_device['serial'])
        return quarry_fastboot()

    return None

def quarry_adb():
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
                'serial': adb_wrapper.current_serial
            }
    except Exception as e:
        handle_quarry_error("ADB", e)
    return None

def quarry_fastboot():
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
                'serial': fastboot_wrapper.current_serial
            }
    except Exception as e:
        handle_quarry_error("Fastboot", e)
    return None

def quarry_heimdall():
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
    except Exception as e:
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
    print(f"{tool} quarry failed: {error}")
    
    # Read the error recovery prompt template
    template_path = 'templates/error_recovery_prompt.txt'
    if os.path.exists(template_path):
        with open(template_path, 'r') as f:
            template = f.read()
        
        prompt = template.format(log=str(error), issue=f"{tool} device detection/quarry failed", AGENT_TOOL_DOCS_md="AGENT_TOOL_DOCS.md")
        
        # Use Gemini to suggest a fix
        ai_integration.initialize_gemini()
        suggestion = ai_integration.gemini_generate_content(prompt)
        print(f"AI Suggestion for {tool}: {suggestion}")
