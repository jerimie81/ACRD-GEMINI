# tests/test_db.py

import unittest
from modules import db_manager

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
        
        with db_manager.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT brand FROM device_profiles WHERE model = 'Pixel 6'")
            result = cursor.fetchone()
            self.assertEqual(result[0], 'Google')

    def test_store_urls(self):
        structure = {
            "recoveries": {"custom": "http://example.com/twrp.img"}
        }
        db_manager.store_urls("Pixel_6", structure)
        url_info = db_manager.get_url("Pixel_6", "recoveries", "custom")
        self.assertEqual(url_info['url'], "http://example.com/twrp.img")

    def test_set_url_verified(self):
        structure = {
            "recoveries": {"custom": "http://example.com/twrp.img"}
        }
        db_manager.store_urls("Pixel_6", structure)
        db_manager.set_url_verified("Pixel_6", "recoveries", "custom", True)
        
        with db_manager.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT verified FROM urls_placeholders WHERE model = 'Pixel_6'")
            result = cursor.fetchone()
            self.assertEqual(result[0], 1)

    def test_store_tailored_options(self):
        db_manager.store_tailored_options("Pixel_6", "Root", '{"Magisk": "OK"}')
        with db_manager.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT tailored_data FROM ai_tailored_options WHERE model = 'Pixel_6'")
            result = cursor.fetchone()
            self.assertEqual(result[0], '{"Magisk": "OK"}')

if __name__ == '__main__':
    unittest.main()
