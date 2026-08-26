from graph.workflow import workflow


INITIAL_STATE = {
    # User Brief
    "topic": "Agentic AI",
    "user_goal": "LinkedIn Post",
    "target_audience": "General Professionals",
    "tone": "Professional",
    "research_depth": "Deep",
    "focus_area": "",
    "latest_information": True,
    "preferred_sources": ["AUTO"],

    # Topic Analysis (filled by topic_analyzer node)
    "topic_category": "",
    "topic_subcategory": "",
    "topic_status": "",
    "user_intent": "",
    "content_type": "",
    "research_priority": "",
    "complexity": "",

    # Planning
    "selected_sources": [],
    "sources_to_use": [],
    "search_queries": [],
    "research_plan": {},
    "research_tasks": [],
    "research_objectives": [],
    "expected_sections": [],

    # Research
    "github_research": [],
    "paper_research": [],
    "docs_research": [],
    "research_findings": [],
    "aggregated_findings": [],
    "ranked_findings": [],
    "deduplicated_findings": [],
    "research_conflicts": [],
    "research_notes": "",

    # Synthesis
    "synthesized_knowledge": {},

    # Writer
    "draft_post": "",

    # Evaluation
    "evaluation": {},

    # Research Loop
    "research_gaps": [],
    "additional_search_queries": [],
    "searched_queries": [],

    # Decision
    "decision": "",

    # Final Output
    "final_post": "",

    # Loop Control
    "iteration_count": 0,
    "max_iterations": 2,
}


result = workflow.invoke(INITIAL_STATE)

print("\n" + "=" * 50)
print("FINAL STATE")
print("=" * 50)

print(f"Sources used: {result.get('sources_to_use', [])}")
print(f"Findings: {len(result.get('research_findings', []))}")
print(f"Conflicts: {len(result.get('research_conflicts', []))}")
print(f"Decision: {result.get('decision', '')}")
print(f"\nDraft Post:\n{result.get('draft_post', '')}")
