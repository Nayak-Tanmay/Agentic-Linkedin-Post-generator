from config.user_input import UserBrief
from agents.topic_analyzer import TopicAnalysis
from graph.state import GraphState


def state_to_user_brief(
    state: GraphState,
) -> UserBrief:

    return UserBrief(
        topic=state["topic"],
        goal=state.get(
            "user_goal",
            "LinkedIn Post",
        ),
        audience=state.get(
            "target_audience",
            "General Professionals",
        ),
        tone=state.get(
            "tone",
            "Professional",
        ),
        research_depth=state.get(
            "research_depth",
            "Deep",
        ),
        focus_area=state.get(
            "focus_area",
            "",
        ),
        latest_information=state.get(
            "latest_information",
            True,
        ),
        preferred_sources=state.get(
            "preferred_sources",
            ["AUTO"],
        ),
        memory_context=state.get(
            "memory_context",
            "",
        ),
    )


def state_to_topic_analysis(
    state: GraphState,
) -> TopicAnalysis:

    return TopicAnalysis(
        topic_category=state.get(
            "topic_category",
            "",
        ),
        topic_subcategory=state.get(
            "topic_subcategory",
            "",
        ),
        topic_status=state.get(
            "topic_status",
            "",
        ),
        user_intent=state.get(
            "user_intent",
            "",
        ),
        content_type=state.get(
            "content_type",
            "",
        ),
        requires_latest_information=state.get(
            "latest_information",
            True,
        ),
        research_priority=state.get(
            "research_priority",
            "Medium",
        ),
        complexity=state.get(
            "complexity",
            "Medium",
        ),
    )
