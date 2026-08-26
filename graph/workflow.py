from langgraph.graph import StateGraph, END

from graph.state import GraphState
from graph.helpers import (
    state_to_user_brief,
    state_to_topic_analysis,
)

from agents.topic_analyzer import topic_analyzer_agent
from agents.planner import planner_agent
from agents.source_selector import (
    source_selector_agent,
    ResearchTask,
)
from agents.research_pipeline import (
    limit_research_tasks,
    run_research_stage,
)
from config.research_limits import MAX_CORRECTIVE_QUERIES
from agents.research_aggregator import aggregate_findings
from agents.knowledge_ranking import rank_findings_by_trust
from agents.duplicate_removal import remove_duplicates
from agents.conflict_detection import detect_conflicts
from agents.knowledge_synthesizer import (
    knowledge_synthesizer_agent,
)
from agents.research_models import ResearchFinding
from agents.writer import writer_agent
from agents.evaluator import evaluator_agent
from agents.reviser import reviser_agent
from agents.decision import decision_agent
from agents.research_gap import research_gap_agent
from agents.query_generator import query_generator_agent


# =====================================================
# Topic Analyzer Node
# =====================================================

def topic_analyzer_node(state: GraphState):

    print("\n[TOPIC ANALYZER NODE]")

    brief = state_to_user_brief(state)

    analysis = topic_analyzer_agent(brief)

    return {
        "topic_category": analysis.topic_category,
        "topic_subcategory": analysis.topic_subcategory,
        "topic_status": analysis.topic_status,
        "user_intent": analysis.user_intent,
        "content_type": analysis.content_type,
        "research_priority": analysis.research_priority,
        "complexity": analysis.complexity,
    }


# =====================================================
# Planner Node
# =====================================================

def planner_node(state: GraphState):

    print("\n[PLANNER NODE]")

    brief = state_to_user_brief(state)
    analysis = state_to_topic_analysis(state)

    plan = planner_agent(brief, analysis)

    return {
        "research_plan": plan.model_dump(),
        "search_queries": plan.search_queries,
        "research_objectives": plan.research_objectives,
        "expected_sections": plan.expected_sections,
    }


# =====================================================
# Source Selector Node
# =====================================================

def source_selector_node(state: GraphState):

    print("\n[SOURCE SELECTOR NODE]")

    from agents.planner import ResearchPlan

    plan = ResearchPlan(**state["research_plan"])

    result = source_selector_agent(plan)

    limited = limit_research_tasks(
        result,
        state.get("research_depth", "Medium"),
    )

    active_sources = sorted(
        {t.source for t in limited.tasks}
    )

    print(
        f"\nGenerated {len(limited.tasks)} "
        f"research tasks across "
        f"{len(active_sources)} sources"
    )

    return {
        "research_tasks": [
            t.model_dump() for t in limited.tasks
        ],
        "sources_to_use": active_sources,
    }


# =====================================================
# Multi-Source Research Node
# =====================================================

def multi_source_research_node(state: GraphState):

    print("\n[MULTI-SOURCE RESEARCH NODE]")

    tasks: list[ResearchTask] = []

    for t in state.get("research_tasks", []):
        tasks.append(ResearchTask(**t))

    searched = set(
        state.get("searched_queries", [])
    )

    if not tasks and not state.get(
        "additional_search_queries", []
    ):

        print("\nNo new research tasks.")

        return {}

    # Gap-fill queries from decision loop
    for query in state.get(
        "additional_search_queries", []
    ):

        if query not in searched:

            tasks.append(
                ResearchTask(
                    source="news",
                    query=query,
                )
            )

    tasks = [
        t for t in tasks
        if t.query not in searched
    ]

    if not tasks:

        print("\nNo new research tasks.")

        return {}

    if state.get("additional_search_queries"):

        from agents.research_dispatcher import (
            dispatch_research_tasks,
        )

        new_findings = dispatch_research_tasks(
            tasks,
            max_tasks=MAX_CORRECTIVE_QUERIES,
        )

    else:

        new_findings = run_research_stage(
            topic=state["topic"],
            tasks=tasks,
            research_depth=state.get(
                "research_depth",
                "Medium",
            ),
        )

    existing = [
        ResearchFinding(**f)
        for f in state.get(
            "research_findings", []
        )
    ]

    all_findings = existing + new_findings

    return {
        "research_findings": [
            f.model_dump() for f in all_findings
        ],
        "searched_queries": list(searched) + [
            t.query for t in tasks
        ],
        "additional_search_queries": [],
        "research_tasks": [],
    }


