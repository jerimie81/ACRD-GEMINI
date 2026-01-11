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

    @patch('config.GEMINI_API_KEY', 'test_key')
    @patch('google.genai.Client')
    def test_gemini_generate_content_plain_text(self, mock_client_cls):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Just some plain text"
        mock_client.models.generate_content.return_value = mock_response
        mock_client_cls.return_value = mock_client
        ai_integration.initialize_gemini('test_key')
        
        response = ai_integration.gemini_generate_content("test prompt")
        self.assertEqual(response, "Just some plain text")

    @patch('config.GEMINI_API_KEY', 'test_key')
    @patch('google.genai.Client')
    def test_gemini_generate_content_error(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = Exception("API Error")
        mock_client_cls.return_value = mock_client
        ai_integration.initialize_gemini('test_key')
        
        from modules.exceptions import AIError
        with self.assertRaises(AIError):
            ai_integration.gemini_generate_content("test prompt")

if __name__ == '__main__':
    unittest.main()
