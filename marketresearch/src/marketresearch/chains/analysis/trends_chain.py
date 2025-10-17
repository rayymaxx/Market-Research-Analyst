"""
Market Trends Analysis LCEL Chain
"""
from typing import List, Dict 
from pydantic import BaseModel, Field
from ..base import BaseChain, ChainInput
from ...prompts.prompt_registry import prompt_registry

class TrendItem(BaseModel):
    """Individual market trend"""
    trend: str = Field(description="Trend description")
    impact: str = Field(description="Impact level")
    confidence: float = Field(description="Confidence score")
    timing: str = Field(description="Timing estimate")

class MarketTrends(BaseModel):
    """Market trends analysis"""
    technology_trends: List[TrendItem] = Field(description="Technology trends")
    consumer_trends: List[TrendItem] = Field(description="Consumer trends")
    regulatory_trends: List[TrendItem] = Field(description="Regulatory trends")
    economic_trends: List[TrendItem] = Field(description="Economic trends")
    key_insights: List[str] = Field(description="Key insights")

class TrendsInput(ChainInput):
    """Trends analysis input"""
    market_data: Dict = Field(default_factory=dict, description="Market data")

class MarketTrendsChain(BaseChain[MarketTrends]):
    """LCEL chain for market trends analysis"""
    
    def __init__(self, llm):
        system_prompt = prompt_registry.get_prompt("analysis", "market_trends")
        super().__init__(llm, MarketTrends, system_prompt)
    
    def analyze_trends(self, research_topic: str, market_data: Dict, **kwargs) -> MarketTrends:
        """Convenience method for trends analysis"""
        input_data = {
            "research_topic": research_topic,
            "current_date": kwargs.get("current_date", "Current date not provided"),
            "market_data": market_data,
            "input": f"Analyze market trends for: {research_topic}"
        }
        return self.invoke(input_data)