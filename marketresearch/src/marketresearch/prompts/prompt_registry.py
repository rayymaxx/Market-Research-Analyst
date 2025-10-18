"""
Enhanced prompt registry with deferred validation
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
    """Enhanced registry with deferred validation"""
    
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
                ),
                "market_trends": PromptValidation(
                    category="analysis",
                    prompt_name="market_trends",
                    required_variables=["research_topic", "current_date", "format_instructions"],
                    optional_variables=["market_data"]
                )
            },
            "research": {
                "data_collection": PromptValidation(
                    category="research",
                    prompt_name="data_collection", 
                    required_variables=["research_topic", "current_date", "format_instructions"],
                    optional_variables=["primary_sources", "secondary_sources", "tertiary_sources"]
                ),
                "company_research": PromptValidation(
                    category="research",
                    prompt_name="company_research",
                    required_variables=["research_topic", "current_date", "company_name", "format_instructions"],
                    optional_variables=["data_sources", "industry_context"]
                ),
                "industry_analysis": PromptValidation(
                    category="research",
                    prompt_name="industry_analysis",
                    required_variables=["research_topic", "current_date", "industry_name", "format_instructions"],
                    optional_variables=["industry_data"]
                )
            },
            "reporting": {
                "executive_summary": PromptValidation(
                    category="reporting",
                    prompt_name="executive_summary",
                    required_variables=["research_topic", "current_date", "analysis_results", "format_instructions"],
                    optional_variables=["target_audience"]
                ),
                "research_report": PromptValidation(
                    category="reporting",
                    prompt_name="research_report",
                    required_variables=["research_topic", "current_date", "analysis_data", "format_instructions"],
                    optional_variables=["target_audience"]
                ),
                "strategic_recommendations": PromptValidation(
                    category="reporting",
                    prompt_name="strategic_recommendations",
                    required_variables=["research_topic", "current_date", "business_context", "analysis_insights", "format_instructions"],
                    optional_variables=["timeframe"]
                )
            }
        }
    
    def get_prompt(self, category: str, prompt_name: str, variables: Dict[str, Any] = None) -> str:
        """Get a prompt with deferred validation"""
        # Only validate if variables are provided (at execution time)
        if variables:
            self._validate_request(category, prompt_name, variables)
        
        manager = self.managers.get(category)
        if not manager:
            raise ValueError(f"Prompt category '{category}' not found. Available: {list(self.managers.keys())}")
        
        # If no variables provided (at chain creation), return prompt without formatting
        if not variables:
            return manager.prompts.get(prompt_name, "")
        
        return manager.get_prompt(prompt_name, variables)
    
    def _validate_request(self, category: str, prompt_name: str, variables: Dict[str, Any]):
        """Validate prompt request against rules - only called at execution time"""
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