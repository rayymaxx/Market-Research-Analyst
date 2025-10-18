# src/marketresearch/config/gemini_config.py
import os
import time
from typing import Dict, Any, List
import google.generativeai as genai
from langchain_core.language_models import BaseLLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.outputs import LLMResult
from pydantic import Field

class GeminiModelManager:
    def __init__(self):
        self.models = {
            "gemini_fast": "gemini-2.0-flash-001",      # For speed
            "gemini_creative": "gemini-2.0-flash-001",        # For creativity  
            "gemini_precise": "gemini-2.0-flash-001",       # For precision
        }
        
        # Configure Gemini with API key
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)
    
    def get_model_for_task(self, task_type: str) -> str:
        """Determine which Gemini model to use based on task type"""
        model_mapping = {
            # Creative tasks - use creative model
            "executive_summary": "gemini_creative",
            "research_report": "gemini_creative",
            "strategic_recommendations": "gemini_creative",
            
            # Analytical tasks - use precise model
            "swot_analysis": "gemini_precise",
            "competitive_benchmarking": "gemini_precise", 
            "industry_analysis": "gemini_precise",
            "company_research": "gemini_precise",
            
            # Fast processing tasks - use fast model
            "data_collection": "gemini_fast",
            "market_trends": "gemini_fast",
        }
        return model_mapping.get(task_type, "gemini_fast")
    
    def get_fallback_model(self, current_model: str) -> str:
        """Get fallback model if current fails"""
        fallback_chain = {
            "gemini_creative": "gemini_precise",
            "gemini_precise": "gemini_fast", 
            "gemini_fast": "gemini_creative"  # Loop back
        }
        return fallback_chain.get(current_model, "gemini_fast")

class GeminiLLM(BaseLLM):
    """Gemini LLM wrapper with retry and fallback logic"""
    
    # Pydantic fields
    model_manager: GeminiModelManager = Field(exclude=True)  # exclude from serialization
    task_type: str
    primary_model: str
    
    def __init__(self, model_manager: GeminiModelManager, task_type: str):
        # Initialize with Pydantic model data
        super().__init__(
            model_manager=model_manager,
            task_type=task_type,
            primary_model=model_manager.get_model_for_task(task_type)
        )
        
    def _call_with_retry(self, prompt: str, model_name: str, **kwargs) -> str:
        """Make API call with retry logic"""
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                model = genai.GenerativeModel(self.model_manager.models[model_name])
                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=kwargs.get('temperature', 0.7),
                        top_p=kwargs.get('top_p', 0.8),
                        max_output_tokens=kwargs.get('max_tokens', 2048),
                    )
                )
                return response.text
                
            except Exception as e:
                print(f"Attempt {attempt + 1} failed for {model_name}: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (attempt + 1))
                else:
                    raise e
        
        return f"Error: All retries failed for {model_name}"
    
    def _call(self, prompt: str, stop: List[str] = None, run_manager: CallbackManagerForLLMRun = None, **kwargs: Any) -> str:
        """Main call method with fallback logic"""
        current_model = self.primary_model
        attempted_models = set()
        
        while current_model not in attempted_models:
            attempted_models.add(current_model)
            
            try:
                result = self._call_with_retry(prompt, current_model, **kwargs)
                if not result.startswith("Error:"):
                    return result
                    
            except Exception as e:
                print(f"Model {current_model} failed: {str(e)}")
            
            # Try fallback model
            current_model = self.model_manager.get_fallback_model(current_model)
            print(f"Falling back to {current_model}")
        
        # All models failed
        error_msg = f"All Gemini models failed for task {self.task_type}"
        print(f"❌ {error_msg}")
        return f"Error: {error_msg}"
    
    @property
    def _llm_type(self) -> str:
        return f"gemini_multi_{self.task_type}"
    
    def _generate(self, prompts: List[str], stop: List[str] = None, run_manager: CallbackManagerForLLMRun = None, **kwargs: Any) -> LLMResult:
        """Generate for multiple prompts"""
        generations = []
        for prompt in prompts:
            text = self._call(prompt, stop=stop, run_manager=run_manager, **kwargs)
            generations.append([{"generation_info": {}, "text": text}])
        return LLMResult(generations=generations)