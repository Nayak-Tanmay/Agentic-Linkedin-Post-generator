from pathlib import Path

from pydantic import BaseModel, Field

from config.user_input import UserBrief
from agents.topic_analyzer import TopicAnalysis
from tools.llm import get_llm


# ==========================================================
# Output Models
# ==========================================================

class SourcePlan(BaseModel):
    official_docs: list[str] = Field(default_factory=list)
    research_papers: list[str] = Field(default_factory=list)
    news: list[str] = Field(default_factory=list)
    industry_reports: list[str] = Field(default_factory=list)
    government_reports: list[str] = Field(default_factory=list)
    blogs: list[str] = Field(default_factory=list)
    github: list[str] = Field(default_factory=list)


class ResearchPlan(BaseModel):
    research_objectives: list[str]
    source_plan: SourcePlan
    expected_sections: list[str]
    search_queries: list[str]


# ==========================================================
# Planner Agent
# ==========================================================

def planner_agent(
    user_brief: UserBrief,
    topic_analysis: TopicAnalysis,
) -> ResearchPlan:

    prompt_path = Path("prompts/planner.txt")

    system_prompt = prompt_path.read_text(
        encoding="utf-8"
    )

    llm = get_llm()

    structured_llm = llm.with_structured_output(
        ResearchPlan
    )

    prompt = f"""
{system_prompt}

=========================
USER BRIEF
=========================

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

Preferred Sources:
{", ".join(user_brief.preferred_sources)}

=========================
TOPIC ANALYSIS
=========================

Topic Category:
{topic_analysis.topic_category}

Topic Subcategory:
{topic_analysis.topic_subcategory}

Topic Status:
{topic_analysis.topic_status}

User Intent:
{topic_analysis.user_intent}

Content Type:
{topic_analysis.content_type}

Research Priority:
{topic_analysis.research_priority}

Complexity:
{topic_analysis.complexity}

Requires Latest Information:
{topic_analysis.requires_latest_information}
"""

    if user_brief.memory_context:
        prompt += f"""

=========================
RELEVANT PAST CONTEXT
=========================

{user_brief.memory_context}
"""

    response = structured_llm.invoke(prompt)

    return response