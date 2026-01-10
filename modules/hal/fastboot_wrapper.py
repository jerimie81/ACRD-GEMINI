# modules/hal/fastboot_wrapper.py

import subprocess
import config
import os

current_serial = None

def set_target_device(serial):
    """Sets the target device for fastboot commands."""
    global current_serial
    current_serial = serial

def run_fastboot_command(command):
    """Runs a fastboot command."""
    global current_serial
    full_command = [config.FASTBOOT_PATH]
    if current_serial:
        full_command += ['-s', current_serial]
    
    try:
        # Fastboot often outputs info to stderr
        result = subprocess.run(full_command + command, check=True, capture_output=True, text=True)
        return (result.stdout + result.stderr).strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error executing fastboot command: {e}")
        return None

def list_devices():
    """Lists connected fastboot devices."""
    if not os.path.exists(config.FASTBOOT_PATH):
        return []
    try:
        output = subprocess.run([config.FASTBOOT_PATH, 'devices'], check=True, capture_output=True, text=True).stdout
        devices = []
        for line in output.splitlines():
            if line.strip() and '\tfastboot' in line:
                serial = line.split('\t')[0]
                devices.append(serial)
        return devices
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []

def getvar(variable):
    """Gets a fastboot variable."""
    return run_fastboot_command(['getvar', variable])

def flash(partition, file):
    """Flashes a file to a partition."""
    return run_fastboot_command(['flash', partition, file])

def boot(image):
    """Boots a specific image."""
    return run_fastboot_command(['boot', image])
