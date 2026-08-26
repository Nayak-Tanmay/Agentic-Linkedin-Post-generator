from agents.researchers.base import search_and_extract


def blog_researcher(query: str) -> list:

    return search_and_extract(
        query=query,
        source="blogs",
        search_query=f"{query} expert blog analysis",
    )
