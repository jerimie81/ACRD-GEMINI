# modules/hal/device_quarry.py

from adbutils import adb
import subprocess
import re

def quarry_device():
    """Quarry device for info using ADB/fastboot/Heimdall.
    For POC, prioritize ADB; fallback to fastboot if in bootloader.
    Refer to AGENT_TOOL_DOCS.md for tools: adb/fastboot from platform-tools.
    """
    device_info = {
        'model': None,
        'brand': None,
        'os_version': None,
        'firmware': None,
        'security_patch': None
    }

    try:
        # Try ADB first (device booted)
        devices = adb.device_list()
        if devices:
            device = devices[0]  # Assume first device
            # Get props
            device_info['os_version'] = device.shell('getprop ro.build.version.release').strip()
            device_info['security_patch'] = device.shell('getprop ro.build.version.security_patch').strip()
            device_info['model'] = device.shell('getprop ro.product.model').strip()
            device_info['brand'] = device.shell('getprop ro.product.brand').strip()
            device_info['firmware'] = device.shell('getprop ro.build.description').strip()  # Or ro.vendor.build.fingerprint
            return device_info
    except Exception as e:
        print(f"ADB quarry failed: {e}")

    try:
        # Fallback to fastboot (bootloader mode)
        fastboot_output = subprocess.check_output(['fastboot', 'getvar', 'all'], stderr=subprocess.STDOUT).decode()
        # Parse output
        device_info['model'] = re.search(r'product:\s*(.+)', fastboot_output).group(1)
        device_info['brand'] = 'unknown'  # Fastboot may not have brand; infer from model
        # For OS/firmware, may need to boot or use other vars like current-slot, etc.
        # For POC, partial info
        return device_info
    except Exception as e:
        print(f"Fastboot quarry failed: {e}")

    try:
        # Heimdall for Samsung (Download mode)
        heimdall_output = subprocess.check_output(['heimdall', 'print-pit', '--no-reboot'], stderr=subprocess.STDOUT).decode()
        # Parse PIT for model/firmware; heuristic
        # For POC, stub
        device_info['brand'] = 'Samsung'
        # Extract model from PIT if possible
    except Exception as e:
        print(f"Heimdall quarry failed: {e}")

    # Heuristic for boot modes: check adb.server_version() or usb detect
    return device_info if any(device_info.values()) else None
