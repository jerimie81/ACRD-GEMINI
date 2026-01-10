# modules/ai_integration.py

from google import genai
import json
import time
import random
from .exceptions import AIError

# Global client instance
_client = None

def initialize_gemini(api_key):
    """Initialize Gemini client."""
    global _client
    if not api_key or api_key == 'your_api_key_here':
        print("Warning: GEMINI_API_KEY is not set. AI features will be limited.")
        return False
    try:
        _client = genai.Client(api_key=api_key)
    except Exception as e:
        raise AIError(f"Failed to configure Gemini: {e}")
    return True

def gemini_generate_content(prompt, max_length=4096, retries=3):
    """
    Generate content using Gemini with prompt optimization, hallucination handling, and retries.
    """
    global _client
    if not _client:
        raise AIError("Gemini client not initialized. Please call initialize_gemini first.")

    # Truncate the prompt to avoid exceeding token limits (basic optimization)
    optimized_prompt = prompt[:max_length]

    for attempt in range(retries):
        try:
            response = _client.models.generate_content(
                model="gemini-2.0-flash",
                contents=optimized_prompt
            )
            
            if not response or not response.text:
                raise AIError("No response from AI.")

            text = response.text.strip()
            
            # Hallucination handling: Clean up potential Markdown code blocks
            if text.startswith("```"):
                lines = text.splitlines()
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                text = "\n".join(lines).strip()

            # Validation: Attempt to parse as JSON if it looks like JSON
            if (text.startswith("{") and text.endswith("}")) or (text.startswith("[") and text.endswith("]")):
                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    pass
            
            return text
        except Exception as e:
            if attempt < retries - 1:
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                print(f"AI Generation error: {e}. Retrying in {wait_time:.2f}s...")
                time.sleep(wait_time)
            else:
                raise AIError(f"AI Generation error after {retries} attempts: {str(e)}")

def get_embedding(text):
    """
    Get vector embeddings for a given text.
    """
    global _client
    if not _client:
        raise AIError("Gemini client not initialized. Please call initialize_gemini first.")
        
    try:
        response = _client.models.embed_content(
            model="text-embedding-004",
            contents=text
        )
        return response.embeddings[0].values
    except Exception as e:
        raise AIError(f"Failed to get embedding: {e}")
