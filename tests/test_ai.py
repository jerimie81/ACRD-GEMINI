# tests/test_ai.py

import unittest
from unittest.mock import patch
from modules import ai_integration

class TestAi(unittest.TestCase):
    
    @patch('config.GEMINI_API_KEY', 'test_key')
    @patch('google.generativeai.GenerativeModel.generate_content')
    def test_gemini_generate_content(self, mock_generate_content):
        mock_generate_content.return_value.text = '{"key": "value"}'
        response = ai_integration.gemini_generate_content("test prompt")
        self.assertEqual(response, {"key": "value"})

    @patch('config.GEMINI_API_KEY', 'your_api_key_here')
    def test_gemini_no_key(self):
        response = ai_integration.gemini_generate_content("test prompt")
        self.assertEqual(response, "AI response unavailable (API key not set).")

if __name__ == '__main__':
    unittest.main()
