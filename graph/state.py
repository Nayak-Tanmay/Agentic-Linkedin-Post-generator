from typing import TypedDict


class GraphState(TypedDict):

    # ---------------- USER BRIEF ---------------- #

    topic: str

    user_goal: str

    target_audience: str

    tone: str

    research_depth: str

    focus_area: str

    latest_information: bool

    preferred_sources: list[str]

    memory_context: str


    # ---------------- TOPIC ANALYSIS ---------------- #

    topic_category: str

    topic_subcategory: str

    topic_status: str

    user_intent: str

    content_type: str

    research_priority: str

    complexity: str


    # ---------------- PLANNING ---------------- #

    selected_sources: list[str]

    sources_to_use: list[str]

    search_queries: list[str]

    research_plan: dict

    research_tasks: list[dict]

    research_objectives: list[str]

    expected_sections: list[str]


    # ---------------- RESEARCH ---------------- #

    github_research: list

    paper_research: list

    docs_research: list

    research_findings: list[dict]

    aggregated_findings: list[dict]

    ranked_findings: list[dict]

    deduplicated_findings: list[dict]

    research_conflicts: list[dict]

    research_notes: str

    synthesized_knowledge: dict

    # ---------------- WRITING ---------------- #

    draft_post: str

    evaluation: dict

    research_gaps: list[str]

    additional_search_queries: list[str]

    searched_queries: list[str]

    decision: str

    final_post: str

    iteration_count: int

    max_iterations: int
