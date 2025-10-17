from .base_tool import BaseMarketTool
import aiohttp

class WebSearchTool(BaseMarketTool):
    name: str = "Web Search"
    description: str = "Searches the web for current market information, trends, and data"

    def _run(self, query: str, max_results: int = 5) -> str:
        """Synchronous wrapper for async search"""
        import asyncio
        return asyncio.run(self._async_search(query, max_results))
    
    async def _async_search(self, query: str, max_results: int) -> str:
        """Perform web search using serper"""
        api_key = self._get_api_key("SERPER_API_KEY")
        if not api_key:
            return self._format_error("Serper API key not configured")
        
        headers = {
            'X-PI-KEY': api_key,
            'Content-Type': 'application/json'
        }
        payload = {
            "q": query,
            "num": min(max_results, 10)
        }

        result = await self._make_api_request(
            "https://google.serper.dev/search",
            method="POST",
            headers=headers,
            json=payload
        )

        if "error" in result:
            return self._format_error(result["error"])
        
        return self._format_search_results(result, query)
    
    def _format_search_results(self, data: dict, query: str) -> str:
        """Format search resuls for CrewAI"""
        if "organic" not in data or not data["organic"]:
            return f"No web results found for: {query}"
        
        results = []
        for i, item in enumerate(data["organic"][:5], 1):
            title = item.get("title", "No title")
            snippet = item.get("snippet", "No description")
            link = item.get("link", "")

            results.append(
                f"{i}. **{title}**\n"
                f"   {snippet}\n"
                f"  Source: {link}\n"
            )

        return f"## Web Search Results for '{query}'\n\n" + "\n".join(results)
    
    