from agents.research_models import ResearchFinding


SOURCE_TRUST_PRIORITY = {
    "memory": 1,
    "official_docs": 2,
    "research_papers": 3,
    "government_reports": 4,
    "industry_reports": 5,
    "blogs": 6,
    "news": 7,
    "reddit": 8,
    "social_media": 9,
    "github": 6,
}


def rank_findings_by_trust(
    findings: list[ResearchFinding],
) -> list[ResearchFinding]:

    return sorted(
        findings,
        key=lambda f: (
            SOURCE_TRUST_PRIORITY.get(
                f.source,
                99,
            ),
            -f.relevance_score,
        ),
    )
