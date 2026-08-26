from agents.planner import planner_agent
from agents.writer import writer_agent
from agents.evaluator import evaluator_agent
from agents.reviser import reviser_agent
from agents.decision import decision_agent
from agents.research_gap import research_gap_agent
from agents.query_generator import query_generator_agent

from config.user_input import collect_user_brief
from config.reference_input import collect_and_ingest_reference_content
from config.research_limits import MAX_ITERATIONS, MAX_CORRECTIVE_QUERIES

from agents.topic_analyzer import topic_analyzer_agent

from agents.source_selector import (
    source_selector_agent,
    ResearchTask,
)

from agents.knowledge_synthesizer import knowledge_synthesizer_agent

from agents.research_pipeline import (
    limit_research_tasks,
    process_findings,
    run_research_stage,
)

from memory.conversation_memory import save_interaction


def main():

    # ======================================================
    # 1. COLLECT USER BRIEF
    # ======================================================

    print("\n" + "=" * 70)
    print("COLLECTING USER BRIEF")
    print("=" * 70)

    user_brief = collect_user_brief()

    print("\nUSER BRIEF")
    print(user_brief)


    # ======================================================
    # 1b. OPTIONAL REFERENCE CONTENT
    # ======================================================

    collect_and_ingest_reference_content()


    # ======================================================
    # 2. TOPIC ANALYZER
    # ======================================================

    print("\n" + "=" * 70)
    print("TOPIC ANALYZER")
    print("=" * 70)

    analysis = topic_analyzer_agent(user_brief)

    print(analysis.model_dump_json(indent=4))


    # ======================================================
    # 3. RESEARCH PLANNER
    # ======================================================

    print("\n" + "=" * 70)
    print("RESEARCH PLANNER")
    print("=" * 70)

    plan = planner_agent(user_brief, analysis)

    print(plan.model_dump_json(indent=4))


    # ======================================================
    # 4. SOURCE SELECTOR (with depth limits)
    # ======================================================

    print("\n" + "=" * 70)
    print("SOURCE SELECTOR")
    print("=" * 70)

    tasks = source_selector_agent(plan)
    tasks = limit_research_tasks(
        tasks,
        user_brief.research_depth,
    )

    print(f"\nResearch tasks created: {len(tasks.tasks)}")

    for i, task in enumerate(tasks.tasks, start=1):
        print(f"{i}. [{task.source}] {task.query}")


    # ======================================================
    # 5. RESEARCH (CRAG + external when needed)
    # ======================================================

    print("\n" + "=" * 70)
    print("RESEARCH STAGE")
    print("=" * 70)

    findings = run_research_stage(
        topic=user_brief.topic,
        tasks=tasks.tasks,
        research_depth=user_brief.research_depth,
    )

    print(f"\nRaw findings collected: {len(findings)}")


    # ======================================================
    # 6–9. PROCESS FINDINGS
    # ======================================================

    marked, conflicts = process_findings(findings)

    print(f"\nFinal findings: {len(marked)}")
    print(f"Conflicts detected: {len(conflicts)}")


    # ======================================================
    # 10. KNOWLEDGE SYNTHESIS
    # ======================================================

    print("\n" + "=" * 70)
    print("KNOWLEDGE SYNTHESIZER")
    print("=" * 70)

    synthesis = knowledge_synthesizer_agent(
        marked,
        conflicts,
    )

    print(synthesis.model_dump_json(indent=4))


    # ======================================================
    # 11. INITIAL WRITING
    # ======================================================

    print("\n" + "=" * 70)
    print("WRITER")
    print("=" * 70)

    draft = writer_agent(synthesis)
    current_post = draft.linkedin_post

    print("\nINITIAL LINKEDIN POST")
    print("-" * 70)
    print(current_post)


    # ======================================================
    # 12. INITIAL EVALUATION
    # ======================================================

    print("\n" + "=" * 70)
    print("INITIAL EVALUATION")
    print("=" * 70)

    current_evaluation = evaluator_agent(current_post)

    print(current_evaluation.model_dump_json(indent=4))


    # ======================================================
    # 13. ITERATIVE IMPROVEMENT LOOP
    # ======================================================

    iteration = 0

    while iteration < MAX_ITERATIONS:

        print("\n" + "=" * 70)
        print(f"ITERATION {iteration + 1}")
        print("=" * 70)

        decision = decision_agent(current_evaluation)

        print(f"\nDecision: {decision}")

        if decision == "end":
            print("\nTarget quality reached.")
            break

        elif decision == "revise":

            iteration += 1

            print(f"\nRevision Round {iteration}")

            revision = reviser_agent(
                current_post,
                current_evaluation,
            )

            current_post = revision.revised_post
            current_evaluation = evaluator_agent(current_post)

        elif decision == "research":

            iteration += 1

            print(f"\nResearch Round {iteration}")

            gap_result = research_gap_agent(
                current_post,
                current_evaluation.model_dump(),
            )

            print("\nRESEARCH GAPS")
            for gap in gap_result.research_gaps:
                print(f"- {gap}")

            query_result = query_generator_agent(
                user_brief.topic,
                gap_result.research_gaps,
                max_queries=MAX_CORRECTIVE_QUERIES,
            )

            queries = query_result.additional_search_queries

            print("\nNEW RESEARCH QUERIES")
            for query in queries:
                print(f"- {query}")

            gap_tasks = [
                ResearchTask(source="news", query=query)
                for query in queries
            ]

            from agents.research_dispatcher import (
                dispatch_research_tasks,
            )

            new_findings = dispatch_research_tasks(
                gap_tasks,
                max_tasks=MAX_CORRECTIVE_QUERIES,
            )

            print(f"\nNew findings: {len(new_findings)}")

            all_findings = marked + new_findings
            marked, conflicts = process_findings(all_findings)

            synthesis = knowledge_synthesizer_agent(
                marked,
                conflicts,
            )

            draft = writer_agent(synthesis)
            current_post = draft.linkedin_post
            current_evaluation = evaluator_agent(current_post)

        else:
            print(f"Unknown decision: {decision}")
            break

        print("\nUPDATED SCORE:")
        print(current_evaluation.overall_score)


    # ======================================================
    # 14. FINAL OUTPUT
    # ======================================================

    print("\n" + "=" * 70)
    print("FINAL LINKEDIN POST")
    print("=" * 70)
    print(current_post)


    # ======================================================
    # 15. FINAL EVALUATION
    # ======================================================

    print("\n" + "=" * 70)
    print("FINAL EVALUATION")
    print("=" * 70)
    print(current_evaluation.model_dump_json(indent=4))


    # ======================================================
    # 16. SAVE CONVERSATION MEMORY
    # ======================================================

    save_interaction(
        user_brief,
        generated_post=current_post,
    )


    # ======================================================
    # PIPELINE SUMMARY
    # ======================================================

    print("\n" + "=" * 70)
    print("PIPELINE COMPLETED")
    print("=" * 70)

    print(f"Topic              : {user_brief.topic}")
    print(f"Research findings  : {len(marked)}")
    print(f"Conflicts detected : {len(conflicts)}")
    print(f"Iterations used    : {iteration}")
    print(f"Final score        : {current_evaluation.overall_score}")


if __name__ == "__main__":
    main()
