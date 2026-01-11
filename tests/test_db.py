# tests/test_db.py

import unittest
from modules import db_manager
from db.models import DeviceProfile, UrlPlaceholder, AiTailoredOption
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class TestDb(unittest.TestCase):

    def setUp(self):
        # Use an in-memory SQLite database for testing
        self.engine = create_engine('sqlite:///:memory:')
        db_manager.engine = self.engine
        db_manager.Session = sessionmaker(bind=self.engine)
        db_manager.init_db()

    def test_insert_device_profile(self):
        device_info = {
            'model': 'Pixel 6',
            'brand': 'Google',
            'os_version': '14',
        }
        db_manager.insert_device_profile(device_info)
        
        with db_manager.get_session() as session:
            device = session.query(DeviceProfile).filter_by(model='Pixel 6').first()
            self.assertIsNotNone(device)
            self.assertEqual(device.brand, 'Google')

    def test_store_urls(self):
        # First, add a device profile to satisfy the foreign key constraint
        db_manager.insert_device_profile({'model': 'Pixel_6', 'brand': 'Google'})
        
        structure = {
            "recoveries": {"custom": "http://example.com/twrp.img"}
        }
        db_manager.store_urls("Pixel_6", structure)
        url_info = db_manager.get_url("Pixel_6", "recoveries", "custom")
        self.assertIsNotNone(url_info)
        self.assertEqual(url_info['url'], "http://example.com/twrp.img")

    def test_set_url_verified(self):
        db_manager.insert_device_profile({'model': 'Pixel_6', 'brand': 'Google'})
        db_manager.store_urls("Pixel_6", {"recoveries": {"custom": "http://example.com/twrp.img"}})
        
        db_manager.set_url_verified("Pixel_6", "recoveries", "custom", True)
        
        url_info = db_manager.get_url("Pixel_6", "recoveries", "custom")
        self.assertTrue(url_info['verified'])


    def test_store_tailored_options(self):
        db_manager.insert_device_profile({'model': 'Pixel_6', 'brand': 'Google'})
        db_manager.store_tailored_options("Pixel_6", "Root", '{"Magisk": "OK"}')

        with db_manager.get_session() as session:
            option = session.query(AiTailoredOption).filter_by(model='Pixel_6').first()
            self.assertIsNotNone(option)
            self.assertEqual(option.tailored_data, '{"Magisk": "OK"}')

if __name__ == '__main__':
    unittest.main()