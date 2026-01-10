# setup.py

import os
import requests
import subprocess
import sys
from modules import db_manager

# Tools metadata from ACRD-toolset.md
TOOL_METADATA = {
    "adb": {
        "category": "Core / Debugging",
        "doc_url": "https://developer.android.com/tools/adb",
        "download_url": "https://dl.google.com/android/repository/platform-tools-latest-linux.zip",
        "type": "zip"
    },
    "fastboot": {
        "category": "Flashing / Bootloader",
        "doc_url": "https://android.googlesource.com/platform/system/core/+/master/fastboot/README.md",
        "download_url": "https://dl.google.com/android/repository/platform-tools-latest-linux.zip",
        "type": "zip"
    },
    "heimdall": {
        "category": "Flashing",
        "doc_url": "https://heimdal.readthedocs.io/en/latest/",
        "download_url": None,
        "type": "manual"
    },
    "payload-dumper-go": {
        "category": "Extraction",
        "doc_url": "https://github.com/ssut/payload-dumper-go",
        "download_url": "https://github.com/ssut/payload-dumper-go/releases/download/1.2.2/payload-dumper-go_1.2.2_linux_amd64.tar.gz",
        "type": "tar.gz"
    },
    "lpunpack": {
        "category": "Extraction",
        "doc_url": "https://github.com/unix3dgforce/lpunpack",
        "download_url": None, # Source code usually
        "type": "binary"
    },
    "apktool": {
        "category": "Decompilation",
        "doc_url": "https://apktool.org/docs/install/",
        "download_url": "https://github.com/iBotPeaches/Apktool/releases/download/v2.9.3/apktool_2.9.3.jar",
        "type": "jar"
    },
    "jadx": {
        "category": "Decompilation",
        "doc_url": "https://github.com/skylot/jadx/wiki",
        "download_url": "https://github.com/skylot/jadx/releases/download/v1.4.7/jadx-1.4.7.zip",
        "type": "zip"
    },
    "avbtool": {
        "category": "Image Manipulation",
        "doc_url": "https://android.googlesource.com/platform/external/avb/+/master/avbtool.py",
        "download_url": "https://android.googlesource.com/platform/external/avb/+/master/avbtool.py?format=TEXT",
        "type": "python"
    },
    "frida-tools": {
        "category": "Instrumentation",
        "doc_url": "https://frida.re/docs/home/",
        "download_url": None, # Install via pip usually
        "type": "pip"
    },
    "odin": {
        "category": "Flashing",
        "doc_url": "https://forum.xda-developers.com/",
        "download_url": None, # Proprietary
        "type": "manual"
    },
    "sp-flash-tool": {
        "category": "Flashing",
        "doc_url": "http://mirtorg.ru/upload/iblock/7a1/7a19c9aee42ad8b73646e2ef7e6f3c8c.pdf",
        "download_url": None, # Manual download
        "type": "manual"
    },
    "qualcomm-edl": {
        "category": "Flashing / Unbricking",
        "doc_url": "https://en.wikipedia.org/wiki/Qualcomm_EDL_mode",
        "download_url": None, # Manual
        "type": "manual"
    },
    "abootimg": {
        "category": "Image Manipulation",
        "doc_url": "https://github.com/ggrandou/abootimg",
        "download_url": None, # Build from source
        "type": "source"
    },
    "simg2img": {
        "category": "Conversion",
        "doc_url": "https://github.com/anestisb/android-simg2img",
        "download_url": None, # Build from source
        "type": "source"
    },
    "binwalk": {
        "category": "Analysis / Extraction",
        "doc_url": "https://github.com/ReFirmLabs/binwalk/wiki",
        "download_url": None, # Install via apt/pip
        "type": "package"
    },
    "androguard": {
        "category": "Analysis",
        "doc_url": "https://androguard.readthedocs.io/",
        "download_url": None, # Install via pip
        "type": "pip"
    },
    "radare2": {
        "category": "Disassembly / Debugging",
        "doc_url": "https://book.rada.re/",
        "download_url": None, # Install via apt/brew
        "type": "package"
    },
    "dex2jar": {
        "category": "Conversion",
        "doc_url": "https://github.com/pxb1988/dex2jar",
        "download_url": "https://github.com/pxb1988/dex2jar/releases/download/v2.4/dex-tools-v2.4.zip",
        "type": "zip"
    },
    "enjarify": {
        "category": "Conversion",
        "doc_url": "https://github.com/google/enjarify",
        "download_url": None, # Clone repo
        "type": "source"
    },
    "bytecode-viewer": {
        "category": "Suite (GUI)",
        "doc_url": "https://github.com/Konloch/bytecode-viewer",
        "download_url": "https://github.com/Konloch/bytecode-viewer/releases/download/v2.11.2/Bytecode-Viewer-2.11.2.jar",
        "type": "jar"
    },
    "mobsf": {
        "category": "Security Auditing",
        "doc_url": "https://mobsf.github.io/docs/",
        "download_url": None, # Docker/Pip
        "type": "manual"
    },
    "qark": {
        "category": "Static Analysis",
        "doc_url": "https://github.com/linkedin/qark",
        "download_url": None, # Pip
        "type": "pip"
    },
    "magisk": {
        "category": "Rooting",
        "doc_url": "https://github.com/topjohnwu/Magisk/blob/master/docs/guides.md",
        "download_url": "https://github.com/topjohnwu/Magisk/releases/download/v27.0/Magisk-v27.0.apk",
        "type": "apk"
    },
    "kernelsu": {
        "category": "Rooting",
        "doc_url": "https://kernelsu.org/",
        "download_url": None, # Kernel specific
        "type": "manual"
    },
    "twrp": {
        "category": "Recovery",
        "doc_url": "https://twrp.me/",
        "download_url": None, # Device specific
        "type": "manual"
    },
    "orangefox": {
        "category": "Recovery",
        "doc_url": "https://wiki.orangefox.tech/",
        "download_url": None, # Device specific
        "type": "manual"
    },
    "xposed": {
        "category": "Modding",
        "doc_url": "https://forum.xda-developers.com/f/xposed-general.3033/",
        "download_url": None, # Legacy
        "type": "manual"
    },
    "aapt2": {
        "category": "Build Tool",
        "doc_url": "https://developer.android.com/tools/aapt2",
        "download_url": "https://dl.google.com/android/repository/build-tools_r34-linux.zip",
        "type": "zip"
    },
    "uber-apk-signer": {
        "category": "Utility",
        "doc_url": "https://github.com/patrickfav/uber-apk-signer",
        "download_url": "https://github.com/patrickfav/uber-apk-signer/releases/download/v1.3.0/uber-apk-signer-1.3.0.jar",
        "type": "jar"
    },
    "7zip": {
        "category": "Compression",
        "doc_url": "https://sevenzip.osdn.jp/chm/cmdline/index.htm",
        "download_url": None, # System package
        "type": "package"
    }
}

