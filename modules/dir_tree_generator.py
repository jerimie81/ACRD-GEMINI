# modules/dir_tree_generator.py

import os
import json
from modules.ai_integration import gemini_generate_content
from modules import db_manager

def generate_dir_tree(device_info):
    """Use Gemini to generate device-specific dir tree with placeholders.
    Prompt from templates/dir_tree_prompt.txt.
    Create actual directories under devices/<model>/
    Source URLs from AGENT_TOOL_DOCS.md hubs.
    """
    # Load prompt template
    with open('templates/dir_tree_prompt.txt', 'r') as f:
        prompt_template = f.read()

    # Fill template
    prompt = prompt_template.format(
        info=json.dumps(device_info),
        components='recoveries, kernels, firmware',
        model=device_info.get('model', 'unknown_device')
    )

    # Generate content via Gemini
    response = gemini_generate_content(prompt)

    # For POC, assume response is JSON-like dir structure
    if isinstance(response, dict):
        dir_structure = response
    else:
        try:
            dir_structure = json.loads(response)  # e.g., {"recoveries": {"custom": "url_twrp", "stock": "url_stock"}, ...}
        except (json.JSONDecodeError, TypeError):
            print("Gemini response not valid JSON. Using default structure.")
            dir_structure = {
                "recoveries": {"custom": "placeholder_twrp_url", "stock": "placeholder_stock_url"},
                "kernels": {"custom": "placeholder_custom_url", "stock": "placeholder_stock_url"},
                "firmware": {"custom": "placeholder_custom_url", "stock": "placeholder_stock_url"}
            }

    # Create dir tree
    model = device_info['model'].replace(' ', '_')  # Sanitize
    base_path = f"devices/{model}"
    os.makedirs(base_path, exist_ok=True)

    for component in ['recoveries', 'kernels', 'firmware', 'logs']:
        comp_path = os.path.join(base_path, component)
        os.makedirs(comp_path, exist_ok=True)
        # Save placeholders as JSON in dir
        with open(os.path.join(comp_path, 'placeholders.json'), 'w') as f:
            json.dump(dir_structure.get(component, {}), f)

    # Store URLs in DB
    db_manager.store_urls(device_info['model'], dir_structure)

    return base_path
