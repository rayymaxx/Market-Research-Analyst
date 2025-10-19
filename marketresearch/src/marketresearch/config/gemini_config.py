# src/marketresearch/config/gemini_config.py
import os
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import google.generativeai as genai
from langchain_core.language_models import BaseLLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.outputs import LLMResult
from pydantic import Field
from crewai import LLM

class RateLimiter:
    """Proper rate limiter with token bucket algorithm"""
    
    def __init__(self, requests_per_minute: int = 15, requests_per_day: int = 1500):
        self.requests_per_minute = requests_per_minute
        self.requests_per_day = requests_per_day
        self.minute_window = 60  # seconds
        self.day_window = 86400  # seconds
        
        # Thread-safe data structures
        self.lock = threading.Lock()
        self.minute_calls = []
        self.day_calls = []
        self.model_usage = {}  # Track usage per model
        
    def can_make_request(self, model_name: str) -> bool:
        """Check if request can be made without exceeding limits"""
        with self.lock:
            now = time.time()
            
            # Clean old entries
            self.minute_calls = [t for t in self.minute_calls if now - t < self.minute_window]
            self.day_calls = [t for t in self.day_calls if now - t < self.day_window]
            
            # Check limits
            if (len(self.minute_calls) >= self.requests_per_minute or 
                len(self.day_calls) >= self.requests_per_day):
                return False
                
            return True
    
    def record_request(self, model_name: str):
        """Record that a request was made"""
        with self.lock:
            now = time.time()
            self.minute_calls.append(now)
            self.day_calls.append(now)
            
            # Track model usage
            if model_name not in self.model_usage:
                self.model_usage[model_name] = []
            self.model_usage[model_name].append(now)
    
    def wait_if_needed(self, model_name: str):
        """Wait if rate limit would be exceeded"""
        while not self.can_make_request(model_name):
            # Calculate wait time
            now = time.time()
            if self.minute_calls:
                oldest_in_minute = min(self.minute_calls)
                time_since_oldest = now - oldest_in_minute
                if time_since_oldest < self.minute_window and len(self.minute_calls) >= self.requests_per_minute:
                    wait_time = self.minute_window - time_since_oldest + 1
                    print(f"🚫 Minute rate limit approaching. Waiting {wait_time:.1f}s...")
                    time.sleep(wait_time)
                    continue
            
            if self.day_calls:
                oldest_in_day = min(self.day_calls)
                time_since_oldest = now - oldest_in_day
                if time_since_oldest < self.day_window and len(self.day_calls) >= self.requests_per_day:
                    wait_time = self.day_window - time_since_oldest + 1
                    print(f"🚫 Daily rate limit approaching. Waiting {wait_time:.1f}s...")
                    time.sleep(wait_time)
                    continue
            
            # Small delay if we're close to limits
            time.sleep(2)

class GeminiModelManager:
    def __init__(self):
        # More reasonable limits
        self.rate_limiter = RateLimiter(
            requests_per_minute=10,   # 10 per minute
            requests_per_day=100      # 100 per day
        )
        
        # Use models with better rate limits
        self.models = {
            "gemini_fast": "gemini-2.0-flash-001",
            "gemini_creative": "gemini-2.0-flash-exp", 
            "gemini_precise": "gemini-2.0-flash-001",
            "gemini_fallback": "gemma-3-12b-it",
        }
        
        # Configure Gemini with API key
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)
        
        # Model-specific rate limits (requests per minute)
        self.model_limits = {
            "gemini_fast": 15,
            "gemini_creative": 15,
            "gemini_precise": 10,
            "gemini_fallback": 10,
        }
    
    def get_model_for_task(self, task_type: str) -> str:
        """Determine which Gemini model to use based on task type"""
        model_mapping = {
            "executive_summary": "gemini_creative",
            "research_report": "gemini_fast",
            "strategic_recommendations": "gemini_creative",
            "swot_analysis": "gemini_precise",
            "competitive_benchmarking": "gemini_fast",  # Changed from fallback
            "industry_analysis": "gemini_fast",
            "company_research": "gemini_creative",
            "data_collection": "gemini_fast",
            "market_trends": "gemini_fallback",  # Changed from fallback
        }
        return model_mapping.get(task_type, "gemini_fast")
    
    def get_fallback_chain(self, current_model: str) -> List[str]:
        """Get ordered fallback chain"""
        fallback_chains = {
            "gemini_creative": ["gemini_fast", "gemini_precise", "gemini_fallback"],
            "gemini_fast": ["gemini_precise", "gemini_fallback"],
            "gemini_precise": ["gemini_fast", "gemini_fallback"],
            "gemini_fallback": ["gemini_fast"]  # No further fallbacks
        }
        return fallback_chains.get(current_model, ["gemini_fallback"])

