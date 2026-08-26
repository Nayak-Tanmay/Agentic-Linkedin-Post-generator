from pydantic import BaseModel

from config.user_input import UserBrief
from tools.llm import get_llm


class TopicAnalysis(BaseModel):

    topic_category: str
    topic_subcategory: str
    topic_status: str

    user_intent: str
    content_type: str

    requires_latest_information: bool

    research_priority: str
    complexity: str


def topic_analyzer_agent(
    user_brief: UserBrief,
) -> TopicAnalysis:

    prompt = f"""
You are an expert AI Content Strategist.

Your job is NOT to generate search queries.

Understand the user's request.

USER INPUT

Topic:
{user_brief.topic}

Goal:
{user_brief.goal}

Audience:
{user_brief.audience}

Tone:
{user_brief.tone}

Research Depth:
{user_brief.research_depth}

Focus Area:
{user_brief.focus_area}

Latest Information:
{user_brief.latest_information}
"""

    if user_brief.memory_context:
        prompt += f"""

Relevant Past Context:
{user_brief.memory_context}
"""

    prompt += """

Determine

1. Topic Category
Examples:
Technology
Sports
Finance
Healthcare
Education
Politics
Entertainment

2. Topic Subcategory
The specific domain within the category.

Examples:

Technology -> Artificial Intelligence

Technology -> Cybersecurity

Sports -> Football

Sports -> Cricket

Finance -> Stock Market

Healthcare -> Biotechnology

3. Topic Status
(Evergreen / Ongoing / Upcoming Event / Completed Event / Historical)

4. User Intent

Examples:
- Educational
- Opinion
- Thought Leadership
- Tutorial
- Storytelling
- Marketing
- Research Summary

5. Best LinkedIn Content Type

Examples:
- Educational
- Trend Analysis
- Framework
- Opinion
- Comparison
- Listicle
- Case Study

6. Whether latest information is actually required.

7. Research Priority
(Low / Medium / High)

8. Complexity
(Low / Medium / High)


Return ONLY structured JSON.
"""

    llm = get_llm()

    structured_llm = llm.with_structured_output(
        TopicAnalysis
    )

    return structured_llm.invoke(prompt)