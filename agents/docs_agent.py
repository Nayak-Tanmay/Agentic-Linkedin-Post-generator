from agents.researchers.official_docs_researcher import (
    official_docs_researcher,
)


def docs_agent(topic: str):

    findings = official_docs_researcher(topic)

    return [
        f.model_dump()
        for f in findings
    ]
