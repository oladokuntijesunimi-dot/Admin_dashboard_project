from langchain_tavily import TavilySearch
from config import Config

def get_search_tool():
    """
    Returns the Tavily search tool for real-time web data.
    """
    return TavilySearch(
        max_results=4, # Fetch top 4 results
        api_key=Config.TAVILY_API_KEY
    )
