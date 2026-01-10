# modules/device_quarry.py

from modules.hal import adb_wrapper, fastboot_wrapper, heimdall_wrapper
from modules import ai_integration
import os

def quarry_device():
    """
    Detects connected devices and quarries them for information.
    Prioritizes ADB, then falls back to fastboot, then heimdall.
    """
    try:
        # Try ADB first
        model = adb_wrapper.get_prop("ro.product.model")
        if model:
            return {
                'model': model,
                'brand': adb_wrapper.get_prop("ro.product.brand"),
                'os_version': adb_wrapper.get_prop("ro.product.version.release"),
                'firmware': adb_wrapper.get_prop("ro.build.version.incremental"),
                'security_patch': adb_wrapper.get_prop("ro.build.version.security_patch"),
                'boot_mode': 'adb'
            }
    except Exception as e:
        handle_quarry_error("ADB", e)

    try:
        # Fallback to fastboot
        model = fastboot_wrapper.getvar("product")
        if model:
            # Check if it's fastbootd
            is_fastbootd = fastboot_wrapper.getvar("is-userspace") == "yes"
            return {
                'model': model,
                'brand': fastboot_wrapper.getvar("product"), # Fastboot doesn't have a standard brand field
                'os_version': fastboot_wrapper.getvar("os-version"),
                'firmware': fastboot_wrapper.getvar("version-bootloader"),
                'security_patch': None, # Not available in fastboot
                'boot_mode': 'fastbootd' if is_fastbootd else 'fastboot'
            }
    except Exception as e:
        handle_quarry_error("Fastboot", e)

    try:
        # Fallback to Heimdall (Samsung Download Mode)
        if heimdall_wrapper.detect():
            pit_data = heimdall_wrapper.print_pit()
            # Extracting model from PIT is complex, but often present in some form. 
            # For now, we'll label it as Samsung and try to get more info later.
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

    print("No device detected.")
    return None

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
