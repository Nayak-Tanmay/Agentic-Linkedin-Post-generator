"""Corrective RAG — reuses the existing research pipeline components."""

from agents.query_generator import query_generator_agent
from agents.research_dispatcher import dispatch_research_tasks
from agents.research_models import ResearchFinding
from agents.source_selector import ResearchTask
from config.research_limits import (
    MAX_CORRECTIVE_QUERIES,
    MIN_CORRECTIVE_QUERIES,
)
from memory.corrective_rag.corrective_rag import grade_retrieval
from memory.retrieval.retriever import retrieve


def chunks_to_findings(
    chunks,
    query: str,
) -> list[ResearchFinding]:

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


def _generate_corrective_queries(
    topic: str,
    missing_information: list[str],
) -> list[str]:

    if not missing_information:
        return []

    result = query_generator_agent(
        topic,
        missing_information,
        max_queries=MAX_CORRECTIVE_QUERIES,
    )

    queries = result.additional_search_queries

    if len(queries) < MIN_CORRECTIVE_QUERIES and missing_information:
        for gap in missing_information:
            if gap not in queries:
                queries.append(gap)
            if len(queries) >= MIN_CORRECTIVE_QUERIES:
                break

    return queries[:MAX_CORRECTIVE_QUERIES]


def run_crag_research(
    query: str,
    topic: str | None = None,
) -> tuple[list[ResearchFinding], bool]:
    """
    Run CRAG for a query.

    Returns (findings, memory_was_sufficient).
    When sufficient, findings come from memory only.
    When insufficient, returns memory + corrective external findings.
    """

    topic = topic or query

    print("\n" + "=" * 50)
    print("CRAG — Memory Retrieval")
    print("=" * 50)

    chunks = retrieve(query)

    if not chunks:
        print("No memory chunks found.")
        return [], False

    grade = grade_retrieval(query, chunks)

    print(
        f"Memory sufficient: {grade.sufficient} "
        f"(confidence: {grade.confidence:.2f})"
    )
    print(f"Reasoning: {grade.reasoning}")

    memory_findings = chunks_to_findings(chunks, query)

    if grade.sufficient:
        print(
            f"Using {len(memory_findings)} memory findings. "
            "Skipping external research for this query."
        )
        return memory_findings, True

    print("\nMemory insufficient — running corrective research.")

    if grade.missing_information:
        print("Missing information:")
        for item in grade.missing_information:
            print(f"  - {item}")

    corrective_queries = _generate_corrective_queries(
        topic,
        grade.missing_information,
    )

    if corrective_queries:
        print("\nCorrective queries:")
        for q in corrective_queries:
            print(f"  - {q}")

    gap_tasks = [
        ResearchTask(source="news", query=q)
        for q in corrective_queries
    ]

    external_findings: list[ResearchFinding] = []

    if gap_tasks:
        external_findings = dispatch_research_tasks(
            gap_tasks,
            max_tasks=MAX_CORRECTIVE_QUERIES,
        )

    combined = memory_findings + external_findings

    print(
        f"\nCRAG combined: {len(memory_findings)} memory + "
        f"{len(external_findings)} external = "
        f"{len(combined)} total"
    )

    return combined, False
