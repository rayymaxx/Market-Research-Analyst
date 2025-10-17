from .base_tool import BaseMarketTool
import asyncio

class CompanyResearchTool(BaseMarketTool):
    name: str = "Company Research"
    description: str = "Get comprehensive information about a company including overview, news, and market position"
    
    def _run(self, company_name: str) -> str:
        """Comprehensive company research"""
        import asyncio
        return asyncio.run(self._async_company_research(company_name))
    
    async def _async_company_research(self, company_name: str) -> str:
        """Perform comprehensive company research"""
        # Import here to avoid circular imports
        from .web_search_tool import WebSearchTool
        from .news_search_tool import NewsSearchTool
        
        web_tool = WebSearchTool()
        news_tool = NewsSearchTool()
        
        # Get company overview
        overview = await web_tool._async_search(
            f"{company_name} company overview business model products", 
            3
        )
        
        # Get recent news
        news = await news_tool._async_news_search(company_name, 3)
        
        # Get financial data if available
        financial_info = await self._get_financial_info(company_name)
        
        return self._format_company_report(company_name, overview, news, financial_info)
    
    async def _get_financial_info(self, company_name: str) -> str:
        """Get basic financial information"""
        from .stock_data_tool import StockDataTool
        
        stock_tool = StockDataTool()
        # Try to get stock data - this will handle errors gracefully
        financial_data = await stock_tool._async_get_stock_data(company_name)
        
        if "Error:" not in financial_data:
            return financial_data
        return "Financial data not available for this company"
    
    def _format_company_report(self, company_name: str, overview: str, news: str, financial: str) -> str:
        """Format comprehensive company report"""
        return f"""
# Company Research Report: {company_name}

## Company Overview
{overview.split('##', 1)[-1] if '##' in overview else overview}

## Recent News & Developments
{news.split('##', 1)[-1] if '##' in news else news}

## Financial Information
{financial}

## Key Insights
- Market position and competitive landscape
- Recent developments and news coverage
- Financial performance (if available)
- Potential growth opportunities
"""