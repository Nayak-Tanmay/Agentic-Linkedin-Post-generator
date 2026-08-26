from config.user_input import UserBrief

from agents.topic_analyzer import topic_analyzer_agent
from agents.planner import planner_agent
from agents.source_selector import source_selector_agent


def main():

    brief = UserBrief(
        topic="Oil war",
        goal="LinkedIn Post",
        audience="Common people",
        tone="Factual and impactful",
        research_depth="Deep",
        focus_area="Economic impact and latest trends",
        latest_information=True,
        preferred_sources=["AUTO"],
    )

    analysis = topic_analyzer_agent(brief)

    plan = planner_agent(
        brief,
        analysis
    )

    tasks = source_selector_agent(plan)

    print("=" * 80)
    print("RESEARCH TASKS")
    print("=" * 80)

    for i, task in enumerate(tasks.tasks, start=1):
        print(f"{i}. [{task.source}] {task.query}")


if __name__ == "__main__":
    main()