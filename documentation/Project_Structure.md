# ACRD-GEMINI Project Structure

As the Senior Android Systems Architect & AI Integration Lead, I am architecting the ACRD-GEMINI project based on the core directives in proj-outline.md. This structure adheres to the "Quarry First" philosophy: always interrogate hardware to establish truth, then dynamically generate environments. The design is modular, scalable, and plugin-based, with SQLite for persistent state management (e.g., device profiles, root methods). Python 3.x serves as the core framework, integrating Google Gemini via the google-generativeai SDK for AI-driven decisions (e.g., dir tree creation, tool tailoring).

The project emphasizes safety-critical execution: all high-risk operations (e.g., rooting, flashing) include checksum verification, compatibility checks, and AI-explained warnings pulled from device-specific documentation (sourced via AGENT_TOOL_DOCS.md as the primary knowledge base). UI is text-based (TUI) using the Rich library for modern CLI experiences.

## High-Level Architecture Overview

- **Entry Point:** `main.py` handles USB connection detection, initiates device quarry, and launches the TUI.
- **State Management:** SQLite DB (`acrd.db`) stores device profiles (e.g., OS, firmware, model), root methods (as per using SQLite-for-on-demand-serving example), learned URLs, and tool configs.
- **AI Integration:** Gemini is invoked for context-aware tasks (e.g., generating dir trees, tailoring options) with optimized prompts from `templates/`.
- **Hardware Abstraction Layer (HAL):** Wrappers in `modules/hal/` for adb, fastboot, heimdall, etc., ensuring protocol-agnostic device interaction.
- **Modular Plugins:** Each option from proj-outline.md (download, root, etc.) is a discrete module, extensible for new tools/exploits.
- **Tool Orchestration:** Pre-compiled binaries in `tools/` are wrapped via standardized Python interfaces.
- **Error Handling:** AI-driven diagnostics parse logs (logcat, dmesg) for automated repair suggestions.

## Directory Tree Structure

Below is the proposed directory structure for ACRD-GEMINI. It expands on the base from AGENT.md, incorporating proj-outline.md's options as modules. Dynamic device-specific dirs (e.g., for a queried Samsung Galaxy S10) are generated at runtime under `devices/<model>/` by Gemini based on quarried info.

```
ACRD-GEMINI/
├── README.md                  # Project overview, setup instructions, and usage guide
├── requirements.txt           # Python dependencies (e.g., google-generativeai, sqlite3, rich, adbutils)
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

## Implementation Notes

- **Setup Process:** Run `python setup.py` to:
  - Initialize SQLite DB (extend using SQLite-for-on-demand-serving: add tables for device_profiles, urls_placeholders).
  - Download/fetch pre-compiled tools from AGENT_TOOL_DOCS.md URLs (e.g., adb from developer.android.com/tools/releases/platform-tools).
  - Verify dependencies (Python 3.10+, OpenJDK for Java tools, libusb for HAL).

- **Device Quarry Flow:**
  1. Detect USB connection (using adbutils or libusb).
  2. Quarry via HAL wrappers: `adb getprop ro.build.version.release` for OS, `fastboot getvar all` for model/firmware.
  3. Feed info to Gemini via `ai_integration.py` to generate `devices/<model>/` tree with URL placeholders (sourced from AGENT_TOOL_DOCS.md hubs like opensource.samsung.com).

- **TUI Menu (ui/tui.py):**
  - Dynamic options tailored by Gemini: e.g., for a Samsung device, show Heimdall-specific repair; hide incompatible root methods.
  - Structure per proj-outline.md: Main menu -> Subsections (e.g., #download -> kernel/recovery/firmware).
  - Warnings: Always display before root/repair, generated by Gemini from brand docs (e.g., query AGENT_TOOL_DOCS.md for Samsung OSRC).

- **AI-Driven Tailoring:**
  - For each option, Gemini receives quarried info + prompt from templates/ to adjust (e.g., "For Android 14 device, recommend Magisk over KingRoot").
  - Error Recovery: In repair/debug, parse logs and chain to Gemini for suggestions (e.g., bootloop -> suggest AVB disable).

- **Safety & Transparency:**
  - Enforce checks: e.g., MD5/SHA256 verification on downloads; compatibility match against DB.
  - Explain steps: TUI outputs AI rationale (e.g., "Recommending Magisk because compatibility: Android 14+").

This structure is scalable---add new modules (e.g., for MTK support) as plugins. Next steps: Implement `main.py` and `device_quarry.py` prototypes, then integrate Gemini for proof-of-concept dir tree generation. Refer to AGENT_TOOL_DOCS.md for all tool sourcing/integration details.