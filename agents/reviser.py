from pathlib import Path

from pydantic import BaseModel

from tools.llm import get_llm


class RevisionOutput(BaseModel):

    revised_post: str


def reviser_agent(
    linkedin_post: str,
    evaluation
):

    # Support both Pydantic objects and dictionaries
    if hasattr(evaluation, "model_dump"):
        evaluation = evaluation.model_dump()

    prompt_path = Path(
        "prompts/reviser.txt"
    )

    system_prompt = prompt_path.read_text(
        encoding="utf-8"
    )

    llm = get_llm()

    structured_llm = llm.with_structured_output(
        RevisionOutput
    )

    response = structured_llm.invoke(
        f"""
        {system_prompt}

        Original LinkedIn Post:

        {linkedin_post}

        Overall Score:
        {evaluation.get("overall_score", 0)}

        Strengths:
        {evaluation.get("strengths", [])}

        Weaknesses:
        {evaluation.get("weaknesses", [])}

        Improvement Suggestions:
        {evaluation.get("improvement_suggestions", [])}

        Instructions:

        - Preserve the strengths.
        - Fix the weaknesses.
        - Apply the improvement suggestions.
        - Improve engagement.
        - Improve originality.
        - Improve clarity.
        - Improve hook quality.
        - Improve CTA.
        - Keep the core message intact.

        Return only the improved LinkedIn post.
        """
    )

    return response