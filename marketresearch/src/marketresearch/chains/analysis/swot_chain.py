"""
SWOT Analysis LCEL Chain
"""
from typing import List, Dict 
from pydantic import BaseModel, Field
from ..base import BaseChain, ChainInput
from ...prompts.prompt_registry import prompt_registry

class SWOTItem(BaseModel):
    """Individual SWOT item"""
    description: str = Field(description="SWOT item description")
    evidence: str = Field(description="Supporting evidence")
    impact: str = Field(description="Impact level")
    confidence: float = Field(description="Confidence score")

class SWOTAnalysis(BaseModel):
    """Complete SWOT analysis"""
    strengths: List[SWOTItem] = Field(description="Strengths")
    weaknesses: List[SWOTItem] = Field(description="Weaknesses") 
    opportunities: List[SWOTItem] = Field(description="Opportunities")
    threats: List[SWOTItem] = Field(description="Threats")
    overall_assessment: str = Field(description="Strategic assessment")

class SWOTInput(ChainInput):
    """SWOT analysis input"""
    competitor_data: Dict = Field(default_factory=dict, description="Competitor data")
    market_data: Dict = Field(default_factory=dict, description="Market data")
    company_data: Dict = Field(default_factory=dict, description="Company data")

class SWOTAnalysisChain(BaseChain[SWOTAnalysis]):
    """LCEL chain for SWOT analysis"""
    
    def __init__(self, llm):
        system_prompt = prompt_registry.get_prompt("analysis", "swot_analysis")
        super().__init__(llm, SWOTAnalysis, system_prompt)
    
    def analyze(self, research_topic: str, **kwargs) -> SWOTAnalysis:
        """Convenience method for SWOT analysis"""
        input_data = {
            "research_topic": research_topic,
            "current_date": kwargs.get("current_date", "Current date not provided"),
            "competitor_data": kwargs.get("competitor_data", {}),
            "market_data": kwargs.get("market_data", {}),
            "company_data": kwargs.get("company_data", {}),
            "input": f"Conduct SWOT analysis for: {research_topic}"
        }
        return self.invoke(input_data)