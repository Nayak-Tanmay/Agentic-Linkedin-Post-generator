from agents.researchers.base import search_and_extract


def github_researcher(query: str) -> list:

    return search_and_extract(
        query=query,
        source="github",
        search_query=f"site:github.com {query} GitHub repository",
    )
