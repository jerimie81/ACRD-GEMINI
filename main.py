# main.py

import argparse
from modules import db_manager, device_quarry, dir_tree_generator, ai_integration
from ui import tui
import config

def main():
    """Main entry point for the ACRD-GEMINI tool."""
    # Initialize Gemini
    ai_integration.initialize_gemini()

    # Initialize the database
    db_manager.init_db()

    # Detect and quarry the device
    device_info = device_quarry.quarry_device()

    if device_info:
        # Store device info in the database
        db_manager.insert_device_profile(device_info)

        # Generate the device-specific directory tree
        dir_tree_generator.generate_dir_tree(device_info)

        # Launch the Text-based User Interface
        tui.launch_tui(device_info)
    else:
        print("Could not find a device. Please ensure it's connected and in ADB or Fastboot mode.")


if __name__ == '__main__':
    main()