# =====================================================
# Research Aggregator Node
# =====================================================

def research_aggregator_node(state: GraphState):

    print("\n[RESEARCH AGGREGATOR NODE]")

    findings = [
        ResearchFinding(**f)
        for f in state.get(
            "research_findings", []
        )
    ]

    aggregated = aggregate_findings(findings)

    return {
        "aggregated_findings": [
            f.model_dump() for f in aggregated
        ],
    }


# =====================================================
# Knowledge Ranking Node
# =====================================================

def knowledge_ranking_node(state: GraphState):

    print("\n[KNOWLEDGE RANKING NODE]")

    findings = [
        ResearchFinding(**f)
        for f in state.get(
            "aggregated_findings", []
        )
    ]

    ranked = rank_findings_by_trust(findings)

    return {
        "ranked_findings": [
            f.model_dump() for f in ranked
        ],
    }


# =====================================================
# Duplicate Removal Node
# =====================================================

def duplicate_removal_node(state: GraphState):

    print("\n[DUPLICATE REMOVAL NODE]")

    findings = [
        ResearchFinding(**f)
        for f in state.get(
            "ranked_findings", []
        )
    ]

    unique = remove_duplicates(findings)

    print(
        f"Removed "
        f"{len(findings) - len(unique)} "
        f"duplicates"
    )

    return {
        "deduplicated_findings": [
            f.model_dump() for f in unique
        ],
    }


# =====================================================
# Conflict Detection Node
# =====================================================

def conflict_detection_node(state: GraphState):

    print("\n[CONFLICT DETECTION NODE]")

    findings = [
        ResearchFinding(**f)
        for f in state.get(
            "deduplicated_findings", []
        )
    ]

    marked, conflicts = detect_conflicts(
        findings
    )

    if conflicts:

        print(
            f"Detected {len(conflicts)} "
            f"conflicts"
        )

    return {
        "deduplicated_findings": [
            f.model_dump() for f in marked
        ],
        "research_conflicts": [
            c.model_dump() for c in conflicts
        ],
    }


# =====================================================
# Knowledge Synthesizer Node
# =====================================================

def knowledge_synthesizer_node(state: GraphState):

    print("\n[KNOWLEDGE SYNTHESIZER NODE]")

    findings = [
        ResearchFinding(**f)
        for f in state.get(
            "deduplicated_findings", []
        )
    ]

    from agents.research_models import (
        ResearchConflict,
    )

    conflicts = [
        ResearchConflict(**c)
        for c in state.get(
            "research_conflicts", []
        )
    ]

    synthesis = knowledge_synthesizer_agent(
        findings,
        conflicts,
    )

    research_notes = (
        f"Topic: {synthesis.topic_summary}\n\n"
        f"Key Insights: "
        f"{synthesis.key_insights}\n\n"
        f"Statistics: "
        f"{synthesis.important_statistics}\n\n"
        f"Trends: {synthesis.future_trends}\n\n"
        f"Controversies: "
        f"{synthesis.controversies}"
    )

    return {
        "synthesized_knowledge":
            synthesis.model_dump(),
        "research_notes": research_notes,
    }


# =====================================================
# Writer Node
# =====================================================

def writer_node(state: GraphState):

    print("\n[WRITER NODE]")

    draft = writer_agent(
        state["synthesized_knowledge"]
    )

    return {
        "draft_post": draft.linkedin_post,
    }


# =====================================================
# Evaluator Node
# =====================================================

def evaluator_node(state: GraphState):

    print("\n[EVALUATOR NODE]")

    evaluation = evaluator_agent(
        state["draft_post"]
    )

    return {
        "evaluation":
            evaluation.model_dump(),
    }


