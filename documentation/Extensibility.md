# Extensibility and Plugin System for ACRD-GEMINI

ACRD-GEMINI is designed to be extensible. You can add support for new SoCs, brands, or tools by following these steps.

## Adding a New HAL Wrapper
To add support for a new communication protocol or tool (e.g., a proprietary flash tool for a new SoC):

1. Create a new file in `modules/hal/` (e.g., `newtool_wrapper.py`).
2. Implement functions for detection, information gathering, and flashing/operations.
3. Update `config.py` with the path to the new tool's executable.
4. Integrate the new wrapper into `modules/device_quarry.py` to allow device detection.
5. Integrate it into relevant modules like `modules/repair.py` or `modules/root.py`.

## Adding New Root Methods
Root methods are stored in the `methods` table in the database.

1. Add a new entry to the `methods` table using `db_manager.py` or a migration script.
2. Update `modules/root.py` in the `execute_root_method` function to handle the logic for the new method.

## Customizing AI Prompts
Prompt templates are stored in the `templates/` directory. You can modify these files to adjust how Gemini generates content for:
- Directory tree generation (`dir_tree_prompt.txt`)
- Rooting warnings (`root_warning_prompt.txt`)
- Error recovery suggestions (`error_recovery_prompt.txt`)
- Tailored options (`option_tailor_prompt.txt`)
