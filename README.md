# ACRD-GEMINI

ACRD-GEMINI is an advanced Android Device Repair and Analysis tool integrated with Gemini AI. It provides a comprehensive suite of utilities for device diagnostics, rooting, decompilation, and firmware management, all accessible through an intuitive Text-based User Interface (TUI).

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Development and Testing](#development-and-testing)
- [Scripts](#scripts)
- [License](#license)

## Overview
ACRD-GEMINI (Android Comprehensive Repair & Diagnostics - Gemini) leverages the power of Google's Gemini AI to assist in complex Android maintenance tasks. From automated device discovery via ADB and Fastboot to tailored repair suggestions, the tool aims to be a one-stop-shop for Android power users and developers.

## Features
- **Device Quarry:** Automatic detection and information gathering from devices in ADB or Fastboot mode.
- **AI Integration:** Uses Gemini AI for optimizing prompts and generating tailored repair/diagnostic options.
- **TUI (Text-based User Interface):** A user-friendly interface powered by `rich` for navigating features.
- **Download Manager:** Download stock/custom recoveries, kernels, and firmware.
- **Rooting Utilities:** Tools and methods for rooting various Android devices.
- **Decompilation:** APK decompilation using `apktool` and `jadx`.
- **Compilation:** Kernel compilation support.
- **Diagnostics & Debugging:** Run device diagnostics and capture real-time logs (Logcat).
- **Repair:** Flash stock ROMs to recover devices.

## Project Structure
```text
ACRD-GEMINI/
├── main.py                 # Main entry point, launches TUI
├── setup.py                # Initialization and dependency setup script
├── config.py               # Configuration management (API keys, paths)
├── db/                     # Database management
│   ├── acrd.db             # SQLite database
│   ├── db_manager.py       # Database operations logic
│   └── Alembic/            # Database migration scripts
├── modules/                # Core logic modules
│   ├── ai_integration.py   # Gemini AI wrapper
│   ├── device_quarry.py    # Device detection logic
│   ├── hal/                # Hardware Abstraction Layer (ADB, Fastboot, Heimdall)
│   ├── decompile.py        # APK decompilation logic
│   ├── compile.py          # Compilation logic
│   ├── root.py             # Rooting procedures
│   └── repair.py           # Device repair and flashing
├── templates/              # AI prompt templates
├── tools/                  # External binaries (ADB, Fastboot, APKTool, etc.)
├── ui/                     # User interface components
│   └── tui.py              # Text-based User Interface implementation
├── tests/                  # Unit and integration tests
└── requirements.txt        # Python dependencies
```

## Requirements
- **Python:** 3.10 or higher.
- **Java:** OpenJDK/JRE (required for tools like Apktool/Jadx).
- **System Dependencies:** `libusb` (recommended for device communication), `unzip`.
- **Google Gemini API Key:** Required for AI-powered features.

## Setup and Installation
1.  **Clone the Repository:**
    ```bash
    git clone <repository-url>
    cd ACRD-GEMINI
    ```
2.  **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the Setup Script:**
    This script checks for system dependencies, initializes the database, and downloads necessary tools (ADB, Fastboot).
    ```bash
    python setup.py
    ```

## Usage
To start the tool, run the main script:
```bash
python main.py
```
Follow the on-screen prompts in the TUI to interact with your connected Android device.

## Configuration
The tool uses a `config.py` file and environment variables for configuration.
- **`GEMINI_API_KEY`**: Set this environment variable with your Google Gemini API key.
    ```bash
    export GEMINI_API_KEY='your_actual_api_key'
    ```
- **Database Path:** Defaults to `db/acrd.db`.
- **Tool Paths:** Paths to ADB, Fastboot, and other tools are managed in `config.py` and the database.

## Development and Testing
### Running Tests
Tests are located in the `tests/` directory. You can run them using `pytest` (if installed) or manually:
```bash
python -m unittest discover tests
```

## Scripts
- **`setup.py`**: Handles initial environment setup, dependency checks, and tool downloads.
- **`main.py`**: The primary entry point for the application.
- **`db/Alembic/integrate_into_setup.py`**: Script to integrate Alembic migration execution into the main `setup.py` flow.
- **`db/Alembic/modify_migrations-env.py`**: Helper script to adjust Alembic's `env.py` for dynamic DB path resolution.

## License
This project is licensed under the [LICENSE](LICENSE) file found in the root directory.
