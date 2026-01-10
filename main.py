# main.py

import os
import sys
import sqlite3
from modules.hal.device_quarry import quarry_device
from modules.dir_tree_generator import generate_dir_tree
from modules.ai_integration import initialize_gemini
from ui.tui import launch_tui
import config

def initialize_db():
    """Initialize SQLite DB if not exists."""
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    # Create tables as per project needs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS device_profiles (
            model TEXT PRIMARY KEY,
            brand TEXT,
            os_version TEXT,
            firmware TEXT,
            security_patch TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls_placeholders (
            model TEXT,
            component TEXT,
            url TEXT,
            type TEXT,  -- custom or stock
            FOREIGN KEY (model) REFERENCES device_profiles(model)
        )
    ''')
    # Extend with root methods as in using SQLite-for-on-demand-serving
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS methods (
            name TEXT PRIMARY KEY,
            description TEXT,
            pros TEXT,
            cons TEXT,
            compatibility TEXT
        )
    ''')
    # Insert sample root method
    cursor.execute('''
        INSERT OR REPLACE INTO methods VALUES
        ('Magisk', 'Systemless root via boot patching', 'Stable, modules', 'Bootloader unlock needed', 'Android 14+')
    ''')
    conn.commit()
    conn.close()

def detect_usb_connection():
    """Prototype for USB detection; in full impl, use libusb or adbutils.wait_for_device()."""
    # For POC, assume connection and prompt user
    print("Connect device via USB and press Enter to continue...")
    input()
    return True

def main():
    # Setup environment
    initialize_db()
    initialize_gemini()  # Sets up Gemini client

    # Detect USB
    if not detect_usb_connection():
        print("No device detected. Exiting.")
        sys.exit(1)

    # Quarry device
    device_info = quarry_device()
    if not device_info:
        print("Failed to quarry device info. Exiting.")
        sys.exit(1)

    # Store device profile in DB
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO device_profiles (model, brand, os_version, firmware, security_patch)
        VALUES (?, ?, ?, ?, ?)
    ''', (device_info['model'], device_info['brand'], device_info['os_version'],
          device_info['firmware'], device_info['security_patch']))
    conn.commit()
    conn.close()

    # Generate dir tree via Gemini
    dir_path = generate_dir_tree(device_info)
    print(f"Device-specific dir tree generated at: {dir_path}")

    # Launch TUI with device info
    launch_tui(device_info)

if __name__ == "__main__":
    main()
