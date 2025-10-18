"""
Competitive Benchmarking LCEL Chain
"""
from typing import List, Dict
from pydantic import BaseModel, Field
from ..base import BaseChain, ChainInput
from ...prompts.prompt_registry import prompt_registry

class CompetitorScore(BaseModel):
    """Competitor scoring"""
    name: str = Field(description="Competitor name")
    product_score: float = Field(description="Product score")
    pricing_score: float = Field(description="Pricing score") 
    market_presence_score: float = Field(description="Market presence score")
    customer_focus_score: float = Field(description="Customer focus score")
    overall_score: float = Field(description="Overall score")
    strengths: List[str] = Field(description="Key strengths")
    weaknesses: List[str] = Field(description="Key weaknesses")

class CompetitiveBenchmarking(BaseModel):
    """Competitive benchmarking results"""
    competitors: List[CompetitorScore] = Field(description="Scored competitors")
    key_findings: List[str] = Field(description="Key insights")
    competitive_landscape: str = Field(description="Market positioning")

class BenchmarkingInput(ChainInput):
    """Benchmarking input"""
    competitors: List[Dict] = Field(description="Competitors to benchmark")

class CompetitiveBenchmarkingChain(BaseChain[CompetitiveBenchmarking]):
    """LCEL chain for competitive benchmarking"""
    
    def __init__(self, llm):
        system_prompt = prompt_registry.get_prompt("analysis", "competitive_benchmarking")
        super().__init__(llm, CompetitiveBenchmarking, system_prompt)
    
    def benchmark(self, research_topic: str, competitors: List[Dict], **kwargs) -> CompetitiveBenchmarking:
        """Convenience method for benchmarking"""
        input_data = {
            "research_topic": research_topic,
            "current_date": kwargs.get("current_date", "Current date not provided"),
            "competitors": competitors,
            "input": f"Benchmark competitors for: {research_topic}"
        }
        return self.invoke(input_data)