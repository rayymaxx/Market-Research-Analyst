# Update your existing src/marketresearch/chains/__init__.py
"""
LCEL Chains for Market Research with Multi-Model Gemini Support
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

# Import our multi-model components
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.gemini_config import GeminiModelManager, GeminiLLM

class ChainFactory:
    """Factory for creating and managing chains with multi-model Gemini support"""
    
    def __init__(self):
        self.model_manager = GeminiModelManager()
        self._chains = {}
    
    def get_chain(self, chain_type: str):
        """Get or create a chain by type with appropriate Gemini model"""
        if chain_type not in self._chains:
            # Create appropriate Gemini LLM for this chain type
            llm = GeminiLLM(self.model_manager, chain_type)
            
            if chain_type == "swot_analysis":
                self._chains[chain_type] = SWOTAnalysisChain(llm)
            elif chain_type == "competitive_benchmarking":
                self._chains[chain_type] = CompetitiveBenchmarkingChain(llm)
            elif chain_type == "market_trends":
                self._chains[chain_type] = MarketTrendsChain(llm)
            elif chain_type == "executive_summary":
                self._chains[chain_type] = ExecutiveSummaryChain(llm)
            elif chain_type == "research_report":
                self._chains[chain_type] = ResearchReportChain(llm)
            elif chain_type == "strategic_recommendations":
                self._chains[chain_type] = RecommendationsChain(llm)
            elif chain_type == "data_collection":
                self._chains[chain_type] = DataCollectionChain(llm)
            elif chain_type == "industry_analysis":
                self._chains[chain_type] = IndustryAnalysisChain(llm)
            elif chain_type == "company_research":
                self._chains[chain_type] = CompanyResearchChain(llm)
            else:
                raise ValueError(f"Unknown chain type: {chain_type}")
        
        return self._chains[chain_type]
    
    def execute_chain(self, chain_type: str, **kwargs):
        """Execute a chain with the given parameters"""
        chain = self.get_chain(chain_type)
        return chain.invoke(kwargs)
    
    def get_available_models(self):
        """Get list of available Gemini models"""
        return list(self.model_manager.models.keys())
    
    def get_model_for_chain(self, chain_type: str):
        """Get which Gemini model is used for a chain type"""
        return self.model_manager.get_model_for_task(chain_type)

__all__ = [
    "ChainFactory",
    "SWOTAnalysis", "CompetitiveBenchmarking", "MarketTrends",
    "ExecutiveSummary", "ResearchReport", "StrategicRecommendations",
    "CollectedData", "IndustryAnalysis", "CompanyResearch"
]