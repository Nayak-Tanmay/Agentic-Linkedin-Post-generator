from memory.ingestion.document_router import LoadingTask

from memory.loaders.pdf_loader import pdf_loader
from memory.loaders.docx_loader import docx_loader
from memory.loaders.url_loader import url_loader
from memory.loaders.github_loader import github_loader
from memory.loaders.codebase_loader import codebase_loader


# ==========================================================
# Loader Dispatcher
# ==========================================================

LOADER_MAP = {

    "pdf": pdf_loader,

    "docx": docx_loader,

    "url": url_loader,

    "github": github_loader,

    "codebase": codebase_loader,

}


def dispatch_loading_tasks(
    tasks: list[LoadingTask],
):

    documents = []

    for task in tasks:

        loader = LOADER_MAP.get(
            task.source_type
        )

        if loader is None:

            print(
                f"Skipping unsupported source: {task.source_type}"
            )

            continue

        print(
            f"Loading {task.source_type}: {task.source_path}"
        )

        loaded_docs = loader(
            task.source_path
        )

        documents.extend(
            loaded_docs
        )

    return documents