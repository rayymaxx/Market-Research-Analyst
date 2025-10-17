"""
Industry Analysis LCEL Chain
"""
from typing import List, Dict
from pydantic import BaseModel, Field
from ..base import BaseChain, ChainInput
from ...prompts.prompt_registry import prompt_registry

class IndustryMetric(BaseModel):
    """Industry metric"""
    name: str = Field(description="Metric name")
    value: str = Field(description="Metric value")
    trend: str = Field(description="Trend direction")

class IndustryAnalysis(BaseModel):
    """Industry analysis results"""
    market_size: str = Field(description="Market size estimate")
    growth_rate: str = Field(description="Growth rate")
    key_segments: List[str] = Field(description="Market segments")
    competitive_landscape: str = Field(description="Competitive overview")
    key_metrics: List[IndustryMetric] = Field(description="Industry metrics")
    strategic_implications: List[str] = Field(description="Strategic implications")

class IndustryAnalysisInput(ChainInput):
    """Industry analysis input"""
    industry_data: Dict = Field(default_factory=dict, description="Industry data")

class IndustryAnalysisChain(BaseChain[IndustryAnalysis]):
    """LCEL chain for industry analysis"""
    
    def __init__(self, llm):
        system_prompt = prompt_registry.get_prompt("research", "industry_analysis")
        super().__init__(llm, IndustryAnalysis, system_prompt)
    
    def analyze_industry(self, research_topic: str, industry_data: Dict, **kwargs) -> IndustryAnalysis:
        """Convenience method for industry analysis"""
        input_data = {
            "research_topic": research_topic,
            "current_date": kwargs.get("current_date", "Current date not provided"),
            "industry_data": industry_data,
            "input": f"Analyze industry for: {research_topic}"
        }
        return self.invoke(input_data)