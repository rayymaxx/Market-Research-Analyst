from .base_tool import BaseMarketTool

class StockDataTool(BaseMarketTool):
    name: str = "Stock Data"
    description: str = "Get stock price, market data, and financial information for public companies"
    
    def _run(self, symbol: str) -> str:
        """Get stock data from Alpha Vantage"""
        api_key = self._get_api_key("ALPHA_VANTAGE_API_KEY")
        if not api_key:
            return self._format_error("Alpha Vantage API key not configured")
        
        # Clean and uppercase symbol
        symbol = symbol.upper().strip()
        
        # Try global quote first
        quote_result = self._get_global_quote(symbol, api_key)
        if "Error:" not in quote_result:
            return quote_result
        
        # If quote fails, try overview
        overview_result = self._get_company_overview(symbol, api_key)
        return overview_result
    
    def _get_global_quote(self, symbol: str, api_key: str) -> str:
        """Get current stock quote"""
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": api_key
        }
        
        result = self._make_api_request(
            "https://www.alphavantage.co/query",
            params=params
        )
        
        if "error" in result:
            return self._format_error(result["error"])
        
        if "Global Quote" in result and result["Global Quote"]:
            quote = result["Global Quote"]
            return self._format_quote_data(quote, symbol)
        
        return self._format_error(f"No stock data found for {symbol}")
    
    def _get_company_overview(self, symbol: str, api_key: str) -> str:
        """Get company overview as fallback"""
        params = {
            "function": "OVERVIEW",
            "symbol": symbol,
            "apikey": api_key
        }
        
        result = self._make_api_request(
            "https://www.alphavantage.co/query",
            params=params
        )
        
        if "error" in result:
            return self._format_error(result["error"])
        
        if result and "Symbol" in result:
            return self._format_overview_data(result, symbol)
        
        return self._format_error(f"No company data found for {symbol}")
    
    def _format_quote_data(self, quote: dict, symbol: str) -> str:
        """Format stock quote data"""
        price = quote.get("05. price", "N/A")
        change = quote.get("09. change", "N/A")
        change_percent = quote.get("10. change percent", "N/A")
        volume = quote.get("06. volume", "N/A")
        
        return f"""
## Stock Data for {symbol}

**Current Price:** ${price}
**Change:** {change} ({change_percent})
**Volume:** {volume}
**Last Updated:** {quote.get("07. latest trading day", "N/A")}

*Real-time trading data from Alpha Vantage*
"""
    
    def _format_overview_data(self, overview: dict, symbol: str) -> str:
        """Format company overview data"""
        return f"""
## Company Overview for {symbol}

**Company:** {overview.get("Name", "N/A")}
**Sector:** {overview.get("Sector", "N/A")}
**Industry:** {overview.get("Industry", "N/A")}
**Market Cap:** {overview.get("MarketCapitalization", "N/A")}
**P/E Ratio:** {overview.get("PERatio", "N/A")}
**EPS:** {overview.get("EPS", "N/A")}
**Dividend Yield:** {overview.get("DividendYield", "N/A")}

*Fundamental data from Alpha Vantage*
"""