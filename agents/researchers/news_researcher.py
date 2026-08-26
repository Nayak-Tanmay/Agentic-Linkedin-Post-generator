from agents.researchers.base import search_and_extract


def news_researcher(query: str) -> list:

    return search_and_extract(
        query=query,
        source="news",
        search_query=f"{query} latest news",
    )
