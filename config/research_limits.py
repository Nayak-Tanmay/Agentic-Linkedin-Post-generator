"""Central limits for research depth, iterations, and token savings."""

MAX_ITERATIONS = 2

RESEARCH_DEPTH_LIMITS: dict[str, tuple[int, int]] = {
    "quick": (3, 5),
    "medium": (5, 8),
    "deep": (8, 12),
}

MAX_CORRECTIVE_QUERIES = 5
MIN_CORRECTIVE_QUERIES = 2

MAX_FINDINGS_FOR_SYNTHESIS = 15
MAX_FINDINGS_FOR_CONFLICT_CHECK = 12

MAX_RESEARCH_TASKS_DEFAULT = 12


def get_max_research_tasks(research_depth: str) -> int:
    depth = research_depth.strip().lower()
    if depth in RESEARCH_DEPTH_LIMITS:
        return RESEARCH_DEPTH_LIMITS[depth][1]
    return RESEARCH_DEPTH_LIMITS["medium"][1]
