from langchain_text_splitters import RecursiveCharacterTextSplitter


# ==========================================================
# Chunk Router
# ==========================================================

def chunk_documents(
    documents,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    chunks = splitter.split_documents(
        documents
    )

    print(
        f"Created {len(chunks)} chunks."
    )

    return chunks