def download_file(url, dest_path):
    """Downloads a file."""
    print(f"Downloading {url} to {dest_path}...")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(dest_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def extract_file(file_path, dest_folder, file_type):
    """Extracts a file based on its type."""
    print(f"Extracting {file_path} to {dest_folder}...")
    if file_type == "zip":
        subprocess.run(["unzip", "-o", file_path, "-d", dest_folder], check=True)
    elif file_type == "tar.gz":
        subprocess.run(["tar", "-xzf", file_path, "-C", dest_folder], check=True)
    elif file_type == "jar":
        # Just move/copy the jar
        os.makedirs(dest_folder, exist_ok=True)
        os.rename(file_path, os.path.join(dest_folder, os.path.basename(file_path)))
    elif file_type == "python":
        # Just move the py file
        os.makedirs(dest_folder, exist_ok=True)
        # Base64 decode if it was ?format=TEXT from googlesource
        import base64
        with open(file_path, 'r') as f:
            content = f.read()
        try:
            decoded_content = base64.b64decode(content).decode('utf-8')
            with open(os.path.join(dest_folder, os.path.basename(file_path).replace('?format=TEXT', '')), 'w') as f:
                f.write(decoded_content)
        except Exception:
             os.rename(file_path, os.path.join(dest_folder, os.path.basename(file_path).replace('?format=TEXT', '')))
    elif file_type == "apk":
         os.makedirs(dest_folder, exist_ok=True)
         os.rename(file_path, os.path.join(dest_folder, os.path.basename(file_path)))
    
    if os.path.exists(file_path) and not file_type in ["jar", "python", "apk"]:
        os.remove(file_path)

def check_dependencies():
    """Checks for required system dependencies."""
    print("Checking dependencies...")
    # Check for Python 3.10+
    if sys.version_info < (3, 10):
        print("Error: Python 3.10 or higher is required.")
        sys.exit(1)

    # Check for OpenJDK/JRE
    try:
        subprocess.run(["java", "-version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: OpenJDK/JRE is not installed. Please install it.")
        sys.exit(1)
        
    # Check for libusb
    try:
        subprocess.run(["lsusb"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Warning: libusb is not installed. This may be required for some devices.")


def main():
    """Main setup script."""
    check_dependencies()

    # Initialize the database
    db_manager.init_db()

    # Download and set up tools
    for tool_name, metadata in TOOL_METADATA.items():
        url = metadata.get("download_url")
        dest_folder = os.path.join("tools", tool_name)
        
        if url:
            os.makedirs(dest_folder, exist_ok=True)
            temp_file = os.path.join(dest_folder, os.path.basename(url.split('?')[0]))
            try:
                download_file(url, temp_file)
                extract_file(temp_file, dest_folder, metadata["type"])
            except Exception as e:
                print(f"Failed to download/extract {tool_name}: {e}")
        else:
            # Handle manual downloads
            print(f"\n[!] Manual action required for: {tool_name.upper()}")
            print(f"    Category: {metadata['category']}")
            print(f"    Instructions: Please visit {metadata.get('doc_url')}")
            if metadata["type"] == "manual":
                print("    Note: This tool is proprietary or requires manual download.")
            elif metadata["type"] == "pip":
                print(f"    Note: Install via: pip install {tool_name}")
            elif metadata["type"] == "package":
                print(f"    Note: Install via your system package manager (apt/brew/etc.).")
            elif metadata["type"] == "source":
                print(f"    Note: Clone the repository and build from source.")
        
        # Populate DB
        db_manager.add_tool_config(
            tool_name=tool_name,
            path=dest_folder,
            version="latest",
            source_url=metadata.get("doc_url")
        )

    # Run Alembic upgrade
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Could not run alembic upgrade. Please ensure alembic is installed and configured.")

    print("Setup complete.")

if __name__ == "__main__":
    main()
