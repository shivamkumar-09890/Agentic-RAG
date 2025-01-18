
# Web search tool implementation using multiple search providers.

import os
from typing import Optional, Type
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.tools import DuckDuckGoSearchRun

# from settings import WEB_SEARCH_PROVIDER

WEB_SEARCH_PROVIDER = 'tavily'

class WebSearchInput(BaseModel):
    query: str = Field(description="The search query")

class WebSearchTool(BaseTool):
    name: str = "web_search"
    description: str = "Search the web for information"
    args_schema: Type[BaseModel] = WebSearchInput

    tavily_api_wrapper: Optional[TavilySearchResults] = None
    duckduckgo_api_wrapper: Optional[object] = None

    def __init__(self):
        super().__init__()
        
        if os.getenv('TAVILY_API_KEY'):
            
            self.tavily_api_wrapper = TavilySearchResults(
                max_results=1,
                search_depth="advanced",
                include_answer=True,
                include_raw_content=True
            )
        
        if not self.tavily_api_wrapper:
            self.duckduckgo_api_wrapper = DuckDuckGoSearchRun(max_results=5)

    def _run(self, query: str) -> str:
        try:
            if not query or not query.strip():
                return "Error: Empty search query provided"
            
            search_results = self._search_web(query)
            return search_results
        except Exception as e:
            return f"Error performing web search: {str(e)}"
    
    def _search_web(self, query: str) -> str:
        if self.tavily_api_wrapper and WEB_SEARCH_PROVIDER == "tavily":
            try:
                results = self.tavily_api_wrapper.invoke(query)
                
                formatted_results = []
                for result in results:
                    formatted_results.append({
                        'title': result.get('title', 'No Title'),
                        'url': result.get('url', ''),
                        'content': result.get('content', '')[:500] + '...'
                    })
                
                return str(formatted_results)
            except Exception as e:
                print(f"Tavily search error: {e}")
        
        if self.duckduckgo_api_wrapper:
            try:
                return self.duckduckgo_api_wrapper.invoke(query)
            except Exception as e:
                print(f"DuckDuckGo search error: {e}")
        
        return "No search provider available"

# # Example to execute the tool

# from web_search import WebSearchTool


# if __name__ == "__main__":
#     print("Running manual test for WebSearch")
#     tool = WebSearchTool()
#     query = "Who is Kiran Silaych?"
#     result = tool._run(query)
#     print(result)
    