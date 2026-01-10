# modules/ai_integration.py

import google.generativeai as genai
import config

def initialize_gemini():
    """Initialize Gemini client."""
    genai.configure(api_key=config.GEMINI_API_KEY)

def gemini_generate_content(prompt):
    """Generate content using Gemini.
    For POC, use gemini-1.5-flash or similar.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text
