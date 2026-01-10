# modules/debug.py

import config
from rich.console import Console
from modules.hal import AdbWrapper

def start_logcat(device_info):
    """
    Starts a logcat stream with filtering options.
    """
    console = Console()
    
    if not device_info or 'serial' not in device_info:
        console.print("[red]Error: Device information with serial is required.[/red]")
        return
        
    adb_wrapper = AdbWrapper(config.ADB_PATH, serial=device_info['serial'])

    console.print("[bold]Logcat Options:[/bold]")
    console.print("1. All logs")
    console.print("2. Filter by Tag")
    console.print("3. Filter by Level (V, D, I, W, E, F)")
    console.print("4. Filter by String (grep)")
    
    choice = console.input("Select option: ")
    options = []
    
    if choice == '2':
        tag = console.input("Enter tag: ")
        options = ["-s", tag]
    elif choice == '3':
        level = console.input("Enter level (e.g., E for Error): ")
        options = [f"*:{{level}}"]
    elif choice == '4':
        # grep is handled by piping, which is tricky with Popen directly on adb logcat
        # adb logcat doesn't have a built-in grep, but we can filter in python
        search_term = console.input("Enter search string: ")
        console.print(f"Starting logcat stream filtered by '{{search_term}}'... (Press Ctrl+C to stop)")
        
        logcat_process = adb_wrapper.logcat(stream=True)
        if logcat_process:
            try:
                for line in logcat_process.stdout:
                    if search_term in line:
                        console.print(line, end="")
            except KeyboardInterrupt:
                console.print("\nStopping logcat stream.")
            finally:
                logcat_process.terminate()
        return

    console.print("Starting logcat stream... (Press Ctrl+C to stop)")
    logcat_process = adb_wrapper.logcat(options=options, stream=True)
    if logcat_process:
        try:
            for line in logcat_process.stdout:
                console.print(line, end="")
        except KeyboardInterrupt:
            console.print("\nStopping logcat stream.")
        finally:
            logcat_process.terminate()