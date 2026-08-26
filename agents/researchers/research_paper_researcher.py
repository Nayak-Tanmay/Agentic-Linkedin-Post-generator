from agents.researchers.base import search_and_extract


def research_paper_researcher(query: str) -> list:

    return search_and_extract(
        query=query,
        source="research_papers",
        search_query=f"{query} research paper arxiv",
    )
