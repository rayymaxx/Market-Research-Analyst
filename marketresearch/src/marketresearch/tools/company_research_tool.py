from .base_tool import BaseMarketTool

class CompanyResearchTool(BaseMarketTool):
    name: str = "Company Research"
    description: str = "Get comprehensive information about a company including overview, news, and market position"
    
    def _run(self, company_name: str) -> str:
        """Comprehensive company research"""
        # Import here to avoid circular imports
        from .web_search_tool import WebSearchTool
        from .news_search_tool import NewsSearchTool
        
        web_tool = WebSearchTool()
        news_tool = NewsSearchTool()
        
        # Get company overview
        overview = web_tool._run(
            f"{company_name} company overview business model products", 
            3
        )
        
        # Get recent news
        news = news_tool._run(company_name, 3)
        
        # Get financial data if available
        financial_info = self._get_financial_info(company_name)
        
        return self._format_company_report(company_name, overview, news, financial_info)
    
    def _get_financial_info(self, company_name: str) -> str:
        """Get basic financial information"""
        from .stock_data_tool import StockDataTool
        
        stock_tool = StockDataTool()
        # Try to get stock data - this will handle errors gracefully
        financial_data = stock_tool._run(company_name)
        
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