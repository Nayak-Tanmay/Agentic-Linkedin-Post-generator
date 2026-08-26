from agents.researchers.research_paper_researcher import (
    research_paper_researcher,
)


def paper_agent(topic: str):

    findings = research_paper_researcher(topic)

    return [
        f.model_dump()
        for f in findings
    ]
