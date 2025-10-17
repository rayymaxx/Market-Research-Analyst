"""
Executive Summary LCEL Chain
"""
from typing import List, Dict 
from pydantic import BaseModel, Field
from ..base import BaseChain, ChainInput
from ...prompts.prompt_registry import prompt_registry

class StrategicRecommendation(BaseModel):
    """Strategic recommendation"""
    priority: str = Field(description="Priority level")
    action: str = Field(description="Action to take")
    timeline: str = Field(description="Timeline")
    resources: str = Field(description="Required resources")
    expected_outcome: str = Field(description="Expected outcome")

class RiskAssessment(BaseModel):
    """Risk assessment"""
    risk: str = Field(description="Risk description")
    probability: str = Field(description="Probability")
    impact: str = Field(description="Impact level")
    mitigation: str = Field(description="Mitigation strategy")

class ExecutiveSummary(BaseModel):
    """Executive summary"""
    market_overview: str = Field(description="Market overview")
    key_insights: List[str] = Field(description="Key insights")
    strategic_recommendations: List[StrategicRecommendation] = Field(description="Recommendations")
    risk_assessment: List[RiskAssessment] = Field(description="Risk assessment")
    success_metrics: List[str] = Field(description="Success metrics")

class ExecutiveSummaryInput(ChainInput):
    """Executive summary input"""
    analysis_results: Dict = Field(description="Analysis results")
    target_audience: str = Field(default="executives", description="Target audience")

class ExecutiveSummaryChain(BaseChain[ExecutiveSummary]):
    """LCEL chain for executive summary generation"""
    
    def __init__(self, llm):
        system_prompt = prompt_registry.get_prompt("reporting", "executive_summary")
        super().__init__(llm, ExecutiveSummary, system_prompt)
    
    def generate_summary(self, research_topic: str, analysis_results: Dict, **kwargs) -> ExecutiveSummary:
        """Convenience method for summary generation"""
        input_data = {
            "research_topic": research_topic,
            "current_date": kwargs.get("current_date", "Current date not provided"),
            "analysis_results": analysis_results,
            "target_audience": kwargs.get("target_audience", "executives"),
            "input": f"Create executive summary for: {research_topic}"
        }
        return self.invoke(input_data)