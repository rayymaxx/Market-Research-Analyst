"""
Enhanced prompt registry with validation and type safety
"""
from .analysis_prompts import AnalysisPrompts
from .research_prompts import ResearchPrompts
from .reporting_prompts import ReportingPrompts
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, ValidationError
import logging

logger = logging.getLogger(__name__)

class PromptValidation(BaseModel):
    """Pydantic model for prompt validation"""
    category: str
    prompt_name: str
    required_variables: List[str]
    optional_variables: List[str] = []

class PromptRegistry:
    """Enhanced registry with validation and type safety"""
    
    def __init__(self):
        self.managers = {
            "analysis": AnalysisPrompts(),
            "research": ResearchPrompts(), 
            "reporting": ReportingPrompts(),
        }
        
        self._setup_validation_rules()
    
    def _setup_validation_rules(self):
        """Setup validation rules for each prompt"""
        self.validation_rules = {
            "analysis": {
                "swot_analysis": PromptValidation(
                    category="analysis",
                    prompt_name="swot_analysis",
                    required_variables=["research_topic", "current_date", "format_instructions"],
                    optional_variables=["competitor_data", "market_data", "company_data", "context_data"]
                ),
                "competitive_benchmarking": PromptValidation(
                    category="analysis", 
                    prompt_name="competitive_benchmarking",
                    required_variables=["research_topic", "current_date", "competitors", "format_instructions"],
                    optional_variables=["context_data"]
                )
            },
            "research": {
                "data_collection": PromptValidation(
                    category="research",
                    prompt_name="data_collection", 
                    required_variables=["research_topic", "current_date", "format_instructions"],
                    optional_variables=["primary_sources", "secondary_sources", "tertiary_sources"]
                )
            }
        }
    
    def get_prompt(self, category: str, prompt_name: str, variables: Dict[str, Any] = None) -> str:
        """Get a prompt with validation"""
        # Validate inputs
        self._validate_request(category, prompt_name, variables or {})
        
        manager = self.managers.get(category)
        if not manager:
            raise ValueError(f"Prompt category '{category}' not found. Available: {list(self.managers.keys())}")
        
        return manager.get_prompt(prompt_name, variables)
    
    def _validate_request(self, category: str, prompt_name: str, variables: Dict[str, Any]):
        """Validate prompt request against rules"""
        category_rules = self.validation_rules.get(category, {})
        validation_rule = category_rules.get(prompt_name)
        
        if not validation_rule:
            logger.warning(f"No validation rules for {category}.{prompt_name}")
            return
        
        # Check required variables
        missing_required = [var for var in validation_rule.required_variables if var not in variables]
        if missing_required:
            raise ValueError(f"Missing required variables for {category}.{prompt_name}: {missing_required}")
        
        # Warn about unknown variables
        all_allowed = validation_rule.required_variables + validation_rule.optional_variables
        unknown_vars = [var for var in variables.keys() if var not in all_allowed]
        if unknown_vars:
            logger.warning(f"Unknown variables for {category}.{prompt_name}: {unknown_vars}")

# Global instance for easy access
prompt_registry = PromptRegistry()