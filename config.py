# config.py

import os

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
