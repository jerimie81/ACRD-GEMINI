# Extending ACRD-GEMINI

ACRD-GEMINI is designed to be modular and extensible. This guide explains how to add new features, support new devices, or integrate new tools.

## Adding New Modules

1.  **Create the Module:** Add a new Python file in the `modules/` directory (e.g., `modules/new_feature.py`).
2.  **Implement Logic:** Define your functions. Use `db_manager` for persistence and `ai_integration` for Gemini capabilities.
3.  **Register in TUI:** Update `ui/tui.py` to add a menu option that calls your new module's entry point.

## Adding New Tools

1.  **Update Toolset Doc:** Add the tool to `documentation/ACRD-toolset.md`.
2.  **Update Setup:** Add the tool's metadata to `TOOL_METADATA` in `setup.py` to handle automated downloading and installation.
3.  **Update Database:** The `setup.py` script automatically adds tools to the `tool_configs` table.

## Supporting New SoCs/Hardware

1.  **HAL Wrappers:** If the new hardware requires specific commands (like a new flashing protocol), create a wrapper in `modules/hal/` (e.g., `modules/hal/new_soc_wrapper.py`).
2.  **Integrate:** Import and use this wrapper in your modules (e.g., `repair.py` or `root.py`).

## Database Extensions

1.  **Schema Changes:** If you need new tables, update `modules/db_manager.py`'s `init_db` function.
2.  **Migrations:** Ideally, use Alembic to generate a migration script for existing databases.
