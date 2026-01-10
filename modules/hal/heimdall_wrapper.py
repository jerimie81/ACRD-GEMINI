# modules/hal/heimdall_wrapper.py

import subprocess
import config

def run_heimdall_command(command):
    """Runs a Heimdall command."""
    try:
        result = subprocess.run([config.HEIMDALL_PATH] + command, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error executing Heimdall command: {e}")
        return None

def detect():
    """Checks if a device is in Download Mode (Samsung)."""
    result = run_heimdall_command(['detect'])
    return "Device detected" in (result or "")

def print_pit():
    """Downloads and prints the PIT file from the device."""
    return run_heimdall_command(['print-pit', '--no-reboot'])

def flash(partition_name, file_path):
    """Flashes a partition."""
    return run_heimdall_command(['flash', '--' + partition_name, file_path])
