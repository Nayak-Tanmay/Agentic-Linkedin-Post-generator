"""Shared research processing helpers used by main.py and the LangGraph workflow."""

from agents.conflict_detection import detect_conflicts
from agents.duplicate_removal import remove_duplicates
from agents.knowledge_ranking import rank_findings_by_trust
from agents.research_aggregator import aggregate_findings
from agents.research_models import ResearchFinding, ResearchConflict
from agents.source_selector import ResearchTask, ResearchTaskList
from config.research_limits import (
    get_max_research_tasks,
    MAX_FINDINGS_FOR_CONFLICT_CHECK,
    MAX_FINDINGS_FOR_SYNTHESIS,
)
from memory.corrective_rag.crag_pipeline import run_crag_research
from memory.memory_manager import memory_manager


def memory_has_content() -> bool:

    try:
        db = memory_manager.get_memory()
        count = db._collection.count()
        return count > 0
    except Exception:
        return False


def limit_research_tasks(
    tasks: ResearchTaskList,
    research_depth: str,
) -> ResearchTaskList:

    max_tasks = get_max_research_tasks(research_depth)

    limited = tasks.tasks[:max_tasks]

    if len(tasks.tasks) > max_tasks:
        print(
            f"\nLimiting research tasks: "
            f"{len(tasks.tasks)} → {max_tasks} "
            f"(depth: {research_depth})"
        )

    return ResearchTaskList(tasks=limited)


def limit_findings(
    findings: list[ResearchFinding],
    max_count: int = MAX_FINDINGS_FOR_SYNTHESIS,
) -> list[ResearchFinding]:

    return findings[:max_count]


def process_findings(
    findings: list[ResearchFinding],
) -> tuple[list[ResearchFinding], list[ResearchConflict]]:

    aggregated = aggregate_findings(findings)
    ranked = rank_findings_by_trust(aggregated)
    unique = remove_duplicates(ranked)

    conflict_input = limit_findings(
        unique,
        MAX_FINDINGS_FOR_CONFLICT_CHECK,
    )

    marked, conflicts = detect_conflicts(conflict_input)

    final = limit_findings(
        marked,
        MAX_FINDINGS_FOR_SYNTHESIS,
    )

    return final, conflicts


def run_research_stage(
    topic: str,
    tasks: list[ResearchTask],
    research_depth: str,
    use_crag: bool = True,
) -> list[ResearchFinding]:
    """
    Run the research stage with optional CRAG.

    If memory has content and CRAG is enabled:
      - Try CRAG first on the main topic.
      - If memory is sufficient, skip external research.
      - If insufficient, CRAG returns memory + corrective external;
        then run remaining planned tasks (within depth budget).

    If no memory, dispatch planned tasks normally.
    """

    from agents.research_dispatcher import (
        dispatch_research_tasks,
    )

    max_tasks = get_max_research_tasks(research_depth)

    if use_crag and memory_has_content():

        print("\n" + "=" * 70)
        print("CRAG — Checking User Memory")
        print("=" * 70)

        crag_findings, sufficient = run_crag_research(
            query=topic,
            topic=topic,
        )

        if sufficient:
            return crag_findings

        remaining_budget = max(
            0,
            max_tasks - len(crag_findings),
        )

        if tasks and remaining_budget > 0:
            external = dispatch_research_tasks(
                tasks,
                max_tasks=remaining_budget,
            )
            return crag_findings + external

        return crag_findings

    return dispatch_research_tasks(
        tasks,
        max_tasks=max_tasks,
    )
