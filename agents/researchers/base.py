from agents.research_models import ResearchFinding
from tools.tavily_search import search_web


def search_and_extract(
    query: str,
    source: str,
    search_query: str,
    max_results: int = 5,
) -> list[ResearchFinding]:

    findings = []

    try:

        results = search_web(search_query)

        for rank, item in enumerate(
            results.get("results", [])[:max_results]
        ):

            relevance = round(
                1.0 - (rank * 0.15),
                2,
            )

            findings.append(
                ResearchFinding(
                    source=source,
                    query=query,
                    title=item.get("title", ""),
                    summary=item.get("content", ""),
                    url=item.get("url", ""),
                    relevance_score=max(relevance, 0.1),
                )
            )

    except Exception as e:

        print(
            f"Search failed [{source}] "
            f"query='{query}': {e}"
        )

    return findings
