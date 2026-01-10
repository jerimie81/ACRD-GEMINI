# modules/db_manager.py

import sqlite3
from contextlib import contextmanager
import config  # Assuming config.DB_PATH is defined

@contextmanager
def get_db_connection():
    """Context manager for DB connections with transaction support."""
    conn = sqlite3.connect(config.DB_PATH)
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Initialize the database with expanded schema."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # device_profiles
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS device_profiles (
                model TEXT PRIMARY KEY,
                brand TEXT NOT NULL,
                os_version TEXT,
                firmware TEXT,
                security_patch TEXT,
                boot_mode TEXT,
                last_quarried TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_model ON device_profiles(model)')
        
        # urls_placeholders
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS urls_placeholders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model TEXT NOT NULL,
                component TEXT NOT NULL,
                url TEXT,
                type TEXT,
                checksum TEXT,
                verified BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (model) REFERENCES device_profiles(model) ON DELETE CASCADE
            )
        ''')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_urls_model ON urls_placeholders(model)')
        
        # methods
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS methods (
                name TEXT PRIMARY KEY,
                description TEXT,
                pros TEXT,
                cons TEXT,
                compatibility TEXT,
                requirements TEXT
            )
        ''')
        
        # tool_configs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tool_configs (
                tool_name TEXT PRIMARY KEY,
                path TEXT,
                version TEXT,
                source_url TEXT
            )
        ''')
        
        # logs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model TEXT,
                operation TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                log_data TEXT,
                status TEXT,
                FOREIGN KEY (model) REFERENCES device_profiles(model) ON DELETE SET NULL
            )
        ''')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_logs_model ON logs(model)')
        
        # ai_tailored_options
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_tailored_options (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model TEXT NOT NULL,
                option TEXT NOT NULL,
                tailored_data TEXT,
                generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (model) REFERENCES device_profiles(model) ON DELETE CASCADE
            )
        ''')
        
        # db_metadata
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS db_metadata (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        # Set initial schema version
        cursor.execute("INSERT OR REPLACE INTO db_metadata (key, value) VALUES ('schema_version', '1')")
        
        # Sample data insertion (extend as needed)
        cursor.execute('''
            INSERT OR REPLACE INTO methods (name, description, pros, cons, compatibility, requirements)
            VALUES ('Magisk', 'Systemless root via boot patching', 'Stable, modules', 'Bootloader unlock needed', 'Android 14+', '{"bootloader_unlock": true, "tools": ["adb", "fastboot"]}')
        ''')
        
        # Example tool_configs from AGENT_TOOL_DOCS.md
        cursor.execute('''
            INSERT OR REPLACE INTO tool_configs (tool_name, path, version, source_url)
            VALUES ('adb', 'tools/adb', 'latest', 'https://developer.android.com/tools/releases/platform-tools')
        ''')
        # Add more tools similarly
        
        conn.commit()

def add_tool_config(tool_name, path, version, source_url):
    """Adds a tool configuration to the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO tool_configs (tool_name, path, version, source_url)
            VALUES (?, ?, ?, ?)
        ''', (tool_name, path, version, source_url))
        conn.commit()

def insert_device_profile(info):
    """Insert or update device profile."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO device_profiles 
            (model, brand, os_version, firmware, security_patch, boot_mode, last_quarried)
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (info.get('model'), info.get('brand'), info.get('os_version'),
              info.get('firmware'), info.get('security_patch'), info.get('boot_mode')))
        conn.commit()

def query_methods(os_version):
    """Query root methods by compatibility."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM methods WHERE compatibility LIKE ?", (f'%{os_version}%',))
        return cursor.fetchall()

def store_urls(model, structure):
    """Store URLs/placeholders for a model."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        for comp, urls in structure.items():
            for typ, url in urls.items():
                cursor.execute('''
                    INSERT OR REPLACE INTO urls_placeholders (model, component, url, type)
                    VALUES (?, ?, ?, ?)
                ''', (model, comp, url, typ))
        conn.commit()

def get_url(model, component, type):
    """Gets a URL for a specific component and type."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT url, checksum FROM urls_placeholders WHERE model = ? AND component = ? AND type = ?", (model, component, type))
        result = cursor.fetchone()
        if result:
            return {"url": result[0], "checksum": result[1]}
        return None

def log_operation(model, operation, log_data, status):
    """Log an operation."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO logs (model, operation, log_data, status)
            VALUES (?, ?, ?, ?)
        ''', (model, operation, log_data, status))
        conn.commit()

def get_schema_version():
    """Get current schema version."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM db_metadata WHERE key = 'schema_version'")
        result = cursor.fetchone()
        return int(result[0]) if result else 0

def set_url_verified(model, component, type, verified=True):
    """Updates the verified status of a URL."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE urls_placeholders 
            SET verified = ? 
            WHERE model = ? AND component = ? AND type = ?
        ''', (verified, model, component, type))
        conn.commit()

def store_tailored_options(model, option, tailored_data):
    """Stores AI-tailored options in the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO ai_tailored_options (model, option, tailored_data)
            VALUES (?, ?, ?)
        ''', (model, option, tailored_data))
        conn.commit()

# Additional functions for other tables can be added similarly
