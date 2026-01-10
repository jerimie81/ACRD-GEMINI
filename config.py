# config.py

import os
import sys

# Gemini API Key
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'your_api_key_here')

# Database Path
DB_PATH = 'db/acrd.db'

# Tool Paths
ADB_PATH = 'tools/adb/platform-tools/adb'
FASTBOOT_PATH = 'tools/fastboot/platform-tools/fastboot'
HEIMDALL_PATH = 'tools/heimdall/heimdall'
PAYLOAD_DUMPER_GO_PATH = 'tools/payload-dumper-go/payload-dumper-go'
LPUNPACK_PATH = 'tools/lpunpack/lpunpack'
APKTOOL_PATH = 'tools/apktool/apktool_2.9.3.jar'
JADX_PATH = 'tools/jadx/bin/jadx'
AVBTOOL_PATH = 'tools/avbtool/avbtool.py'
ABOOTIMG_PATH = 'tools/abootimg/abootimg'
LPMAKE_PATH = 'tools/lpmake/lpmake'

def validate_config():
    """Validates the configuration."""
    errors = []
    
    if GEMINI_API_KEY == 'your_api_key_here':
        errors.append("GEMINI_API_KEY is not set. Please set the environment variable.")
        
    # Check if critical tools exist (warn only, as setup.py handles downloads)
    # We don't want to crash if a tool is missing, but we should warn.
    # However, for critical paths like DB, we might want to ensure the directory exists.
    
    db_dir = os.path.dirname(DB_PATH)
    if not os.path.exists(db_dir):
        try:
            os.makedirs(db_dir)
        except OSError as e:
            errors.append(f"Could not create database directory {db_dir}: {e}")

    if errors:
        print("Configuration Errors:")
        for error in errors:
            print(f"  - {error}")
        return False
    return True
