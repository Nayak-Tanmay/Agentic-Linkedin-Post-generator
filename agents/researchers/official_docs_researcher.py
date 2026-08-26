from agents.researchers.base import search_and_extract


def official_docs_researcher(query: str) -> list:

    return search_and_extract(
        query=query,
        source="official_docs",
        search_query=f"{query} official documentation",
    )
