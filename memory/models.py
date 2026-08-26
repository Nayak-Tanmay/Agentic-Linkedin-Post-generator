from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# ==========================================================
# Uploaded Document
# ==========================================================

class MemoryDocument(BaseModel):

    document_id: str

    file_name: str

    file_path: str

    document_type: str

    source: str

    uploaded_at: datetime = Field(
        default_factory=datetime.utcnow
    )


# ==========================================================
# Metadata
# ==========================================================

class DocumentMetadata(BaseModel):

    page: Optional[int] = None

    section: Optional[str] = None

    author: Optional[str] = None

    title: Optional[str] = None

    language: Optional[str] = None

    url: Optional[str] = None

    tags: list[str] = Field(
        default_factory=list
    )


# ==========================================================
# Chunk
# ==========================================================

class DocumentChunk(BaseModel):

    chunk_id: str

    document_id: str

    content: str

    metadata: DocumentMetadata


# ==========================================================
# Embedded Chunk
# ==========================================================

class EmbeddedChunk(BaseModel):

    chunk: DocumentChunk

    embedding_model: str

    vector: list[float]


# ==========================================================
# Retrieved Chunk
# ==========================================================

class RetrievedChunk(BaseModel):

    chunk: DocumentChunk

    similarity_score: float

    source: str


# ==========================================================
# Retrieval Result
# ==========================================================

class RetrievalResult(BaseModel):

    query: str

    retrieved_chunks: list[RetrievedChunk]


# ==========================================================
# Corrective RAG Result
# ==========================================================

class CorrectiveRAGResult(BaseModel):

    query: str

    confidence_score: float

    needs_web_search: bool

    retrieved_chunks: list[RetrievedChunk]