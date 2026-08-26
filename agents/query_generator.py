from pydantic import BaseModel

from tools.llm import get_llm


class QueryGeneratorOutput(BaseModel):

    additional_search_queries: list[str]


def query_generator_agent(
    topic: str,
    research_gaps: list[str],
    max_queries: int = 5,
):

    prompt = f"""
    You are a search strategist.

    Topic:

    {topic}

    Missing Information:

    {research_gaps}

    Generate highly specific search queries
    that can help fill these gaps.

    Queries should be:

    - Search engine friendly
    - Specific
    - Research oriented
    - Not duplicates

    Generate at most {max_queries} queries.
    """

    llm = get_llm()

    structured_llm = llm.with_structured_output(
        QueryGeneratorOutput
    )

    response = structured_llm.invoke(prompt)

    response.additional_search_queries = (
        response.additional_search_queries[:max_queries]
    )

    return response