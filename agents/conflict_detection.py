from pydantic import BaseModel

from agents.research_models import ResearchFinding, ResearchConflict
from tools.llm import get_llm


class ConflictDetectionOutput(BaseModel):
    conflicts: list[ResearchConflict]


def detect_conflicts(
    findings: list[ResearchFinding],
) -> tuple[list[ResearchFinding], list[ResearchConflict]]:

    if len(findings) < 2:
        return findings, []

    summaries = []

    for i, f in enumerate(findings):

        summaries.append(
            f"[{i}] ({f.source}) {f.title}: "
            f"{f.summary[:200]}"
        )

    llm = get_llm()

    structured_llm = llm.with_structured_output(
        ConflictDetectionOutput
    )

    response = structured_llm.invoke(
        f"""
You are a research analyst.

Review the findings below and identify
contradictory or conflicting information
between different sources.

Only report genuine factual contradictions,
not differences in perspective or emphasis.

If no conflicts exist, return an empty list.

Findings:

{chr(10).join(summaries)}
"""
    )

    marked = list(findings)
    conflict_titles = set()

    for conflict in response.conflicts:

        conflict_titles.add(
            conflict.finding_a_title.lower()
        )
        conflict_titles.add(
            conflict.finding_b_title.lower()
        )

    for finding in marked:

        if finding.title.lower() in conflict_titles:

            finding.has_conflict = True

            related = [
                c.conflict_description
                for c in response.conflicts
                if (
                    finding.title.lower()
                    in (
                        c.finding_a_title.lower(),
                        c.finding_b_title.lower(),
                    )
                )
            ]

            finding.conflict_notes = "; ".join(
                related
            )

    return marked, response.conflicts
