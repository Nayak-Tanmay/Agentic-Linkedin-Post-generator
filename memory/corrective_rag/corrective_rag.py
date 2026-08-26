from pydantic import BaseModel, Field

from tools.llm import get_llm


# ==========================================================
# Retrieval Grade
# ==========================================================

class RetrievalGrade(BaseModel):

    sufficient: bool = Field(
        description="Whether the retrieved context is sufficient to answer the user's query."
    )

    confidence: float = Field(
        description="Confidence score between 0 and 1."
    )

    reasoning: str = Field(
        description="Short explanation for the decision."
    )

    missing_information: list[str] = Field(
        default_factory=list,
        description="Important missing information required to fully answer the user's query."
    )


# ==========================================================
# Grade Retrieved Context
# ==========================================================

def grade_retrieval(
    query: str,
    retrieved_chunks,
) -> RetrievalGrade:

    context = "\n\n".join(
        chunk.page_content
        for chunk in retrieved_chunks
    )

    prompt = f"""
You are an expert Retrieval Quality Evaluator for a Corrective RAG system.

Your task is NOT to answer the user's question.

Your task is ONLY to evaluate whether the retrieved context is sufficient for another AI assistant to generate a high-quality answer.

IMPORTANT RULES

1. The answer DOES NOT have to appear word-for-word.

2. If the answer can be reasonably inferred from the retrieved context,
mark it as sufficient.

3. Only mark it as insufficient if important information required for answering the query is missing.

4. If insufficient, identify ONLY the missing information.
Do NOT generate new facts.

-----------------------------------------------------

USER QUERY

{query}

-----------------------------------------------------

RETRIEVED CONTEXT

{context}

-----------------------------------------------------

Return

1. sufficient (true/false)

2. confidence (0-1)

3. reasoning

4. missing_information

Examples

Query:
What is curve setting?

If the retrieved context explains the purpose,
methods and procedure of curve setting,
then it is sufficient even if there is no direct definition.

-----------------------------------------------------

Return structured JSON only.
"""

    llm = get_llm()

    structured_llm = llm.with_structured_output(
        RetrievalGrade
    )

    return structured_llm.invoke(prompt)