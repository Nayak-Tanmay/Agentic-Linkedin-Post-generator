from pathlib import Path

from pydantic import BaseModel

from tools.llm import get_llm


class ResearchGapOutput(BaseModel):

    research_gaps: list[str]


def research_gap_agent(
    linkedin_post: str,
    evaluation: dict
):

    if hasattr(evaluation, "model_dump"):
        evaluation = evaluation.model_dump()

    prompt = f"""
    You are an expert content strategist.

    Analyze the LinkedIn post and evaluation report.

    Identify missing information that would
    significantly improve the post.

    Focus on:

    - Missing statistics
    - Missing case studies
    - Missing real-world examples
    - Missing trends
    - Missing industry insights
    - Missing research evidence

    LinkedIn Post:

    {linkedin_post}

    Evaluation Report:

    {evaluation}
    """

    llm = get_llm()

    structured_llm = llm.with_structured_output(
        ResearchGapOutput
    )

    response = structured_llm.invoke(prompt)

    return response