# Agentic LinkedIn Post Generator

An Agentic AI system that performs research, evaluates information, generates LinkedIn posts, and iteratively improves them using multiple specialized agents.

The system combines:

- Agentic AI workflows
- Multi-source research
- Corrective RAG (CRAG)
- User-provided reference documents
- Conversation memory
- Knowledge ranking
- Conflict detection
- Iterative evaluation and revision
- LLM-based content generation

---

# Architecture Overview

The complete workflow is:

```text
                              ┌──────────────────────┐
                              │        USER          │
                              │                      │
                              │ Topic                │
                              │ Goal                 │
                              │ Audience             │
                              │ Tone                 │
                              │ Research Depth       │
                              │ Focus Area           │
                              │ Latest Information   │
                              └──────────┬───────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │ Optional Reference   │
                              │ Content              │
                              │                      │
                              │ PDF / DOCX / URL     │
                              │ GitHub / Codebase    │
                              └──────────┬───────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │    Memory / RAG      │
                              │                      │
                              │ Load → Chunk → Embed │
                              │ → Chroma Vector DB   │
                              └──────────┬───────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │   Topic Analyzer     │
                              └──────────┬───────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │   Research Planner   │
                              └──────────┬───────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │   Source Selector    │
                              └──────────┬───────────┘
                                         │
                                         ▼
                    ┌────────────────────────────────────────┐
                    │          RESEARCH DISPATCHER           │
                    └────────────────────┬───────────────────┘
                                         │
              ┌──────────────────────────┼──────────────────────────┐
              │                          │                          │
              ▼                          ▼                          ▼
       ┌─────────────┐            ┌─────────────┐            ┌─────────────┐
       │ News        │            │ Research    │            │ Government  │
       │ Researcher  │            │ Papers      │            │ Reports     │
       └─────────────┘            └─────────────┘            └─────────────┘
              │                          │                          │
              ├──────────────────────────┼──────────────────────────┤
              │                          │
              ▼                          ▼
       ┌─────────────┐            ┌─────────────┐
       │ GitHub      │            │ Official    │
       │ Researcher  │            │ Docs        │
       └─────────────┘            └─────────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │    Memory Research   │
                              │                      │
                              │ Retrieve → Grade     │
                              └──────────┬───────────┘
                                         │
                                  ┌──────┴──────┐
                                  │             │
                                  ▼             ▼
                             Sufficient     Insufficient
                                  │             │
                                  │             ▼
                                  │      ┌───────────────┐
                                  │      │ Missing Info  │
                                  │      └───────┬───────┘
                                  │              │
                                  │              ▼
                                  │      ┌───────────────┐
                                  │      │ Query         │
                                  │      │ Generator     │
                                  │      └───────┬───────┘
                                  │              │
                                  │              ▼
                                  │      External Research
                                  │              │
                                  └──────────────┬┘
                                                 │
                                                 ▼
                                  ┌────────────────────────┐
                                  │   Combined Findings    │
                                  └────────────┬───────────┘
                                               │
                                               ▼
                                  ┌────────────────────────┐
                                  │   Trust Ranking        │
                                  └────────────┬───────────┘
                                               │
                                               ▼
                                  ┌────────────────────────┐
                                  │   Duplicate Removal    │
                                  └────────────┬───────────┘
                                               │
                                               ▼
                                  ┌────────────────────────┐
                                  │   Conflict Detection   │
                                  └────────────┬───────────┘
                                               │
                                               ▼
                                  ┌────────────────────────┐
                                  │ Knowledge Synthesizer  │
                                  └────────────┬───────────┘
                                               │
                                               ▼
                                  ┌────────────────────────┐
                                  │     Writer Agent       │
                                  └────────────┬───────────┘
                                               │
                                               ▼
                                  ┌────────────────────────┐
                                  │    LinkedIn Draft      │
                                  └────────────┬───────────┘
                                               │
                                               ▼
                                  ┌────────────────────────┐
                                  │    Evaluator Agent     │
                                  └────────────┬───────────┘
                                               │
                                               ▼
                                  ┌────────────────────────┐
                                  │     Decision Agent     │
                                  └────────────┬───────────┘
                                               │
                              ┌────────────────┼────────────────┐
                              │                │                │
                              ▼                ▼                ▼
                            END             REVISE           RESEARCH
                              │                │                │
                              │                ▼                ▼
                              │          Reviser Agent    Research Gap
                              │                │                │
                              │                ▼                ▼
                              │           Evaluator      Query Generator
                              │                                 │
                              │                                 ▼
                              │                         Corrective Research
                              │                                 │
                              └─────────────────────────────────┘
                                               │
                                               ▼
                                  ┌────────────────────────┐
                                  │    FINAL LINKEDIN      │
                                  │         POST           │
                                  └────────────┬───────────┘
                                               │
                                               ▼
                                  ┌────────────────────────┐
                                  │ Conversation Memory    │
                                  │        Saved           │
                                  └────────────────────────┘
