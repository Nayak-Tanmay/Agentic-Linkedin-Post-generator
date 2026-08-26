from agents.researchers.github_researcher import github_researcher


def github_agent(topic: str):

    findings = github_researcher(topic)

    return [
        f.model_dump()
        for f in findings
    ]
