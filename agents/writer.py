from pydantic import BaseModel


class WriterOutput(BaseModel):

    linkedin_post: str
from pathlib import Path

from pydantic import BaseModel

from tools.llm import get_llm


class WriterOutput(BaseModel):

    linkedin_post: str


def writer_agent(synthesis):

    if hasattr(synthesis, "model_dump"):
        synthesis = synthesis.model_dump()

    prompt_path = Path("prompts/writer.txt")

    system_prompt = prompt_path.read_text(
        encoding="utf-8"
    )

    llm = get_llm()

    structured_llm = llm.with_structured_output(
        WriterOutput
    )

    response = structured_llm.invoke(
        f"""
{system_prompt}

Synthesized Knowledge:

{synthesis}
"""
    )

    return response