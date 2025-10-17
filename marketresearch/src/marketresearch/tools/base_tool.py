from crewai.tools import BaseTool
import aiohttp
import os
from typing import Dict, Any

class BaseMarketTool(BaseTool):
    """Base class for all market research tools with common utilities"""
    
    def _make_api_request(self, url: str, method: str = "GET", **kwargs) -> Dict[str, Any]:
        """Make HTTP request with error handling"""
        import asyncio
        return asyncio.run(self._async_make_api_request(url, method, **kwargs))
    
    async def _async_make_api_request(self, url: str, method: str = "GET", **kwargs) -> Dict[str, Any]:
        """Async implementation of API request"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(method, url, **kwargs) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        return {"error": f"API returned status {response.status}"}
        except Exception as e:
            return {"error": f"Request failed: {str(e)}"}
    
    def _get_api_key(self, key_name: str) -> str:
        """Get API key from environment variables"""
        return os.getenv(key_name, "")
    
    def _format_error(self, message: str) -> str:
        """Format error message for CrewAI"""
        return f"Error: {message}"