from agents.researchers.base import search_and_extract


def government_report_researcher(query: str) -> list:

    return search_and_extract(
        query=query,
        source="government_reports",
        search_query=f"{query} government report official",
    )
