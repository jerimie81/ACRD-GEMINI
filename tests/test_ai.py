# tests/test_ai.py

import unittest
from unittest.mock import patch, MagicMock
from modules import ai_integration

class TestAi(unittest.TestCase):
    
    @patch('config.GEMINI_API_KEY', 'test_key')
    @patch('google.genai.Client')
    def test_gemini_generate_content(self, mock_client_cls):
        # Setup mock client and response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = '{"key": "value"}'
        mock_client.models.generate_content.return_value = mock_response
        mock_client_cls.return_value = mock_client

        # Initialize
        ai_integration.initialize_gemini('test_key')
        
        # Test
        response = ai_integration.gemini_generate_content("test prompt")
        self.assertEqual(response, {"key": "value"})

    @patch('config.GEMINI_API_KEY', 'your_api_key_here')
    def test_gemini_no_key(self):
        # Reset client
        ai_integration._client = None
        # Initialize with invalid key (simulated by initialize_gemini logic)
        ai_integration.initialize_gemini('your_api_key_here')
        
        # Expect error because client wasn't initialized
        with self.assertRaises(Exception) as cm:
             ai_integration.gemini_generate_content("test prompt")
        self.assertIn("Gemini client not initialized", str(cm.exception))

if __name__ == '__main__':
    unittest.main()
