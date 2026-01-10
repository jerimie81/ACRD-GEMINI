# scripts/prune_logs.py

import sqlite3
import time
import os
import sys

# Add project root to path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config
from modules import db_manager

def prune_old_logs(days=30):
    """Deletes logs older than the specified number of days."""
    print(f"Pruning logs older than {days} days...")
    
    with db_manager.get_db_connection() as conn:
        cursor = conn.cursor()
        
        # SQLite 'now' is in UTC. Ensure your timestamps match.
        # Assuming timestamps are stored as 'YYYY-MM-DD HH:MM:SS'
        cursor.execute(f'''
            DELETE FROM logs 
            WHERE timestamp < date('now', '-{days} days')
        ''')
        
        deleted_count = cursor.rowcount
        conn.commit()
        
        # Optional: Vacuum to reclaim space
        cursor.execute("VACUUM")
        
    print(f"Deleted {deleted_count} old log entries.")

if __name__ == "__main__":
    prune_old_logs()
