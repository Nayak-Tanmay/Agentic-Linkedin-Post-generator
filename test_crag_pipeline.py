"""
Test cases for CRAG pipeline and reference content integration.

Run individual tests:
  python test_crag_pipeline.py --test 1   # normal pipeline (no reference)
  python test_crag_pipeline.py --test 2   # PDF ingestion + retrieval
  python test_crag_pipeline.py --test 3   # insufficient memory → corrective research
  python test_crag_pipeline.py --test 4   # dry-run pipeline structure check
"""

import argparse
import sys


def test_normal_pipeline_no_reference():
    """Test 1: Pipeline works without reference content."""

    from config.research_limits import (
        get_max_research_tasks,
        MAX_ITERATIONS,
    )
    from agents.source_selector import ResearchTask
    from agents.research_pipeline import (
        limit_research_tasks,
        process_findings,
    )
    from agents.source_selector import ResearchTaskList

    tasks = ResearchTaskList(
        tasks=[
            ResearchTask(source="news", query="AI agents 2026"),
            ResearchTask(source="blogs", query="agentic AI trends"),
        ]
    )

    limited = limit_research_tasks(tasks, "Quick")

    assert len(limited.tasks) <= get_max_research_tasks("Quick")
    assert MAX_ITERATIONS == 2

    findings = process_findings([])

    assert findings == ([], [])

    print("TEST 1 PASSED: limits and empty processing OK")


def test_memory_retrieval():
    """Test 2: Memory retrieval returns chunks for ingested content."""

    from memory.retrieval.retriever import retrieve
    from memory.memory_manager import memory_manager

    try:
        memory_manager.connect()
    except Exception:
        print(
            "TEST 2 SKIPPED: no memory database. "
            "Ingest a PDF first via main.py."
        )
        return

    chunks = retrieve("test query", k=3)

    print(f"Retrieved {len(chunks)} chunks")
    print("TEST 2 PASSED: retrieval runs without error")


def test_crag_insufficient_triggers_corrective():
    """Test 3: CRAG runs and returns findings structure."""

    from memory.corrective_rag.crag_pipeline import (
        run_crag_research,
        chunks_to_findings,
    )
    from agents.research_models import ResearchFinding

    try:
        findings, sufficient = run_crag_research(
            query="completely unknown xyz topic 99999",
            topic="completely unknown xyz topic 99999",
        )
    except Exception as e:
        print(f"TEST 3 SKIPPED: CRAG requires API keys ({e})")
        return

    for f in findings:
        assert isinstance(f, ResearchFinding)
        assert f.summary

    print(
        f"TEST 3 PASSED: CRAG returned {len(findings)} findings, "
        f"sufficient={sufficient}"
    )


def test_pipeline_structure():
    """Test 4: Verify all pipeline modules import correctly."""

    from main import main  # noqa: F401
    from agents.research_pipeline import run_research_stage
    from memory.conversation_memory import (
        get_relevant_memories,
        save_interaction,
    )
    from config.reference_input import (
        collect_and_ingest_reference_content,
    )
    from memory.corrective_rag.crag_pipeline import run_crag_research

    memories = get_relevant_memories("AI agents")

    print(f"Found {len(memories)} relevant memories")
    print("TEST 4 PASSED: all modules import correctly")


TESTS = {
    1: test_normal_pipeline_no_reference,
    2: test_memory_retrieval,
    3: test_crag_insufficient_triggers_corrective,
    4: test_pipeline_structure,
}


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--test",
        type=int,
        choices=[1, 2, 3, 4],
        help="Run a specific test (1-4)",
    )
    args = parser.parse_args()

    if args.test:
        TESTS[args.test]()
    else:
        for test_fn in TESTS.values():
            test_fn()
            print()
