from pydantic import BaseModel
from agents.planner import ResearchPlan


class ResearchTask(BaseModel):
    source: str
    query: str


class ResearchTaskList(BaseModel):
    tasks: list[ResearchTask]


def source_selector_agent(plan: ResearchPlan) -> ResearchTaskList:

    tasks = []

    source_mapping = {
        "official_docs": plan.source_plan.official_docs,
        "research_papers": plan.source_plan.research_papers,
        "news": plan.source_plan.news,
        "industry_reports": plan.source_plan.industry_reports,
        "government_reports": plan.source_plan.government_reports,
        "blogs": plan.source_plan.blogs,
        "github": plan.source_plan.github,
    }

    for source, queries in source_mapping.items():

        for query in queries:

            tasks.append(
                ResearchTask(
                    source=source,
                    query=query
                )
            )

    return ResearchTaskList(tasks=tasks)