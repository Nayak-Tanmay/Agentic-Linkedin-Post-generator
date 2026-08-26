from agents.research_models import ResearchFinding
from agents.researchers import RESEARCHER_MAP
from agents.source_selector import ResearchTask
from config.research_limits import MAX_RESEARCH_TASKS_DEFAULT


def dispatch_research_tasks(
    tasks: list[ResearchTask],
    max_tasks: int | None = None,
) -> list[ResearchFinding]:

    limit = max_tasks or MAX_RESEARCH_TASKS_DEFAULT
    all_findings: list[ResearchFinding] = []

    for task in tasks[:limit]:

        researcher = RESEARCHER_MAP.get(task.source)

        if researcher is None:

            print(
                f"Unknown source '{task.source}', "
                f"skipping query: {task.query}"
            )
            continue

        print(
            f"\nResearching [{task.source}]: "
            f"{task.query}"
        )

        findings = researcher(task.query)

        all_findings.extend(findings)

    return all_findings