class GeminiLLM(BaseLLM):
    """Gemini LLM wrapper with proper rate limiting"""
    
    task_type: str
    primary_model: str
    
    def __init__(self, model_manager, task_type: str):
        # Store model manager without Pydantic validation using object.__setattr__
        object.__setattr__(self, 'model_manager', model_manager)
        super().__init__(
            task_type=task_type,
            primary_model=model_manager.get_model_for_task(task_type)
        )
        
    def _call_with_retry(self, prompt: str, model_name: str, **kwargs) -> str:
        """Make API call with proper rate limiting and retry logic"""
        max_retries = 2  # Reduced retries
        base_delay = 10  # Start with 10 seconds
        
        for attempt in range(max_retries):
            try:
                # Wait for rate limit clearance
                self.model_manager.rate_limiter.wait_if_needed(model_name)
                
                # Add increasing delay between retries
                if attempt > 0:
                    wait_time = base_delay * (2 ** attempt)  # Exponential backoff
                    print(f"⏳ Retry {attempt + 1}/{max_retries}. Waiting {wait_time}s...")
                    time.sleep(wait_time)
                
                # Record the request
                self.model_manager.rate_limiter.record_request(model_name)
                
                model = genai.GenerativeModel(self.model_manager.models[model_name])
                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=kwargs.get('temperature', 0.7),
                        top_p=kwargs.get('top_p', 0.8),
                        max_output_tokens=kwargs.get('max_tokens', 8192),  # Increased for comprehensive reports
                    )
                )
                
                # Shorter delay after successful call
                time.sleep(2)  # Reduced to 2 seconds
                return response.text
                
            except Exception as e:
                error_str = str(e)
                print(f"Attempt {attempt + 1} failed for {model_name}: {error_str}")
                
                # Check for rate limit errors
                if any(keyword in error_str.lower() for keyword in ["429", "quota", "rate", "resource exhausted"]):
                    if attempt < max_retries - 1:
                        # Longer wait for rate limits
                        wait_time = 30 * (attempt + 1)
                        print(f"🚫 Rate limit hit. Waiting {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                    else:
                        # Final attempt failed due to rate limit
                        return f"RATE_LIMIT_ERROR:{model_name}"
                
                # For other errors, continue to next retry
                if attempt < max_retries - 1:
                    continue
                else:
                    return f"ERROR:{str(e)}"
        
        return f"ERROR:All retries failed for {model_name}"
    
    def _call(self, prompt: str, stop: List[str] = None, run_manager: CallbackManagerForLLMRun = None, **kwargs: Any) -> str:
        """Main call method with proper fallback chain"""
        current_models = [self.primary_model] + self.model_manager.get_fallback_chain(self.primary_model)
        
        for model_name in current_models:
            print(f"🔄 Trying model: {model_name}")
            
            result = self._call_with_retry(prompt, model_name, **kwargs)
            
            if result.startswith("RATE_LIMIT_ERROR:"):
                print(f"🚫 Rate limit exceeded for {model_name}, trying next model...")
                continue
            elif not result.startswith("ERROR:"):
                return result
            else:
                print(f"❌ Model {model_name} failed: {result}")
                continue
        
        # All models failed
        error_msg = f"All Gemini models failed for task {self.task_type}"
        print(f"❌ {error_msg}")
        return f"Error: {error_msg}"
    
    @property
    def _llm_type(self) -> str:
        return f"gemini_multi_{self.task_type}"
    
    def _generate(self, prompts: List[str], stop: List[str] = None, run_manager: CallbackManagerForLLMRun = None, **kwargs: Any) -> LLMResult:
        """Generate for multiple prompts with proper rate limiting"""
        generations = []
        for i, prompt in enumerate(prompts):
            # Add longer delay between multiple prompts
            if i > 0:
                time.sleep(10)  # Even longer delay between batch prompts
            text = self._call(prompt, stop=stop, run_manager=run_manager, **kwargs)
            generations.append([{"generation_info": {}, "text": text}])
        return LLMResult(generations=generations)


# Global shared model manager to coordinate rate limiting across all agents
_shared_model_manager = None

def get_shared_model_manager():
    global _shared_model_manager
    if _shared_model_manager is None:
        _shared_model_manager = GeminiModelManager()
    return _shared_model_manager

def get_crewai_gemini_llm(task_type: str = "general"):
    """Get a CrewAI LLM that uses your existing multi-model Gemini system"""
    
    # Use SHARED model manager for all agents
    model_manager = get_shared_model_manager()
    gemini_llm = GeminiLLM(model_manager, task_type)
    
    # Get the actual model name from your mapping
    model_key = model_manager.get_model_for_task(task_type)
    actual_model = model_manager.models[model_key]
    
    # Create CrewAI LLM wrapper with settings for comprehensive reports
    crewai_llm = LLM(
        model=f"gemini/{actual_model}",  # Use your actual model selection
        temperature=0.7,
        max_tokens=8192,   # Much higher token limit for comprehensive reports
        api_key=os.getenv("GEMINI_API_KEY"),
        max_retries=1,     # Reduce retries to avoid rate limits
        request_timeout=120,  # Longer timeout for large outputs
    )
    
    # Store your GeminiLLM instance for reference
    crewai_llm._gemini_llm = gemini_llm
    
    print(f"🔧 CrewAI using {actual_model} for {task_type}")
    return crewai_llm