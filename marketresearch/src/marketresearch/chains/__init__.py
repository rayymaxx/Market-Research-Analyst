"""
LCEL Chains for Market Research
"""
from .analysis.swot_chain import SWOTAnalysisChain, SWOTAnalysis
from .analysis.benchmarking_chain import CompetitiveBenchmarkingChain, CompetitiveBenchmarking
from .analysis.trends_chain import MarketTrendsChain, MarketTrends
from .reporting.executive_summary_chain import ExecutiveSummaryChain, ExecutiveSummary
from .reporting.research_report_chain import ResearchReportChain, ResearchReport
from .reporting.recommendations_chain import RecommendationsChain, StrategicRecommendations
from .research.data_collection_chain import DataCollectionChain, CollectedData
from .research.industry_analysis_chain import IndustryAnalysisChain, IndustryAnalysis
from .research.company_research_chain import CompanyResearchChain, CompanyResearch

class ChainFactory:
    """Factory for creating and managing chains"""
    
    def __init__(self, llm):
        self.llm = llm
        self._chains = {}
    
    def get_chain(self, chain_type: str):
        """Get or create a chain by type"""
        if chain_type not in self._chains:
            if chain_type == "swot_analysis":
                self._chains[chain_type] = SWOTAnalysisChain(self.llm)
            elif chain_type == "competitive_benchmarking":
                self._chains[chain_type] = CompetitiveBenchmarkingChain(self.llm)
            elif chain_type == "market_trends":
                self._chains[chain_type] = MarketTrendsChain(self.llm)
            elif chain_type == "executive_summary":
                self._chains[chain_type] = ExecutiveSummaryChain(self.llm)
            elif chain_type == "research_report":
                self._chains[chain_type] = ResearchReportChain(self.llm)
            elif chain_type == "strategic_recommendations":
                self._chains[chain_type] = RecommendationsChain(self.llm)
            elif chain_type == "data_collection":
                self._chains[chain_type] = DataCollectionChain(self.llm)
            elif chain_type == "industry_analysis":
                self._chains[chain_type] = IndustryAnalysisChain(self.llm)
            elif chain_type == "company_research":
                self._chains[chain_type] = CompanyResearchChain(self.llm)
            else:
                raise ValueError(f"Unknown chain type: {chain_type}")
        
        return self._chains[chain_type]
    
    def execute_chain(self, chain_type: str, **kwargs):
        """Execute a chain with the given parameters"""
        chain = self.get_chain(chain_type)
        return chain.invoke(kwargs)

__all__ = [
    "ChainFactory",
    "SWOTAnalysis", "CompetitiveBenchmarking", "MarketTrends",
    "ExecutiveSummary", "ResearchReport", "StrategicRecommendations",
    "CollectedData", "IndustryAnalysis", "CompanyResearch"
]