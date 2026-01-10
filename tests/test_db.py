# tests/test_db.py

import unittest
from db import db_manager

class TestDb(unittest.TestCase):

    def setUp(self):
        # Use an in-memory database for testing
        db_manager.DB_PATH = ":memory:"
        db_manager.init_db()

    def test_insert_device_profile(self):
        device_info = {
            'model': 'Pixel 6',
            'brand': 'Google',
            'os_version': '14',
        }
        db_manager.insert_device_profile(device_info)
        # TODO: Add assertion

if __name__ == '__main__':
    unittest.main()
