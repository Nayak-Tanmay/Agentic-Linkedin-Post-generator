from dotenv import load_dotenv
from tavily import TavilyClient
import os

load_dotenv()

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


def search_web(query: str):

    return client.search(
        query=query,
        search_depth="basic",   # cheaper than advanced
        max_results=3           # enough for testing
    )