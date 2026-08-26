from agents.research_models import ResearchFinding

from memory.retrieval.retriever import retrieve


def memory_researcher(
    query: str,
) -> list[ResearchFinding]:
    """Retrieve findings from user memory (Chroma). Grading is done by CRAG."""

    chunks = retrieve(query)

    if not chunks:
        return []

    findings: list[ResearchFinding] = []

    for rank, chunk in enumerate(chunks):

        relevance = round(1.0 - (rank * 0.1), 2)

        findings.append(
            ResearchFinding(
                source="memory",
                query=query,
                title=chunk.metadata.get(
                    "source",
                    "User Reference",
                ),
                summary=chunk.page_content[:800],
                url=chunk.metadata.get("url", ""),
                relevance_score=max(relevance, 0.5),
            )
        )

    return findings
