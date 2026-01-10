### List of All Tools, Libraries, and Dependencies So Far

Based on the project structure, code prototypes, and references in AGENT.md and AGENT_TOOL_DOCS.md (as the primary knowledge base), below is a comprehensive list of all tools, libraries, and dependencies identified to date. This is compiled from explicit mentions in the architecture, modules, and tool stacks. I've categorized them for clarity:

#### 1. **Pre-Compiled Binaries and Tools** (From `tools/` directory and AGENT_TOOL_DOCS.md)
These are standalone executables or scripts for Android internals, reverse engineering, and hardware interaction. Sourced from official hubs like Android SDK, GitHub repos, and OEM sites.
- **Core Android Tools**:
  - adb (From Android SDK Platform Tools: https://developer.android.com/tools/releases/platform-tools)
  - fastboot (From Android SDK Platform Tools)
  - aapt2 (From prebuilts/sdk/tools/)
  - aidl (From system/tools/aidl/)
  - dtc (Device Tree Compiler, from prebuilts/misc/)
  - mke2fs (From external/e2fsprogs/)
  - e2fsdroid (From system/extras/)
  - lpmake (Logical Partition Maker, from system/extras/)
  - avbtool (From external/avb/)
- **Firmware and Partition Tools**:
  - lpunpack (Super partition management)
  - payload-dumper-go (OTA extraction)
  - simg2img (Sparse image converter)
  - abootimg (Boot image manipulation)
  - binwalk (Firmware analysis)
- **Reverse Engineering and Analysis Tools**:
  - apktool.jar (APK de/recompilation, Java-based; requires JRE: https://www.java.com/en/download/manual.jsp)
  - jadx (DEX to Java decompiler)
  - dex2jar (DEX converter)
  - bytecode-viewer (Bytecode analysis)
  - androguard (Android analysis framework)
  - qark (Android vulnerability scanner)
  - mobsf (Mobile Security Framework)
  - radare2 (Reverse engineering framework)
  - frida-tools (Dynamic instrumentation)
  - uber-apk-signer (APK signing)
  - enjarify (Python to JAR converter)
  - smali (Bytecode manipulation)
- **Hardware/Protocol-Specific Tools**:
  - heimdall (Samsung Odin alternative, open-source)
  - mtk-tools (MediaTek tools)
  - qualcomm-edl (Qualcomm Emergency Download mode)
  - SP Flash Tool (MediaTek flasher: https://spflashtool.com/)
- **Root and Recovery Tools** (From AGENT_TOOL_DOCS.md):
  - Magisk (Systemless root: https://github.com/topjohnwu/Magisk)
  - TWRP (Custom recovery: https://twrp.me/)
  - OrangeFox Recovery (https://orangefox.download/)

#### 2. **Python Libraries and Dependencies** (From `requirements.txt`, code prototypes, and AGENT.md)
These are Python packages for the core framework, AI integration, UI, and HAL. Versions assume Python 3.10+.
- **Core and Utilities**:
  - sqlite3 (Built-in for DB management)
  - os, sys, json, re, subprocess (Built-in Python modules)
- **AI and Generative**:
  - google-genai (Gemini SDK for AI integration)
- **UI and CLI**:
  - rich (For modern TUI experiences)
- **Hardware and Device Interaction**:
  - adbutils (For ADB wrapper and USB detection)
  - libusb (For low-level USB/HAL; system dependency, not pip-installable)
- **Other Potential** (Inferred from AGENT.md for extensibility):
  - textual (Alternative TUI library, if rich is insufficient)

#### 3. **System-Level Dependencies** (From setup and AGENT.md)
These are runtime requirements for tools and execution.
- **Languages and Runtimes**:
  - Python 3.10+ (Core framework)
  - Bash/Shell Scripting (For build scripts)
  - OpenJDK (JDK for building AOSP/JDK 17+ for Android 13+; JRE for Java tools like apktool: https://source.android.com/docs/setup/build/requirements)
- **Build Systems** (From AGENT_TOOL_DOCS.md):
  - Repo (Git wrapper: https://source.android.com/docs/setup/create/repo)
  - Soong (.bp files)
  - Kati (Make to Ninja: https://github.com/google/kati)
  - Ninja (https://ninja-build.org/manual.html)
  - Bazel (For kernels: https://bazel.build/)
  - Clang/LLVM (Compiler: https://clang.llvm.org/docs/)
- **Development Kits**:
  - Android SDK (Platform Tools)
  - Android NDK (Native code: https://developer.android.com/ndk/downloads)
  - Android ADK (USB accessories: https://developer.android.com/guide/topics/connectivity/usb/accessory)
- **Version Control**:
  - Git (For manifests and source)

#### 4. **External Resources and Hubs** (Dependencies for Sourcing Tools/Firmware, from AGENT_TOOL_DOCS.md)
These are not local dependencies but required for dynamic fetching (e.g., via download module).
- **AOSP and Official**:
  - AOSP Source (https://source.android.com/)
  - Android Source Code Search (https://cs.android.com/android/platform/superproject)
- **Chipset-Specific**:
  - CodeLinaro (Qualcomm: https://git.codelinaro.org/)
  - Qualcomm Developer Network (https://developer.qualcomm.com/software/android)
  - Hovatek Forum (MediaTek: https://forum.hovatek.com/)
- **OEM Hubs**:
  - Samsung OSRC (https://opensource.samsung.com/)
  - Sony Open Devices (https://developer.sony.com/open-source/aosp-on-xperia-open-devices/)
  - Xiaomi MiCode (https://github.com/MiCode)
  - OnePlusOSS (https://github.com/OnePlusOSS)
  - MotorolaMobilityLLC (https://github.com/MotorolaMobilityLLC)
  - NothingOSS (https://github.com/NothingOSS)
  - ASUS (https://www.asus.com/support/Download-Center/)
  - Realme (https://github.com/realme-kernel-opensource)
  - OPPO (https://github.com/oppo-source)
  - Vivo (https://opensource.vivo.com/)
  - LG (https://opensource.lge.com/)
  - Google Pixel Drivers (https://developers.google.com/android/drivers)
- **ROM and Community**:
  - LineageOS (https://lineageos.org/)
  - crDroid (https://crdroid.net/)
  - OmniROM (http://omnirom.org/)
  - PixelExperience (https://github.com/PixelExperience)
  - ArrowOS (https://arrowos.net/)
  - XDA Developers (https://www.xda-developers.com/)
  - Awesome AOSP (https://github.com/Akipe/awesome-android-aosp)
- **Advanced Architecture**:
  - Project Treble (https://github.com/phhusson/treble_experimentations)
  - Dynamic Partitions (https://source.android.com/docs/core/ota/dynamic_partitions/implement)
  - AVB (https://android.googlesource.com/platform/external/avb/)

This list is exhaustive based on current prototypes and docs. If new modules are added, it can be extended via plugins.

### Strategy for Creating Database

As per AGENT.md directives (explicit agent config: modular design, state management via SQLite for device profiles, learned paths, and tool configurations), the database (acrd.db) is central for persistence across sessions. It ensures "Quarry First" by storing quarried device info, tailored options, and URLs, enabling AI-driven tailoring without re-quarrying. The strategy follows a scalable, normalized schema to minimize redundancy and support queries (e.g., for compatibility matching). Build on the prototype in main.py's initialize_db(), extending from using SQLite-for-on-demand-serving example.

#### 1. **Objectives and Design Principles**
- **Persistence**: Store device profiles, root methods, URLs, logs, and configs to survive restarts.
- **Normalization**: Use relational tables with foreign keys (e.g., link URLs to devices) to avoid duplication.
- **Extensibility**: Plugin-friendly—add tables for new modules (e.g., repair logs) without core changes.
- **Safety**: Include fields for checksums/verified flags; enforce transactions for high-risk ops.
- **AI Integration**: Store Gemini-generated data (e.g., tailored warnings) for reuse.
- **Performance**: Index frequently queried fields (e.g., model, compatibility); keep DB local/lightweight.
- **Initialization**: Run on setup/first launch; migrate schemas if versions change.

#### 2. **Schema Design**
Extend existing tables (device_profiles, urls_placeholders, methods). Use SQLite pragmas for integrity.
- **device_profiles** (Core table for quarried info):
  - model (TEXT PRIMARY KEY)
  - brand (TEXT)
  - os_version (TEXT)
  - firmware (TEXT)
  - security_patch (TEXT)
  - boot_mode (TEXT)  # e.g., 'normal', 'bootloader', 'download'
  - last_quarried (TIMESTAMP)  # For freshness checks
- **urls_placeholders** (Gemini-generated placeholders):
  - id (INTEGER PRIMARY KEY AUTOINCREMENT)
  - model (TEXT, FOREIGN KEY to device_profiles.model)
  - component (TEXT)  # e.g., 'recoveries', 'kernels'
  - url (TEXT)
  - type (TEXT)  # 'custom' or 'stock'
  - checksum (TEXT)  # For download verification
  - verified (BOOLEAN DEFAULT FALSE)
- **methods** (Root/exploit methods, from using SQLite-for-on-demand-serving):
  - name (TEXT PRIMARY KEY)  # e.g., 'Magisk'
  - description (TEXT)
  - pros (TEXT)
  - cons (TEXT)
  - compatibility (TEXT)  # e.g., 'Android 14+'
  - requirements (TEXT)  # JSON-like: bootloader unlock, etc.
- **New Tables for Expansion**:
  - **tool_configs** (Paths and versions for tools):
    - tool_name (TEXT PRIMARY KEY)  # e.g., 'adb'
    - path (TEXT)
    - version (TEXT)
    - source_url (TEXT)
  - **logs** (For debug/diagnostic/repair):
    - id (INTEGER PRIMARY KEY AUTOINCREMENT)
    - model (TEXT, FOREIGN KEY)
    - operation (TEXT)  # e.g., 'root', 'flash'
    - timestamp (TIMESTAMP)
    - log_data (TEXT)  # JSON or raw logcat/dmesg
    - status (TEXT)  # 'success', 'error'
  - **ai_tailored_options** (Gemini outputs for reuse):
    - id (INTEGER PRIMARY KEY AUTOINCREMENT)
    - model (TEXT, FOREIGN KEY)
    - option (TEXT)  # e.g., 'root', 'repair'
    - tailored_data (TEXT)  # JSON: subsections, warnings
- Indexes: CREATE INDEX idx_model ON device_profiles(model); etc., for fast lookups.

#### 3. **Implementation Steps**
1. **DB Module Creation**: Create `modules/db_manager.py` with functions like `init_db()`, `migrate_db()`, `insert_device_profile(info)`, `query_methods(version)`, `store_urls(model, structure)`. Import sqlite3; use context managers for connections.
2. **Initialization in setup.py**: Call `init_db()` to create tables if not exists. Populate sample data (e.g., root methods). Verify schema version in a metadata table.
3. **Integration with Quarry Flow** (in main.py/device_quarry.py):
   - After quarrying, insert/update device_profiles.
   - Feed to Gemini for dir_tree, then store in urls_placeholders via `store_urls()`.
4. **Querying Strategy**:
   - For tailoring: e.g., `SELECT * FROM methods WHERE compatibility LIKE '%{os_version}%'`
   - Use prepared statements to prevent injection.
   - Cache frequent queries in memory for performance.
5. **Backup and Migration**:
   - On updates, use PRAGMA user_version for schema tracking.
   - Backup DB before high-risk ops (e.g., repair).
6. **Error Handling**: Wrap ops in try-except; log failures. Use transactions (conn.begin()) for atomicity.
7. **Testing**: In `tests/test_db.py`, mock inserts/queries; ensure foreign key constraints.

#### 4. **Timeline and Milestones**
- **Phase 1 (Immediate)**: Implement db_manager.py with core tables; integrate into main.py prototype.
- **Phase 2**: Add new tables; test with sample quarry (e.g., mock Samsung device).
- **Phase 3**: AI-driven population—Gemini prompts include "Store in DB format: {schema}".
- **Ongoing**: Monitor size; prune old logs periodically.

This strategy aligns with AGENT.md's modular, safety-critical philosophy, using AGENT_TOOL_DOCS.md for any tool-related DB extensions (e.g., storing source URLs).
