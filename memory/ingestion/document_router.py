from dataclasses import dataclass

from memory.ingestion.upload_pipeline import UploadRequest


# ==========================================================
# Loading Task
# ==========================================================

@dataclass
class LoadingTask:

    source_type: str

    source_path: str


# ==========================================================
# Document Router
# ==========================================================

def document_router(
    request: UploadRequest,
) -> list[LoadingTask]:

    tasks = []

    # ---------------- PDF ----------------

    for pdf in request.pdfs:

        tasks.append(
            LoadingTask(
                source_type="pdf",
                source_path=pdf,
            )
        )

    # ---------------- DOCX ----------------

    for doc in request.docx_files:

        tasks.append(
            LoadingTask(
                source_type="docx",
                source_path=doc,
            )
        )

    # ---------------- PPT ----------------

    for ppt in request.ppt_files:

        tasks.append(
            LoadingTask(
                source_type="ppt",
                source_path=ppt,
            )
        )

    # ---------------- MARKDOWN ----------------

    for md in request.markdown_files:

        tasks.append(
            LoadingTask(
                source_type="markdown",
                source_path=md,
            )
        )

    # ---------------- TEXT ----------------

    for txt in request.text_files:

        tasks.append(
            LoadingTask(
                source_type="text",
                source_path=txt,
            )
        )

    # ---------------- CSV ----------------

    for csv in request.csv_files:

        tasks.append(
            LoadingTask(
                source_type="csv",
                source_path=csv,
            )
        )

    # ---------------- URL ----------------

    for url in request.urls:

        tasks.append(
            LoadingTask(
                source_type="url",
                source_path=url,
            )
        )

    # ---------------- GITHUB ----------------

    for repo in request.github_repositories:

        tasks.append(
            LoadingTask(
                source_type="github",
                source_path=repo,
            )
        )

    # ---------------- CODEBASE ----------------

    for folder in request.codebases:

        tasks.append(
            LoadingTask(
                source_type="codebase",
                source_path=folder,
            )
        )

    return tasks