from pydantic import BaseModel

from tools.llm import get_llm
from tools.tavily_search import search_web


class ResearchOutput(BaseModel):

    research_notes: str


def researcher_agent(
    search_queries: list[str]
) -> str:

    """
    Performs web research using Tavily.

    Receives only NEW search queries.

    Returns structured research notes.
    """

    # Free tier protection
    search_queries = search_queries[:3]

    collected_results = []

    for query in search_queries:

        print(f"\nSearching: {query}")

        try:

            results = search_web(query)

            simplified_results = []

            for item in results.get("results", [])[:3]:

                simplified_results.append(
                    {
                        "title": item.get("title", ""),
                        "content": item.get("content", "")
                    }
                )

            collected_results.append(
                {
                    "query": query,
                    "results": simplified_results
                }
            )

        except Exception as e:

            print(
                f"Search failed for query: {query}"
            )

            print(e)

    if not collected_results:

        return "No research data collected."

    llm = get_llm()

    prompt = f"""
You are an expert research analyst.

Analyze the search results below.

Create structured research notes.

Focus on:

1. Key Concepts

2. Important Insights

3. Statistics and Metrics

4. Current Trends

5. Frameworks / Tools

6. Real-world Examples

7. Industry Adoption

8. Challenges

9. Future Outlook

Keep notes concise but information dense.

Search Results:

{collected_results}
"""

    response = llm.invoke(prompt)

    return response.content