"""
Data Collection LCEL Chain
"""
from typing import Dict, List
from pydantic import BaseModel, Field
from ..base import BaseChain, ChainInput
from ...prompts.prompt_registry import prompt_registry

class CollectedData(BaseModel):
    """Collected market data"""
    competitor_data: Dict = Field(description="Competitor intelligence")
    market_metrics: Dict = Field(description="Market metrics")
    consumer_insights: Dict = Field(description="Consumer insights")
    industry_trends: Dict = Field(description="Industry trends")
    data_sources: List[str] = Field(description="Data sources used")

class DataCollectionInput(ChainInput):
    """Data collection input"""
    primary_sources: List[str] = Field(default_factory=list, description="Primary sources")
    secondary_sources: List[str] = Field(default_factory=list, description="Secondary sources")

class DataCollectionChain(BaseChain[CollectedData]):
    """LCEL chain for data collection"""
    
    def __init__(self, llm):
        system_prompt = prompt_registry.get_prompt("research", "data_collection")
        super().__init__(llm, CollectedData, system_prompt)
    
    def collect_data(self, research_topic: str, **kwargs) -> CollectedData:
        """Convenience method for data collection"""
        input_data = {
            "research_topic": research_topic,
            "current_date": kwargs.get("current_date", "Current date not provided"),
            "primary_sources": kwargs.get("primary_sources", []),
            "secondary_sources": kwargs.get("secondary_sources", []),
            "input": f"Collect market data for: {research_topic}"
        }
        return self.invoke(input_data)