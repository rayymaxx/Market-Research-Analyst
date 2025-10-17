from .base_tool import BaseMarketTool

class NewsSearchTool(BaseMarketTool):
    name: str = "News Search"
    description: str = "Search for recent news articles about companies, industries, or market trends"
    
    def _run(self, query: str, max_results: int = 5) -> str:
        """Synchronous wrapper for async news search"""
        import asyncio
        return asyncio.run(self._async_news_search(query, max_results))
    
    async def _async_news_search(self, query: str, max_results: int) -> str:
        """Perform news search using Serper API"""
        api_key = self._get_api_key("SERPER_API_KEY")
        if not api_key:
            return self._format_error("Serper API key not configured")
        
        headers = {
            'X-API-KEY': api_key,
            'Content-Type': 'application/json'
        }
        payload = {
            "q": query,
            "num": min(max_results, 10)
        }
        
        result = await self._make_api_request(
            "https://google.serper.dev/news",
            method="POST",
            headers=headers,
            json=payload
        )
        
        if "error" in result:
            return self._format_error(result["error"])
        
        return self._format_news_results(result, query)
    
    def _format_news_results(self, data: dict, query: str) -> str:
        """Format news results for CrewAI"""
        if "news" not in data or not data["news"]:
            return f"No news articles found for: {query}"
        
        articles = []
        for i, article in enumerate(data["news"][:5], 1):
            title = article.get("title", "No title")
            source = article.get("source", "Unknown source")
            date = article.get("date", "Unknown date")
            snippet = article.get("snippet", "No description")
            
            articles.append(
                f"{i}. **{title}**\n"
                f"   📰 {source} | 📅 {date}\n"
                f"   {snippet}\n"
            )
        
        return f"## News Results for '{query}'\n\n" + "\n".join(articles)