from pydantic import BaseModel

from tools.llm import get_llm


class TestOutput(BaseModel):
    answer: str


llm = get_llm()

structured_llm = llm.with_structured_output(
    TestOutput
)

response = structured_llm.invoke(
    "What is Agentic AI?"
)

print(response)