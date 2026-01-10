# modules/hal/adb_wrapper.py

import subprocess
import config
import os

current_serial = None

def set_target_device(serial):
    """Sets the target device for ADB commands."""
    global current_serial
    current_serial = serial

def run_adb_command(command):
    """Runs an ADB command."""
    global current_serial
    full_command = [config.ADB_PATH]
    if current_serial:
        full_command += ['-s', current_serial]
    
    try:
        result = subprocess.run(full_command + command, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error executing ADB command: {e}")
        return None

def list_devices():
    """Lists connected ADB devices."""
    if not os.path.exists(config.ADB_PATH):
        return []
    try:
        output = subprocess.run([config.ADB_PATH, 'devices'], check=True, capture_output=True, text=True).stdout
        devices = []
        for line in output.splitlines()[1:]:
            if line.strip() and '\tdevice' in line:
                serial = line.split('\t')[0]
                devices.append(serial)
        return devices
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []

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
