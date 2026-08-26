from dataclasses import dataclass, field


@dataclass
class UserBrief:
    topic: str
    goal: str
    audience: str
    tone: str
    research_depth: str
    focus_area: str
    latest_information: bool
    preferred_sources: list[str]
    memory_context: str = field(default_factory=str)


def collect_user_brief() -> UserBrief:

    print("=" * 50)
    print(" LinkedIn AI Research Assistant ")
    print("=" * 50)

    topic = input("Topic: ").strip()

    goal = input(
        "Goal (LinkedIn Post/Blog/Twitter) [LinkedIn Post]: "
    ).strip() or "LinkedIn Post"

    audience = input(
        "Target Audience [General Professionals]: "
    ).strip() or "General Professionals"

    tone = input(
        "Tone (Professional/Casual/Storytelling) [Professional]: "
    ).strip() or "Professional"

    research_depth = input(
        "Research Depth (Quick/Medium/Deep) [Deep]: "
    ).strip() or "Deep"

    focus_area = input(
        "Focus Area (Optional): "
    ).strip()

    latest = input(
        "Use Latest Information? (y/n) [y]: "
    ).strip().lower()

    latest_information = latest != "n"

    preferred = input(
        "Preferred Sources (comma separated / blank for Auto): "
    ).strip()

    if preferred:

        preferred_sources = [
            x.strip()
            for x in preferred.split(",")
        ]

    else:

        preferred_sources = ["AUTO"]

    from memory.conversation_memory import (
        get_relevant_memories,
        format_memories_for_prompt,
    )

    relevant = get_relevant_memories(topic)

    memory_context = format_memories_for_prompt(
        relevant
    )

    if memory_context:
        print(
            f"\nLoaded {len(relevant)} "
            "relevant past interaction(s)."
        )

    return UserBrief(
        topic=topic,
        goal=goal,
        audience=audience,
        tone=tone,
        research_depth=research_depth,
        focus_area=focus_area,
        latest_information=latest_information,
        preferred_sources=preferred_sources,
        memory_context=memory_context,
    )
