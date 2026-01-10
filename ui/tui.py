# ui/tui.py

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from modules import download, root, compile, decompile, diagnostic, debug, repair, ai_integration, db_manager
from modules.exceptions import AIError
import json
import config

console = Console()

def get_tailored_options(option, device_info):
    """Gets tailored options for a specific menu item using AI."""
    try:
        with open('templates/option_tailor_prompt.txt', 'r') as f:
            template = f.read()
        
        prompt = template.format(option=option, device_specs=json.dumps(device_info))
        tailored = ai_integration.gemini_generate_content(prompt)
        
        # Store in DB for caching
        if isinstance(tailored, dict):
            db_manager.store_tailored_options(device_info['model'], option, json.dumps(tailored))
            return tailored
    except (FileNotFoundError, AIError) as e:
        console.print(f"[red]Could not get tailored options: {e}[/red]")
    return {}

def launch_tui(device_info):
    """Launches the Text-based User Interface."""
    # Display device info
    device_panel = Panel(
        f"[bold]Model:[/bold] {device_info['model']}\n"
        f"[bold]Brand:[/bold] {device_info['brand']}\n"
        f"[bold]OS Version:[/bold] {device_info['os_version']}",
        title="Device Information",
        border_style="green"
    )
    console.print(device_panel)

    # Main menu
    menu = Table(show_header=False, show_lines=True)
    menu.add_column("Option", style="cyan")
    menu.add_column("Description")

    menu.add_row("1", "Download")
    menu.add_row("2", "Root")
    menu.add_row("3", "Compile")
    menu.add_row("4", "Decompile")
    menu.add_row("5", "Diagnostic")
    menu.add_row("6", "Debug")
    menu.add_row("7", "Repair")
    menu.add_row("q", "Quit")

    console.print(menu)

    while True:
        choice = console.input("Select an option: ")
        if choice == '1':
            component = console.input("Enter component (e.g., recovery, kernel, firmware): ")
            type = console.input("Enter type (e.g., custom, stock): ")
            download.download_component(device_info['model'], component, type)
        elif choice == '2':
            if console.input("[bold red]WARNING: Rooting can brick your device and voids warranty. Continue? (y/N): [/bold red]").lower() == 'y':
                root.root_device(device_info)
        elif choice == '3':
            compile_menu = Table(show_header=False, show_lines=True)
            compile_menu.add_column("Option", style="cyan")
            compile_menu.add_column("Description")
            compile_menu.add_row("1", "Kernel")
            compile_menu.add_row("2", "ROM")
            compile_menu.add_row("3", "Sign AVB")
            compile_menu.add_row("4", "Create Super Image (lpmake)")
            console.print(compile_menu)
            compile_choice = console.input("Select a compile option: ")
            if compile_choice == '1':
                source_path = console.input("Enter kernel source path: ")
                toolchain_path = console.input("Enter toolchain path: ")
                compile.compile_kernel(source_path, toolchain_path)
            elif compile_choice == '2':
                source_path = console.input("Enter ROM source path: ")
                target_device = device_info['model']
                compile.compile_rom(source_path, target_device)
            elif compile_choice == '3':
                image_path = console.input("Enter image path: ")
                key_path = console.input("Enter key path: ")
                compile.sign_avb(image_path, key_path, config.AVBTOOL_PATH)
            elif compile_choice == '4':
                output_path = console.input("Enter output path: ")
                # partition_info would be gathered here
                compile.lpmake(output_path, {}, config.LPMAKE_PATH)
        elif choice == '4':
            decompile_menu = Table(show_header=False, show_lines=True)
            decompile_menu.add_column("Option", style="cyan")
            decompile_menu.add_column("Description")
            decompile_menu.add_row("1", "APK")
            decompile_menu.add_row("2", "Boot Image")
            decompile_menu.add_row("3", "Payload.bin")
            decompile_menu.add_row("4", "Super Image")
            console.print(decompile_menu)
            decompile_choice = console.input("Select a decompile option: ")
            if decompile_choice == '1':
                apk_path = console.input("Enter APK path: ")
                output_path = console.input("Enter output path: ")
                tool = console.input("Select tool (1 for apktool, 2 for jadx) [1]: ") or "1"
                decompile.decompile_apk(apk_path, output_path, tool='jadx' if tool == '2' else 'apktool', apktool_path=config.APKTOOL_PATH, jadx_path=config.JADX_PATH)
            elif decompile_choice == '2':
                boot_img_path = console.input("Enter boot image path: ")
                output_path = console.input("Enter output path: ")
                decompile.decompile_boot_img(boot_img_path, output_path, config.ABOOTIMG_PATH)
            elif decompile_choice == '3':
                payload_path = console.input("Enter payload.bin path: ")
                output_path = console.input("Enter output path: ")
                decompile.decompile_payload(payload_path, output_path, config.PAYLOAD_DUMPER_GO_PATH)
            elif decompile_choice == '4':
                super_img_path = console.input("Enter super image path: ")
                output_path = console.input("Enter output path: ")
                decompile.decompile_super_img(super_img_path, output_path, config.LPUNPACK_PATH)
        elif choice == '5':
            diagnostic.run_diagnostics(device_info)
        elif choice == '6':
            debug.start_logcat(device_info)
        elif choice == '7':
            if console.input("[bold red]WARNING: Repair/Flashing can result in data loss. Continue? (y/N): [/bold red]").lower() == 'y':
                repair.repair_device(device_info)
        elif choice == 'q':
            break
