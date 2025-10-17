"""
Strategic Recommendations LCEL Chain
"""
from typing import List, Dict
from pydantic import BaseModel, Field
from ..base import BaseChain, ChainInput
from ...prompts.prompt_registry import prompt_registry

class RecommendationItem(BaseModel):
    """Individual recommendation"""
    action: str = Field(description="Recommended action")
    rationale: str = Field(description="Business rationale")
    owner: str = Field(description="Responsible party")
    timeline: str = Field(description="Implementation timeline")
    resources: str = Field(description="Required resources")
    expected_outcome: str = Field(description="Expected outcome")
    success_metrics: List[str] = Field(description="Success metrics")

class StrategicRecommendations(BaseModel):
    """Strategic recommendations"""
    immediate_actions: List[RecommendationItem] = Field(description="Immediate actions (0-3 months)")
    short_term_initiatives: List[RecommendationItem] = Field(description="Short-term initiatives (3-6 months)")
    long_term_strategies: List[RecommendationItem] = Field(description="Long-term strategies (6-12+ months)")
    overall_priority: str = Field(description="Overall strategic priority")

class RecommendationsInput(ChainInput):
    """Recommendations input"""
    business_context: str = Field(description="Business context")
    analysis_insights: Dict = Field(description="Analysis insights")
    timeframe: str = Field(default="12 months", description="Planning timeframe")

class RecommendationsChain(BaseChain[StrategicRecommendations]):
    """LCEL chain for strategic recommendations"""
    
    def __init__(self, llm):
        system_prompt = prompt_registry.get_prompt("reporting", "strategic_recommendations")
        super().__init__(llm, StrategicRecommendations, system_prompt)
    
    def generate_recommendations(self, research_topic: str, business_context: str, analysis_insights: Dict, **kwargs) -> StrategicRecommendations:
        """Convenience method for recommendations generation"""
        input_data = {
            "research_topic": research_topic,
            "current_date": kwargs.get("current_date", "Current date not provided"),
            "business_context": business_context,
            "analysis_insights": analysis_insights,
            "timeframe": kwargs.get("timeframe", "12 months"),
            "input": f"Generate strategic recommendations for: {research_topic}"
        }
        return self.invoke(input_data)