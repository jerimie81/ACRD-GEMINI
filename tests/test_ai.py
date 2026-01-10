# tests/test_ai.py

import unittest
from unittest.mock import patch
from modules import ai_integration

class TestAi(unittest.TestCase):

    @patch('google.generativeai.GenerativeModel.generate_content')
    def test_gemini_generate_content(self, mock_generate_content):
        mock_generate_content.return_value.text = '{"key": "value"}'
        response = ai_integration.gemini_generate_content("test prompt")
        self.assertEqual(response, {"key": "value"})

if __name__ == '__main__':
    unittest.main()
