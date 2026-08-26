from agents.researchers.base import search_and_extract


def industry_report_researcher(query: str) -> list:

    return search_and_extract(
        query=query,
        source="industry_reports",
        search_query=f"{query} industry report market analysis",
    )
