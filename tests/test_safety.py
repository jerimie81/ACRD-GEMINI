# tests/test_safety.py

import unittest
from unittest.mock import patch, MagicMock
from modules import download

class TestSafety(unittest.TestCase):

    @patch('modules.download.download_file')
    @patch('modules.download.verify_checksum')
    @patch('modules.db_manager.get_url')
    def test_checksum_verification_failure(self, mock_get_url, mock_verify, mock_download):
        # Setup
        mock_get_url.return_value = {'url': 'http://test.com/file.zip', 'checksum': 'valid_checksum'}
        mock_download.return_value = True
        mock_verify.return_value = False # Simulate checksum failure
        
        # Capture stdout to verify error message
        with patch('builtins.print') as mock_print:
            download.download_component('TestModel', 'recovery', 'custom')
            
            # Verify that the checksum failure message was printed
            mock_print.assert_any_call("Checksum verification failed!")

if __name__ == '__main__':
    unittest.main()
