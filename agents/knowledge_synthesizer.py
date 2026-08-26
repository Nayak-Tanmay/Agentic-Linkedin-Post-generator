from pathlib import Path

from agents.research_models import (
    ResearchFinding,
    ResearchConflict,
    KnowledgeSynthesisOutput,
)
from config.research_limits import MAX_FINDINGS_FOR_SYNTHESIS
from tools.llm import get_llm


def _format_findings_for_prompt(
    findings: list[ResearchFinding],
    conflicts: list[ResearchConflict],
) -> str:

    sections = []

    for f in findings:

        entry = (
            f"Source: {f.source}\n"
            f"Title: {f.title}\n"
            f"Summary: {f.summary}\n"
            f"URL: {f.url}\n"
            f"Trust Rank: {f.source}\n"
        )

        if f.has_conflict:

            entry += (
                f"CONFLICT: {f.conflict_notes}\n"
            )

        sections.append(entry)

    conflict_section = ""

    if conflicts:

        conflict_lines = [
            f"- {c.finding_a_title} vs "
            f"{c.finding_b_title}: "
            f"{c.conflict_description}"
            for c in conflicts
        ]

        conflict_section = (
            "\n\nDETECTED CONFLICTS:\n"
            + "\n".join(conflict_lines)
        )

    return "\n---\n".join(sections) + conflict_section


def knowledge_synthesizer_agent(
    findings: list[ResearchFinding],
    conflicts: list[ResearchConflict] | None = None,
) -> KnowledgeSynthesisOutput:

    conflicts = conflicts or []

    limited_findings = findings[:MAX_FINDINGS_FOR_SYNTHESIS]

    if len(findings) > MAX_FINDINGS_FOR_SYNTHESIS:
        print(
            f"Synthesizer: using top "
            f"{MAX_FINDINGS_FOR_SYNTHESIS} of "
            f"{len(findings)} findings"
        )

    findings_text = _format_findings_for_prompt(
        limited_findings,
        conflicts,
    )

    prompt_path = Path(
        "prompts/knowledge_synthesizer.txt"
    )

    if prompt_path.exists():

        system_prompt = prompt_path.read_text(
            encoding="utf-8"
        )

    else:

        system_prompt = (
            "You are an expert research analyst. "
            "Synthesize the research findings into "
            "structured knowledge for LinkedIn content."
        )

    llm = get_llm()

    structured_llm = llm.with_structured_output(
        KnowledgeSynthesisOutput
    )

    return structured_llm.invoke(
        f"""
{system_prompt}

Research Findings:

{findings_text}
"""
    )
