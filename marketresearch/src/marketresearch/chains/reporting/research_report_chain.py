"""
Research Report LCEL Chain
"""
from typing import List, Dict
from pydantic import BaseModel, Field
from ..base import BaseChain, ChainInput
from ...prompts.prompt_registry import prompt_registry

class ResearchReport(BaseModel):
    """Comprehensive research report"""
    executive_summary: str = Field(description="Executive summary")
    methodology: str = Field(description="Research methodology")
    market_overview: str = Field(description="Market overview")
    competitive_analysis: str = Field(description="Competitive analysis")
    strategic_recommendations: List[str] = Field(description="Recommendations")
    implementation_roadmap: str = Field(description="Implementation plan")

class ResearchReportInput(ChainInput):
    """Research report input"""
    analysis_data: Dict = Field(description="Analysis data")
    target_audience: str = Field(default="stakeholders", description="Target audience")

class ResearchReportChain(BaseChain[ResearchReport]):
    """LCEL chain for research report generation"""
    
    def __init__(self, llm):
        system_prompt = prompt_registry.get_prompt("reporting", "research_report")
        super().__init__(llm, ResearchReport, system_prompt)
    
    def generate_report(self, research_topic: str, analysis_data: Dict, **kwargs) -> ResearchReport:
        """Convenience method for report generation"""
        input_data = {
            "research_topic": research_topic,
            "current_date": kwargs.get("current_date", "Current date not provided"),
            "analysis_data": analysis_data,
            "target_audience": kwargs.get("target_audience", "stakeholders"),
            "input": f"Create research report for: {research_topic}"
        }
        return self.invoke(input_data)