# =====================================================
# Decision Node
# =====================================================

def decision_node(state: GraphState):

    print("\n[DECISION NODE]")

    decision = decision_agent(
        state["evaluation"]
    )

    print(f"Decision: {decision}")

    return {"decision": decision}


# =====================================================
# Reviser Node
# =====================================================

def reviser_node(state: GraphState):

    print("\n[REVISER NODE]")

    revision = reviser_agent(
        state["draft_post"],
        state["evaluation"],
    )

    return {
        "draft_post": revision.revised_post,
        "iteration_count":
            state["iteration_count"] + 1,
    }


# =====================================================
# Research Gap Node
# =====================================================

def research_gap_node(state: GraphState):

    print("\n[RESEARCH GAP NODE]")

    result = research_gap_agent(
        state["draft_post"],
        state["evaluation"],
    )

    return {
        "research_gaps": result.research_gaps,
    }


# =====================================================
# Query Generator Node
# =====================================================

def query_generator_node(state: GraphState):

    print("\n[QUERY GENERATOR NODE]")

    result = query_generator_agent(
        state["topic"],
        state["research_gaps"],
    )

    return {
        "additional_search_queries":
            result.additional_search_queries,
    }


# =====================================================
# Router
# =====================================================

def route_decision(state: GraphState):

    if (
        state["iteration_count"]
        >= state["max_iterations"]
    ):
        print(
            "\nMaximum iterations reached."
        )
        return "end"

    return state["decision"]


# =====================================================
# Graph Builder
# =====================================================

builder = StateGraph(GraphState)


# =====================================================
# Register Nodes
# =====================================================

builder.add_node(
    "topic_analyzer",
    topic_analyzer_node,
)
builder.add_node("planner", planner_node)
builder.add_node(
    "source_selector",
    source_selector_node,
)
builder.add_node(
    "multi_source_research",
    multi_source_research_node,
)
builder.add_node(
    "research_aggregator",
    research_aggregator_node,
)
builder.add_node(
    "knowledge_ranking",
    knowledge_ranking_node,
)
builder.add_node(
    "duplicate_removal",
    duplicate_removal_node,
)
builder.add_node(
    "conflict_detection",
    conflict_detection_node,
)
builder.add_node(
    "knowledge_synthesizer",
    knowledge_synthesizer_node,
)
builder.add_node("writer", writer_node)
builder.add_node("evaluator", evaluator_node)
builder.add_node("decision", decision_node)
builder.add_node("reviser", reviser_node)
builder.add_node(
    "research_gap",
    research_gap_node,
)
builder.add_node(
    "query_generator",
    query_generator_node,
)


# =====================================================
# Entry Point
# =====================================================

builder.set_entry_point("topic_analyzer")


# =====================================================
# Main Flow
# =====================================================

builder.add_edge(
    "topic_analyzer", "planner"
)
builder.add_edge(
    "planner", "source_selector"
)
builder.add_edge(
    "source_selector",
    "multi_source_research",
)
builder.add_edge(
    "multi_source_research",
    "research_aggregator",
)
builder.add_edge(
    "research_aggregator",
    "knowledge_ranking",
)
builder.add_edge(
    "knowledge_ranking",
    "duplicate_removal",
)
builder.add_edge(
    "duplicate_removal",
    "conflict_detection",
)
builder.add_edge(
    "conflict_detection",
    "knowledge_synthesizer",
)
builder.add_edge(
    "knowledge_synthesizer", "writer"
)
builder.add_edge("writer", "evaluator")
builder.add_edge("evaluator", "decision")


# =====================================================
# Revision Loop
# =====================================================

builder.add_edge("reviser", "evaluator")


# =====================================================
# Research Loop
# =====================================================

builder.add_edge(
    "research_gap", "query_generator"
)
builder.add_edge(
    "query_generator",
    "multi_source_research",
)


# =====================================================
# Conditional Routing
# =====================================================

builder.add_conditional_edges(
    "decision",
    route_decision,
    {
        "end": END,
        "revise": "reviser",
        "research": "research_gap",
    },
)


# =====================================================
# Compile
# =====================================================

workflow = builder.compile()
