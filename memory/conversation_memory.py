"""Simple persistent conversation memory (JSON)."""

import json
from datetime import datetime, timezone
from pathlib import Path

from config.user_input import UserBrief

MEMORY_FILE = Path("memory/conversation_store.json")
MAX_STORED_INTERACTIONS = 50


def _load_store() -> dict:

    if not MEMORY_FILE.exists():
        return {"interactions": []}

    try:
        return json.loads(
            MEMORY_FILE.read_text(encoding="utf-8")
        )
    except (json.JSONDecodeError, OSError):
        return {"interactions": []}


def _save_store(store: dict) -> None:

    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    MEMORY_FILE.write_text(
        json.dumps(store, indent=2),
        encoding="utf-8",
    )


def _topic_overlap_score(
    topic_a: str,
    topic_b: str,
) -> float:

    words_a = set(topic_a.lower().split())
    words_b = set(topic_b.lower().split())

    if not words_a or not words_b:
        return 0.0

    overlap = words_a & words_b

    return len(overlap) / max(len(words_a), len(words_b))


def get_relevant_memories(
    topic: str,
    limit: int = 5,
) -> list[dict]:

    store = _load_store()
    interactions = store.get("interactions", [])

    scored = []

    for entry in interactions:
        score = _topic_overlap_score(
            topic,
            entry.get("topic", ""),
        )
        if score > 0:
            scored.append((score, entry))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [entry for _, entry in scored[:limit]]


def format_memories_for_prompt(
    memories: list[dict],
) -> str:

    if not memories:
        return ""

    lines = ["Relevant past interactions:"]

    for mem in memories:
        lines.append(
            f"- Topic: {mem.get('topic', '')} | "
            f"Audience: {mem.get('audience', '')} | "
            f"Tone: {mem.get('tone', '')} | "
            f"Depth: {mem.get('research_depth', '')}"
        )

        if mem.get("focus_area"):
            lines.append(
                f"  Focus: {mem['focus_area']}"
            )

        if mem.get("context_notes"):
            lines.append(
                f"  Context: {mem['context_notes']}"
            )

    return "\n".join(lines)


def save_interaction(
    user_brief: UserBrief,
    generated_post: str = "",
    context_notes: str = "",
) -> None:

    store = _load_store()

    entry = {
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "topic": user_brief.topic,
        "goal": user_brief.goal,
        "audience": user_brief.audience,
        "tone": user_brief.tone,
        "research_depth": user_brief.research_depth,
        "focus_area": user_brief.focus_area,
        "context_notes": context_notes,
        "post_preview": generated_post[:300],
    }

    store["interactions"].append(entry)

    store["interactions"] = store[
        "interactions"
    ][-MAX_STORED_INTERACTIONS:]

    _save_store(store)
