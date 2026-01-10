# modules/decompile.py

from rich.console import Console
import subprocess
import os

def decompile_apk(apk_path, output_path, tool='apktool', apktool_path=None, jadx_path=None):
    """
    Decompiles an APK file.
    """
    console = Console()
    if tool == 'apktool':
        if not apktool_path:
            console.print("[red]APKTool path not provided.[/red]")
            return
        console.print(f"Decompiling {apk_path} to {output_path} using apktool...")
        try:
            subprocess.run(['java', '-jar', apktool_path, 'd', apk_path, '-o', output_path], check=True)
            console.print("APK decompilation complete.")
        except Exception as e:
            console.print(f"[red]APK decompilation failed: {e}[/red]")
    elif tool == 'jadx':
        if not jadx_path:
            console.print("[red]JADX path not provided.[/red]")
            return
        console.print(f"Decompiling {apk_path} to {output_path} using jadx...")
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
    console.print(f"Decompiling boot image {boot_img_path} to {output_path}...")
    try:
        os.makedirs(output_path, exist_ok=True)
        # abootimg is often in the system path, but we allow specifying it
        subprocess.run([abootimg_path, '-x', os.path.abspath(boot_img_path)], cwd=output_path, check=True)
        console.print("Boot image decompilation complete.")
    except Exception as e:
        console.print(f"[red]Boot image decompilation failed: {e}[/red]")

def decompile_payload(payload_path, output_path, payload_dumper_path):
    """
    Decompiles (extracts) a payload.bin file.
    """
    console = Console()
    console.print(f"Extracting {payload_path} to {output_path} using payload-dumper-go...")
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
    console.print(f"Unpacking super image {super_img_path} to {output_path} using lpunpack...")
    try:
        subprocess.run([lpunpack_path, super_img_path, output_path], check=True)
        console.print("Super image unpacking complete.")
    except Exception as e:
        console.print(f"[red]Super image unpacking failed: {e}[/red]")