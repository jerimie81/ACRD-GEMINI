# TODO List for ACRD-GEMINI Project Completion

As the Senior Android Systems Architect & AI Integration Lead, this TODO list outlines the remaining tasks to fully implement the ACRD-GEMINI project based on proj-outline.md, AGENT.md, and AGENT_TOOL_DOCS.md (primary knowledge base for tool sourcing). Tasks are prioritized and categorized for modular development. The project adheres to "Quarry First," safety-critical execution, and plugin-based scalability. Current progress includes project structure, prototypes (main.py, device_quarry.py, dir_tree_generator.py, ai_integration.py), db_manager.py, and Alembic migrations.

Estimated timeline: 4-6 weeks for core completion, assuming 1-2 developers. Use Git for version control; track issues via README.md or a simple issue tracker.

## High-Priority Tasks (Immediate: 1-2 Weeks)
These ensure a functional prototype with core flow (quarry → dir tree → TUI).

- [ ] Integrate db_manager.py into main.py: Replace direct SQLite calls in main.py and dir_tree_generator.py with db_manager functions (e.g., insert_device_profile, store_urls).
- [ ] Expand device_quarry.py: Add full heuristics for boot modes (EDL, Download Mode, FastbootD); integrate Heimdall for Samsung; handle errors with AI-driven diagnostics (feed to Gemini via error_recovery_prompt.txt).
- [ ] Complete ai_integration.py: Add prompt optimization (e.g., context window limits); handle hallucinations with validation (e.g., check JSON validity); integrate vector embeddings for doc search if needed (from AGENT.md).
- [ ] Implement setup.py fully: 
  - Download pre-compiled tools from AGENT_TOOL_DOCS.md URLs (e.g., adb, fastboot via requests lib; heimdall from GitHub).
  - Verify dependencies (Python 3.10+, OpenJDK/JRE, libusb).
  - Populate tool_configs table in DB with sourced tools.
  - Run init_db() and Alembic upgrade.
- [ ] Create templates/ directory with prompt files:
  - dir_tree_prompt.txt: "Based on device info {info}, create dir tree with placeholders for {components}. Source URLs from {AGENT_TOOL_DOCS.md hubs}."
  - root_warning_prompt.txt: "Pull warnings for {brand} {model} rooting from brand-specific docs in {AGENT_TOOL_DOCS.md}."
  - option_tailor_prompt.txt: "Tailor {option} subsections for {device_specs} using compatibility from DB."
  - error_recovery_prompt.txt: "Analyze log {log} and suggest repair for {issue}; reference {AGENT_TOOL_DOCS.md} for tools."
- [ ] Enhance config.py: Add GEMINI_API_KEY env var handling; DB_PATH; tool paths.
- [ ] Test core flow: Mock USB detection; quarry a test device (emulator or physical); generate dir tree; verify DB storage.

## Module Implementation (2-4 Weeks)
Implement each module as per proj-outline.md, with Gemini tailoring and safety checks. Each should use HAL wrappers, DB queries, and AI for device-specific adjustments.

- [ ] hal/ wrappers:
  - adb_wrapper.py: Full ADB commands (getprop, shell, logcat, dmesg).
  - fastboot_wrapper.py: getvar, flash, boot.
  - heimdall_wrapper.py: print-pit, flash, download mode handling.
- [ ] download.py: Subsections for kernel/recovery/firmware (custom/stock); use requests to fetch from DB URLs; checksum verification (store in urls_placeholders).
- [ ] root.py: Pull warnings via Gemini; query methods from DB; execute tailored root (e.g., Magisk patch); enforce bootloader checks.
- [ ] compile.py: Subsections for ROM/kernel/app/Heimdall/Magisk; integrate tools (avbtool, lpmake); AVB signing.
- [ ] decompile.py: Subsections for firmware/kernel/APK/boot.img/super.img/payload.bin; integrate apktool, jadx, binwalk.
- [ ] diagnostic.py: AI-directed checks (boot, network); parse logs; store in logs table.
- [ ] debug.py: Log operations to DB; real-time logcat/dmesg redirection.
- [ ] repair.py: Subsections for flash/soft-brick/hard-brick/SoC/IMEI; safety checks (checksum, compatibility); AI error recovery.

## UI and User Experience (Parallel with Modules)
- [ ] Expand ui/tui.py: Use Rich for dynamic menus; main menu with options from proj-outline.md; subsections tailored via ai_tailored_options DB table; display warnings/explanations inline.

## Testing and Quality Assurance (Ongoing, 1 Week Post-Modules)
- [ ] Unit tests in tests/:
  - test_hal.py: Mock adb/fastboot outputs.
  - test_ai.py: Stub Gemini responses; validate JSON.
  - test_modules.py: End-to-end for each module.
  - test_db.py: Schema integrity, queries, migrations (add field, run Alembic).
- [ ] Integration tests: Full flow with emulator (e.g., Pixel AVD); test Samsung/MTK specifics.
- [ ] Safety testing: Simulate bricks; verify checks prevent invalid ops.
- [ ] Performance: Ensure async I/O for logs/UI updates (use asyncio if needed).

## Documentation and Polish (Final Week)
- [ ] Update README.md: Installation, usage, contribution; include setup.py instructions.
- [ ] Add LICENSE (e.g., MIT) and .gitignore.
- [ ] Optimize: Prune old logs (>30 days) via cron-like script; DB vacuum.
- [ ] Extensibility: Document adding plugins (e.g., new SoC support in hal/).
- [ ] Review against AGENT.md: Ensure HAL abstraction, AI context management, reverse pipelines.

## Dependencies and Risks
- Monitor Gemini API changes; fallback to stubs.
- Source all tools from AGENT_TOOL_DOCS.md; handle download failures.
- Legal: Emphasize warnings for rooting/flashing (voids warranty, risks bricking).

Track completion with checkboxes; assign issues if team expands. Next immediate: Integrate DB into prototypes and implement download.py. Refer to AGENT_TOOL_DOCS.md for any tool integrations.
