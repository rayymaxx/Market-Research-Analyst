"""
Company Research LCEL Chain
"""
from typing import List, Dict
from pydantic import BaseModel, Field
from ..base import BaseChain, ChainInput
from ...prompts.prompt_registry import prompt_registry

class CompanyMetric(BaseModel):
    """Company metric"""
    category: str = Field(description="Metric category")
    value: str = Field(description="Metric value")

class CompanyResearch(BaseModel):
    """Company research results"""
    company_name: str = Field(description="Company name")
    overview: str = Field(description="Company overview")
    products_services: List[str] = Field(description="Products and services")
    market_position: str = Field(description="Market position")
    financial_health: str = Field(description="Financial health")
    key_metrics: List[CompanyMetric] = Field(description="Key metrics")
    strengths: List[str] = Field(description="Company strengths")
    challenges: List[str] = Field(description="Company challenges")

class CompanyResearchInput(ChainInput):
    """Company research input"""
    company_name: str = Field(description="Company to research")
    data_sources: Dict = Field(default_factory=dict, description="Data sources")

class CompanyResearchChain(BaseChain[CompanyResearch]):
    """LCEL chain for company research"""
    
    def __init__(self, llm):
        system_prompt = prompt_registry.get_prompt("research", "company_research")
        super().__init__(llm, CompanyResearch, system_prompt)
    
    def research_company(self, research_topic: str, company_name: str, **kwargs) -> CompanyResearch:
        """Convenience method for company research"""
        input_data = {
            "research_topic": research_topic,
            "current_date": kwargs.get("current_date", "Current date not provided"),
            "company_name": company_name,
            "data_sources": kwargs.get("data_sources", {}),
            "input": f"Research company: {company_name} in context of {research_topic}"
        }
        return self.invoke(input_data)