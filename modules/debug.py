# modules/debug.py

from rich.console import Console
from modules.hal import adb_wrapper

def start_logcat(device_info):
    """
    Starts a logcat stream.
    """
    console = Console()
    console.print("Starting logcat stream... (Press Ctrl+C to stop)")
    logcat_process = adb_wrapper.logcat(stream=True)
    if logcat_process:
        try:
            for line in logcat_process.stdout:
                console.print(line, end="")
        except KeyboardInterrupt:
            console.print("\nStopping logcat stream.")
        finally:
            logcat_process.terminate()
