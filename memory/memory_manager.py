from memory.ingestion.upload_pipeline import (
    UploadRequest,
    validate_upload_request,
)

from memory.ingestion.document_router import (
    document_router,
)

from memory.loaders.loader_dispatcher import (
    dispatch_loading_tasks,
)

from memory.chunking.chunk_router import (
    chunk_documents,
)

from memory.vectordb.vector_store import (
    create_memory,
    load_memory,
    update_memory,
)


# ==========================================================
# Memory Manager
# ==========================================================

class MemoryManager:

    def __init__(self):

        self.vector_db = None

    # ------------------------------------------------------
    # Ingest Knowledge
    # ------------------------------------------------------

    def ingest(
        self,
        request: UploadRequest,
    ):

        validate_upload_request(request)

        print("\nRouting documents...")

        tasks = document_router(request)

        print(f"{len(tasks)} loading tasks created.")

        print("\nLoading documents...")

        documents = dispatch_loading_tasks(
            tasks
        )

        print(f"{len(documents)} documents loaded.")

        print("\nChunking documents...")

        chunks = chunk_documents(
            documents
        )

        print(f"{len(chunks)} chunks created.")

        if self.vector_db is None:

            print("\nCreating Memory...")

            self.vector_db = create_memory(
                chunks
            )

        else:

            print("\nUpdating Memory...")

            update_memory(
                self.vector_db,
                chunks,
            )

        print("\nMemory Updated Successfully.")

    # ------------------------------------------------------
    # Load Existing Memory
    # ------------------------------------------------------

    def connect(self):

        self.vector_db = load_memory()

        print(
            "\nConnected to existing memory."
        )

        return self.vector_db

    # ------------------------------------------------------
    # Get Memory Instance
    # ------------------------------------------------------

    def get_memory(self):

        if self.vector_db is None:

            self.connect()

        return self.vector_db


# ==========================================================
# Singleton Instance
# ==========================================================

memory_manager = MemoryManager()