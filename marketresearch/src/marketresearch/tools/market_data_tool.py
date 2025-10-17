from .base_tool import BaseMarketTool

class MarketDataTool(BaseMarketTool):
    name: str = "Market Data"
    description: str = "Get market trends, industry analysis, and economic indicators"
    
    def _run(self, industry: str, region: str = "global") -> str:
        """Get market data for specific industry"""
        import asyncio
        return asyncio.run(self._async_get_market_data(industry, region))
    
    async def _async_get_market_data(self, industry: str, region: str) -> str:
        """Get comprehensive market data"""
        from .web_search_tool import WebSearchTool
        from .news_search_tool import NewsSearchTool
        
        web_tool = WebSearchTool()
        news_tool = NewsSearchTool()
        
        # Search for market trends
        trends_query = f"{industry} market trends growth forecast {region}"
        trends = await web_tool._async_search(trends_query, 4)
        
        # Search for industry news
        industry_news = await news_tool._async_news_search(f"{industry} industry", 3)
        
        # Get economic context
        economic_context = await self._get_economic_context()
        
        return self._format_market_report(industry, region, trends, industry_news, economic_context)
    
    async def _get_economic_context(self) -> str:
        """Get relevant economic indicators"""
        # This can be expanded with FRED API later
        return """
## Economic Context
- Global economic trends affecting all markets
- Interest rate environment
- Inflation considerations
- Consumer sentiment indicators
"""
    
    def _format_market_report(self, industry: str, region: str, trends: str, news: str, economic: str) -> str:
        """Format comprehensive market report"""
        return f"""
# Market Analysis: {industry} ({region})

## Market Trends & Forecast
{trends.split('##', 1)[-1] if '##' in trends else trends}

## Industry Developments
{news.split('##', 1)[-1] if '##' in news else news}

{economic}

## Key Market Insights
- Growth drivers and opportunities
- Competitive landscape dynamics
- Regulatory and economic factors
- Future outlook and projections
"""