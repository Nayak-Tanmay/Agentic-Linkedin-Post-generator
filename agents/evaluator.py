from pathlib import Path

from pydantic import BaseModel

from tools.llm import get_llm


class EvaluationOutput(BaseModel):

    hook_score: float

    clarity_score: float

    engagement_score: float

    originality_score: float

    accuracy_score: float

    structure_score: float

    overall_score: float

    writing_quality_score: float

    research_quality_score: float

    strengths: list[str]

    weaknesses: list[str]

    improvement_suggestions: list[str]


def evaluator_agent(linkedin_post: str):

    prompt_path = Path(
        "prompts/evaluator.txt"
    )

    system_prompt = prompt_path.read_text(
        encoding="utf-8"
    )

    llm = get_llm()

    structured_llm = llm.with_structured_output(
        EvaluationOutput
    )

    response = structured_llm.invoke(
        f"""
        {system_prompt}

        LinkedIn Post:

        {linkedin_post}
        """
    )

    return response