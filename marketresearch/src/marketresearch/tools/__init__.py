# src/marketresearch/tools/__init__.py
from .web_search_tool import WebSearchTool
from .news_search_tool import NewsSearchTool

from .chain_tools import (
    SWOTAnalysisTool, 
    CompanyResearchChainTool, 
    MarketTrendsTool,
    CompetitiveBenchmarkingTool
)

# Factory function to create all tools
def create_all_tools():
    """Create and return all market research tools"""
    return [
        WebSearchTool(),
        NewsSearchTool(),

    ]

__all__ = [
    "WebSearchTool",
    "NewsSearchTool", 

    "SWOTAnalysisTool",
    "CompanyResearchChainTool", 
    "MarketTrendsTool",
    "CompetitiveBenchmarkingTool",
    "create_all_tools"
]