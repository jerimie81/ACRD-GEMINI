# modules/ai_integration.py

import google.generativeai as genai
import config
import json

def initialize_gemini():
    """Initialize Gemini client."""
    if not config.GEMINI_API_KEY or config.GEMINI_API_KEY == 'your_api_key_here':
        print("Warning: GEMINI_API_KEY is not set. AI features will be limited.")
        return False
    genai.configure(api_key=config.GEMINI_API_KEY)
    return True

def gemini_generate_content(prompt, max_length=4096):
    """
    Generate content using Gemini with prompt optimization and hallucination handling.
    """
    if not config.GEMINI_API_KEY or config.GEMINI_API_KEY == 'your_api_key_here':
        return "AI response unavailable (API key not set)."

    # Truncate the prompt to avoid exceeding token limits (basic optimization)
    optimized_prompt = prompt[:max_length]

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(optimized_prompt)
        
        if not response or not response.text:
            return "No response from AI."

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
        return f"AI Generation error: {str(e)}"

def get_embedding(text):
    """
    Get vector embeddings for a given text.
    """
    return genai.embed_content(model="models/embedding-001",
                                content=text,
                                task_type="retrieval_document")["embedding"]
