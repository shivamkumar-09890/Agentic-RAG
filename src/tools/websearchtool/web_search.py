from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.tools import DuckDuckGoSearchRun
import os
import asyncio
from typing import Optional, Type, List

WEB_SEARCH_PROVIDER = 'tavily'

class WebSearchInput(BaseModel):
    query: str = Field(description="The search query")

class WebSearchTool(BaseTool):
    name: str = "web_search"
    description: str = "Search the web for information"
    args_schema: Type[BaseModel] = WebSearchInput

    tavily_api_wrapper: Optional[TavilySearchResults] = None
    duckduckgo_api_wrapper: Optional[DuckDuckGoSearchRun] = None

    def __init__(self):
        super().__init__()

        # Initialize the API wrappers conditionally
        if os.getenv('TAVILY_API_KEY'):
            self.tavily_api_wrapper = TavilySearchResults(
                max_results=5,
                search_depth="advanced",
                include_answer=True,
                include_raw_content=True
            )

        if not self.tavily_api_wrapper:
            self.duckduckgo_api_wrapper = DuckDuckGoSearchRun(max_results=5)

    def _run(self, query: str) -> str:
        try:
            if not query.strip():
                return "Error: Empty search query provided"

            search_results = self._search_web(query)

            if not self._is_content_sufficient(search_results):
                urls = self._extract_urls(search_results)
                scraped_data = asyncio.run(self._scrape_webpages(urls))
                return scraped_data

            return search_results
        except Exception as e:
            return f"Error performing web search: {str(e)}"

    def _search_web(self, query: str) -> str:
        if self.tavily_api_wrapper and WEB_SEARCH_PROVIDER == "tavily":
            try:
                results = self.tavily_api_wrapper.invoke(query)
                return str(results)
            except Exception as e:
                print(f"Tavily search error: {e}")

        if self.duckduckgo_api_wrapper:
            try:
                return self.duckduckgo_api_wrapper.invoke(query)
            except Exception as e:
                print(f"DuckDuckGo search error: {e}")

        return "No search provider available"

    def _is_content_sufficient(self, search_results: str) -> bool:
        return len(search_results) > 100

    def _extract_urls(self, search_results: str) -> List[str]:
        return [res['url'] for res in eval(search_results) if 'url' in res]

    async def _scrape_webpages(self, urls: List[str]) -> str:
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            context = await browser.new_context()
            page = await context.new_page()

            results = {}
            for url in urls:
                try:
                    await page.goto(url)
                    text = await page.evaluate("document.body.innerText")
                    results[url] = text[:1000]
                except Exception as e:
                    results[url] = f"Error scraping: {e}"

            await browser.close()
            return str(results)

# Example usage
if __name__ == "__main__":
    tool = WebSearchTool()
    query = "What are profit made by apple company this year"
    result = tool._run(query)
    print(result)
