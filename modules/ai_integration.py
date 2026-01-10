# modules/ai_integration.py

import google.generativeai as genai
import config
import json

def initialize_gemini():
    """Initialize Gemini client."""
    genai.configure(api_key=config.GEMINI_API_KEY)

def gemini_generate_content(prompt, max_length=2048):
    """
    Generate content using Gemini with prompt optimization and hallucination handling.
    """
    # Truncate the prompt to avoid exceeding token limits
    optimized_prompt = prompt[:max_length]

    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(optimized_prompt)

    try:
        # Attempt to parse the response as JSON, a common source of hallucinations
        # Some responses might be wrapped in ```json ... ```
        text = response.text.strip()
        if text.startswith("```json") and text.endswith("```"):
            text = text[7:-3].strip()
        elif text.startswith("```") and text.endswith("```"):
            text = text[3:-3].strip()
            
        return json.loads(text)
    except (json.JSONDecodeError, TypeError, AttributeError):
        # If it's not valid JSON, return the raw text
        return response.text

def get_embedding(text):
    """
    Get vector embeddings for a given text.
    """
    return genai.embed_content(model="models/embedding-001",
                                content=text,
                                task_type="retrieval_document")["embedding"]
