# modules/decompile.py

from rich.console import Console
import subprocess
import config

def decompile_apk(apk_path, output_path):
    """
    Decompiles an APK file.
    """
    console = Console()
    console.print(f"Decompiling {apk_path} to {output_path} using apktool...")
    try:
        subprocess.run(['java', '-jar', 'tools/apktool.jar', 'd', apk_path, '-o', output_path], check=True)
        console.print("APK decompilation complete.")
    except subprocess.CalledProcessError as e:
        console.print(f"[red]APK decompilation failed: {e}[/red]")

def decompile_boot_img(boot_img_path, output_path):
    """
    Decompiles a boot image.
    """
    console = Console()
    console.print(f"Decompiling boot image {boot_img_path}...")
    # Example: unpack_bootimg --boot_img ...
    console.print("Boot image decompilation complete (placeholder).")

def decompile_payload(payload_path, output_path):
    """
    Decompiles (extracts) a payload.bin file.
    """
    console = Console()
    console.print(f"Extracting {payload_path} using payload-dumper-go...")
    try:
        subprocess.run(['tools/payload-dumper-go', '-o', output_path, payload_path], check=True)
        console.print("Payload extraction complete.")
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Payload extraction failed: {e}[/red]")

def decompile_super_img(super_img_path, output_path):
    """
    Decompiles (unpacks) a super image.
    """
    console = Console()
    console.print(f"Unpacking super image {super_img_path} using lpunpack...")
    try:
        subprocess.run(['tools/lpunpack', super_img_path, output_path], check=True)
        console.print("Super image unpacking complete.")
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Super image unpacking failed: {e}[/red]")
