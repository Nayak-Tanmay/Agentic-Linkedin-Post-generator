from urllib.parse import urlparse

from agents.research_models import ResearchFinding


def _normalize_title(title: str) -> str:

    return " ".join(
        title.lower().split()
    )


def _normalize_url(url: str) -> str:

    parsed = urlparse(url)

    return (
        f"{parsed.netloc}{parsed.path}"
        .rstrip("/")
        .lower()
    )


def remove_duplicates(
    findings: list[ResearchFinding],
) -> list[ResearchFinding]:

    seen_urls: set[str] = set()
    seen_titles: set[str] = set()
    unique: list[ResearchFinding] = []

    for finding in findings:

        norm_url = _normalize_url(finding.url)

        if norm_url and norm_url in seen_urls:
            continue

        norm_title = _normalize_title(finding.title)

        if norm_title and norm_title in seen_titles:
            continue

        if norm_url:
            seen_urls.add(norm_url)

        if norm_title:
            seen_titles.add(norm_title)

        unique.append(finding)

    return unique
