# tests/test_setup.py

import unittest
import os
import shutil
from unittest.mock import patch, MagicMock
import setup

class TestSetup(unittest.TestCase):

    def setUp(self):
        # Create a temporary tools directory
        self.test_tools_dir = "tests/temp_tools"
        os.makedirs(self.test_tools_dir, exist_ok=True)

    def tearDown(self):
        # Clean up
        if os.path.exists(self.test_tools_dir):
            shutil.rmtree(self.test_tools_dir)

    @patch('requests.get')
    def test_download_file(self, mock_get):
        # Mock the response
        mock_response = MagicMock()
        mock_response.iter_content.return_value = [b'test data']
        mock_response.status_code = 200
        mock_get.return_value.__enter__.return_value = mock_response

        url = "http://example.com/test.zip"
        dest = os.path.join(self.test_tools_dir, "test.zip")
        
        setup.download_file(url, dest)
        
        self.assertTrue(os.path.exists(dest))
        with open(dest, 'rb') as f:
            self.assertEqual(f.read(), b'test data')

    @patch('subprocess.run')
    def test_extract_zip(self, mock_run):
        # Create a dummy zip file
        zip_path = os.path.join(self.test_tools_dir, "test.zip")
        with open(zip_path, 'w') as f:
            f.write("dummy zip content")
            
        dest_folder = os.path.join(self.test_tools_dir, "extracted")
        
        setup.extract_file(zip_path, dest_folder, "zip")
        
        # Verify subprocess was called correctly
        mock_run.assert_called_with(["unzip", "-o", zip_path, "-d", dest_folder], check=True)

if __name__ == '__main__':
    unittest.main()
