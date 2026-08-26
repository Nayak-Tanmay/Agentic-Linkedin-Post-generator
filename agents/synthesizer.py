from pydantic import BaseModel


class SynthesisOutput(BaseModel):

    key_insights: list[str]

    trends: list[str]

    controversies: list[str]

    linkedin_angles: list[str]

    hook_ideas: list[str]

    target_post_style: str

from pathlib import Path

from pydantic import BaseModel

from tools.llm import get_llm


class SynthesisOutput(BaseModel):

    key_insights: list[str]

    trends: list[str]

    controversies: list[str]

    linkedin_angles: list[str]

    hook_ideas: list[str]


def synthesizer_agent(research_notes: str):

    prompt_path = Path("prompts/synthesizer.txt")

    system_prompt = prompt_path.read_text(
        encoding="utf-8"
    )

    llm = get_llm()

    structured_llm = llm.with_structured_output(
        SynthesisOutput
    )

    response = structured_llm.invoke(
        f"""
        {system_prompt}

        Research Notes:

        {research_notes}
        """
    )

    return response