# tests/test_gemini_models.py
import os
from dotenv import load_dotenv

load_dotenv()

def test_gemini_models():
    """Test which Gemini models work with CrewAI"""
    from crewai import LLM
    
    models_to_test = [
        "gemini/gemma-3-27b-it",
        "gemini/gemma-3-12b-it", 
        "gemini/gemma-3-1b-it",
        "gemini/gemini-2.0-flash-exp",
    ]
    
    for model_name in models_to_test:
        try:
            print(f"Testing {model_name}...")
            llm = LLM(
                model=model_name,
                temperature=0.1,
                max_tokens=100,
                api_key=os.getenv("GEMINI_API_KEY")
            )
            
            # Test with a simple prompt
            response = llm.call("Say 'Hello' in one word.")
            print(f"✅ {model_name} works: {response}")
            
        except Exception as e:
            print(f"❌ {model_name} failed: {e}")
        
        print()

if __name__ == "__main__":
    test_gemini_models()