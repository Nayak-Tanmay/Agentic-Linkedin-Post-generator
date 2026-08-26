from memory.memory_manager import memory_manager


# ==========================================================
# Retrieve Relevant Chunks
# ==========================================================

def retrieve(
    query: str,
    k: int = 5,
):

    vector_db = memory_manager.get_memory()

    print(
        f"\nSearching Memory for: {query}"
    )

    results = vector_db.similarity_search(
        query,
        k=k,
    )

    print(
        f"Retrieved {len(results)} chunks."
    )

    return results