# modules/hal/adb_wrapper.py

import subprocess
import config

def run_adb_command(command):
    """Runs an ADB command."""
    try:
        result = subprocess.run([config.ADB_PATH] + command, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error executing ADB command: {e}")
        return None

def get_prop(prop):
    """Gets a device property."""
    return run_adb_command(['shell', 'getprop', prop])

def shell(command):
    """Executes a shell command on the device."""
    return run_adb_command(['shell'] + command)

def logcat(options=None, stream=False):
    """Gets a device logcat. If stream is True, returns a subprocess.Popen object."""
    if options is None:
        options = []
    
    command = [config.ADB_PATH, 'logcat'] + options
    if stream:
        return subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error executing ADB logcat: {e}")
        return None

def dmesg():
    """Gets the device's dmesg log."""
    return run_adb_command(['shell', 'dmesg'])
