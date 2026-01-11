# tests/test_core_flow.py

import unittest
import os
import shutil
import json
from unittest.mock import patch, MagicMock
from modules import db_manager, dir_tree_generator
import config

class TestCoreFlow(unittest.TestCase):

    def setUp(self):
        # Use a test database
        config.DB_PATH = "tests/test_acrd.db"
        if os.path.exists(config.DB_PATH):
            os.remove(config.DB_PATH)
        db_manager.reset_engine()
        db_manager.init_db()
        
        # Mock device info
        self.mock_device = {
            'model': 'Test Pixel 6',
            'brand': 'Google',
            'os_version': '14',
            'firmware': 'TEST.123456.001',
            'security_patch': '2024-01-01',
            'boot_mode': 'adb'
        }
        
        # Clean up previous test artifacts
        self.device_dir = f"devices/{self.mock_device['model'].replace(' ', '_')}"
        if os.path.exists(self.device_dir):
            shutil.rmtree(self.device_dir)

    def tearDown(self):
        # Clean up DB and directories
        if os.path.exists(config.DB_PATH):
            os.remove(config.DB_PATH)
        if os.path.exists(self.device_dir):
            shutil.rmtree(self.device_dir)

    @patch('modules.device_quarry.quarry_device')
    @patch('modules.dir_tree_generator.gemini_generate_content')
    def test_quarry_to_dirtree_flow(self, mock_gemini, mock_quarry):
        # Setup mocks
        mock_quarry.return_value = self.mock_device
        
        # Mock Gemini response for dir tree structure
        mock_tree_structure = {
            "recoveries": {"custom": "https://twrp.me/test", "stock": "https://google.com/stock"},
            "kernels": {"custom": "https://github.com/test/kernel", "stock": None},
            "firmware": {"stock": "https://developers.google.com/android/images"}
        }
        mock_gemini.return_value = json.dumps(mock_tree_structure)

        # 1. Simulate Main Flow: Quarry Device
        device_info = mock_quarry()
        self.assertEqual(device_info['model'], 'Test Pixel 6')

        # 2. Store in DB
        db_manager.insert_device_profile(device_info)
        
        # Verify DB insertion
        with db_manager.get_session() as session:
            from db.models import DeviceProfile
            device = session.query(DeviceProfile).filter_by(model=device_info['model']).first()
            self.assertEqual(device.brand, 'Google')

        # 3. Generate Directory Tree
        # We need to mock the template reading since we might not want to rely on actual files
        with patch('builtins.open', create=True) as mock_open:
            # Configure mock_open to handle read for template and write for json
            # This is tricky with multiple opens, so we might just let it read the real template if it exists
            # or just mock the generate_dir_tree internal logic. 
            # For this integration test, let's allow it to try reading the real template 
            # but we need to ensure the template file exists or mock it specifically.
            
            # Simpler approach: Let's just call the function. 
            # If template is missing, we might need to create it in setUp.
            pass

        # Ensure template exists for the test
        os.makedirs('templates', exist_ok=True)
        if not os.path.exists('templates/dir_tree_prompt.txt'):
            with open('templates/dir_tree_prompt.txt', 'w') as f:
                f.write("Test template {info}")

        base_path = dir_tree_generator.generate_dir_tree(device_info)

        # 4. Verify Directory Creation
        self.assertTrue(os.path.exists(base_path))
        self.assertTrue(os.path.exists(os.path.join(base_path, 'recoveries')))
        self.assertTrue(os.path.exists(os.path.join(base_path, 'kernels')))
        
        # 5. Verify URLs stored in DB
        url_info = db_manager.get_url(device_info['model'], 'recoveries', 'custom')
        self.assertEqual(url_info['url'], "https://twrp.me/test")

if __name__ == '__main__':
    unittest.main()
