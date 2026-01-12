# modules/decompile.py

from rich.console import Console
import subprocess
import os
import config

def decompile_apk(apk_path, output_path, tool='apktool', apktool_path=None, jadx_path=None):
    """
    Decompiles an APK file.
    """
    console = Console()
    if tool == 'apktool':
        resolved_apktool_path = apktool_path or config.APKTOOL_PATH
        if not resolved_apktool_path:
            console.print("[red]APKTool path not provided.[/red]")
            return
        with console.status(f"[bold blue]Decompiling {apk_path} to {output_path} using apktool...", spinner="dots"):
            try:
                subprocess.run(['java', '-jar', resolved_apktool_path, 'd', apk_path, '-o', output_path], check=True)
                console.print("APK decompilation complete.")
            except Exception as e:
                console.print(f"[red]APK decompilation failed: {e}[/red]")
    elif tool == 'jadx':
        if not jadx_path:
            console.print("[red]JADX path not provided.[/red]")
            return
        with console.status(f"[bold blue]Decompiling {apk_path} to {output_path} using jadx...", spinner="dots"):
            try:
                subprocess.run([jadx_path, '-d', output_path, apk_path], check=True)
                console.print("APK decompilation (Java source) complete.")
            except Exception as e:
                console.print(f"[red]JADX decompilation failed: {e}[/red]")

def decompile_boot_img(boot_img_path, output_path, abootimg_path):
    """
    Decompiles a boot image using abootimg.
    """
    console = Console()
    with console.status(f"[bold blue]Decompiling boot image {boot_img_path} to {output_path}...", spinner="dots"):
        try:
            subprocess.run([abootimg_path, '-x', boot_img_path, '-f', output_path], check=True)
            console.print("Boot image decompilation complete.")
        except Exception as e:
            console.print(f"[red]Boot image decompilation failed: {e}[/red]")

def decompile_payload(payload_path, output_path, payload_dumper_path):
    """
    Decompiles (extracts) a payload.bin file.
    """
    console = Console()
    with console.status(f"[bold blue]Extracting {payload_path} to {output_path} using payload-dumper-go...", spinner="dots"):
        try:
            subprocess.run([payload_dumper_path, '-o', output_path, payload_path], check=True)
            console.print("Payload extraction complete.")
        except Exception as e:
            console.print(f"[red]Payload extraction failed: {e}[/red]")

def decompile_super_img(super_img_path, output_path, lpunpack_path):
    """
    Decompiles (unpacks) a super image.
    """
    console = Console()
    with console.status(f"[bold blue]Unpacking super image {super_img_path} to {output_path} using lpunpack...", spinner="dots"):
        try:
            subprocess.run([lpunpack_path, super_img_path, output_path], check=True)
            console.print("Super image unpacking complete.")
        except Exception as e:
            console.print(f"[red]Super image unpacking failed: {e}[/red]")
