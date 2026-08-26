"""
Test memory retrieval and CRAG grading.

Usage:
  python test_memory.py
  python test_memory.py "your query here"
"""

import sys

from memory.retrieval.retriever import retrieve
from memory.corrective_rag.corrective_rag import grade_retrieval
from memory.corrective_rag.crag_pipeline import run_crag_research


query = sys.argv[1] if len(sys.argv) > 1 else "what is curve settings"

print(f"\nQuery: {query}\n")

chunks = retrieve(query)
print(f"Retrieved {len(chunks)} chunks.\n")

if chunks:
    result = grade_retrieval(query, chunks)
    print("Grade:", result.model_dump())

print("\n--- Full CRAG run ---\n")

findings, sufficient = run_crag_research(query)
print(f"Sufficient: {sufficient}")
print(f"Findings: {len(findings)}")
