from langchain_huggingface import HuggingFaceEmbeddings


# ==========================================================
# Embedding Model
# ==========================================================

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    model_kwargs={
        "device": "cpu",
    },
    encode_kwargs={
        "normalize_embeddings": True,
    },
)


# ==========================================================
# Embed Documents
# ==========================================================

def embed_documents(chunks):

    print(
        f"Generating embeddings for {len(chunks)} chunks..."
    )

    return embeddings, chunks