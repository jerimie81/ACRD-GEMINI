# modules/hal/fastboot_wrapper.py

import subprocess
import config

def run_fastboot_command(command):
    """Runs a fastboot command."""
    try:
        # Fastboot often outputs info to stderr
        result = subprocess.run([config.FASTBOOT_PATH] + command, check=True, capture_output=True, text=True)
        return (result.stdout + result.stderr).strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error executing fastboot command: {e}")
        return None

def getvar(variable):
    """Gets a fastboot variable."""
    return run_fastboot_command(['getvar', variable])

def flash(partition, file):
    """Flashes a file to a partition."""
    return run_fastboot_command(['flash', partition, file])

def boot(image):
    """Boots a specific image."""
    return run_fastboot_command(['boot', image])
