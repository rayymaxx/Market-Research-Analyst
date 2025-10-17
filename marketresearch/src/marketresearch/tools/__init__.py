from .web_search_tool import WebSearchTool
from .news_search_tool import NewsSearchTool
from .company_research_tool import CompanyResearchTool
from .stock_data_tool import StockDataTool
from .market_data_tool import MarketDataTool

# Factory function to create all tools
def create_all_tools():
    """Create and return all market research tools"""
    return [
        WebSearchTool(),
        NewsSearchTool(),
        CompanyResearchTool(),
        StockDataTool(),
        MarketDataTool()
    ]

__all__ = [
    "WebSearchTool",
    "NewsSearchTool", 
    "CompanyResearchTool",
    "StockDataTool",
    "MarketDataTool",
    "create_all_tools"
]