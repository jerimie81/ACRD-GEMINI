# ACRD-GEMINI Directory Tree

```
ACRD-GEMINI/
├── README.md                  # Project overview, setup instructions, and usage guide
├── requirements.txt           # Python dependencies (e.g., google-genai, sqlite3, rich, adbutils)
├── setup.py                   # Script to initialize DB, download pre-compiled tools, and configure environment
├── main.py                    # Core entry point: detects USB, quarries device, generates dir tree via Gemini, launches TUI
├── config.py                  # Global configs: API keys (Gemini), DB path, tool paths from AGENT_TOOL_DOCS.md
├── db/
│   └── acrd.db                # SQLite DB for device profiles, root methods, URLs (initialized via init_root_methods_db-like functions)
├── modules/                   # Discrete logic blocks per proj-outline.md options
│   ├── hal/                   # Hardware Abstraction Layer for protocol wrapping
│   │   ├── adb_wrapper.py     # ADB interactions (e.g., getprop, shell)
│   │   ├── fastboot_wrapper.py# Fastboot commands (e.g., getvar all)
│   │   ├── heimdall_wrapper.py# Samsung-specific (e.g., download pit)
│   │   └── device_quarry.py   # Core reconnaissance: extracts OS, firmware, security patch, brand, model; heuristic for boot modes
│   ├── ai_integration.py      # Gemini SDK wrapper: prompt engineering for dir tree, option tailoring, warnings
│   ├── dir_tree_generator.py  # Uses Gemini to create device-specific dir tree with URL placeholders (recoveries, kernels, firmware)
│   ├── download.py            # Subsections: kernel (custom/stock), recovery (custom/stock), firmware (custom/stock, compile/decompile)
│   ├── root.py                # Warnings from brand docs (via AGENT_TOOL_DOCS.md), tailored methods (e.g., Magisk for Android 14+)
│   ├── compile.py             # Subsections: ROM, kernel, app, heimdall packages, Magisk modules; AVB signing
│   ├── decompile.py           # Subsections: firmware, kernel, APK, boot.img, super.img, payload.bin; tools like apktool, binwalk
│   ├── diagnostic.py          # AI-directed checks: systems, boot, network; parses logs for issues
│   ├── debug.py               # Logging for operations (e.g., logcat redirection, dmesg analysis)
│   └── repair.py              # Subsections: flash, soft/hard brick recovery, SoC flash, IMEI repair; safety checks enforced
├── tools/                     # Pre-compiled binary assets (managed via setup.py; sourced from AGENT_TOOL_DOCS.md)
│   ├── adb                    # From Android SDK Platform Tools
│   ├── fastboot               # From Android SDK Platform Tools
│   ├── heimdall               # Open-source Samsung flasher
│   ├── apktool.jar            # APK de/recompilation (Java-based, requires JRE)
│   ├── jadx                   # DEX to Java decompiler
│   ├── lpunpack               # Super partition management
│   ├── payload-dumper-go      # OTA extraction
│   ├── avbtool.py             # Android Verified Boot signing
│   ├── frida-tools            # Dynamic instrumentation
│   ├── radare2                # Reverse engineering binary
│   └── ...                    # Additional from AGENT_TOOL_DOCS.md (e.g., simg2img, abootimg, mke2fs)
├── templates/                 # AI prompt templates and personas
│   ├── dir_tree_prompt.txt    # Template for Gemini: "Based on device info {info}, create dir tree with placeholders for {components}"
│   ├── root_warning_prompt.txt# "Pull warnings for {brand} {model} rooting from docs"
│   ├── option_tailor_prompt.txt# "Tailor {option} subsections for {device_specs}"
│   └── error_recovery_prompt.txt# "Analyze log {log} and suggest repair for {issue}"
├── ui/                        # Text-based UI components
│   └── tui.py                 # Rich-based TUI: menu for options (download, root, etc.), dynamic based on device quarry
├── devices/                   # Runtime-generated device-specific dirs (created by dir_tree_generator.py)
│   └── <model>/               # e.g., SM-G973F/ (Samsung S10)
│       ├── recoveries/        # Placeholders/URLs for custom/stock (e.g., TWRP)
│       ├── kernels/           # Custom/stock URLs
│       ├── firmware/          # Custom/stock URLs
│       └── logs/              # Device-specific logs from debug/diagnostic
└── tests/                     # Unit/integration tests (e.g., mock device quarry, Gemini stubs)
    ├── test_hal.py
    ├── test_ai.py
    └── test_modules.py
```
