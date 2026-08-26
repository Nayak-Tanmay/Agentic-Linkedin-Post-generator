"""CLI helper for optional user reference content ingestion."""

from memory.ingestion.upload_pipeline import UploadRequest
from memory.memory_manager import memory_manager


def collect_and_ingest_reference_content() -> bool:
    """
    Ask the user if they want to add reference content.
    Returns True if content was ingested.
    """

    answer = input(
        "\nDo you want to add extra reference content? (y/n): "
    ).strip().lower()

    if answer != "y":
        return False

    request = UploadRequest()

    print(
        "\nReference types (you can add multiple, "
        "enter blank type to finish):"
    )
    print("  1. PDF")
    print("  2. DOCX")
    print("  3. URL")
    print("  4. GitHub repository")
    print("  5. Local file/folder")

    while True:

        choice = input(
            "\nReference type (1-5, or blank to finish): "
        ).strip()

        if not choice:
            break

        if choice == "1":
            path = input("PDF file path: ").strip()
            if path:
                request.pdfs.append(path)

        elif choice == "2":
            path = input("DOCX file path: ").strip()
            if path:
                request.docx_files.append(path)

        elif choice == "3":
            url = input("URL: ").strip()
            if url:
                request.urls.append(url)

        elif choice == "4":
            repo = input(
                "GitHub repository URL or owner/repo: "
            ).strip()
            if repo:
                request.github_repositories.append(repo)

        elif choice == "5":
            path = input(
                "Local file or folder path: "
            ).strip()
            if path:
                request.codebases.append(path)

        else:
            print("Invalid choice. Enter 1-5 or blank.")

    has_sources = any([
        request.pdfs,
        request.docx_files,
        request.ppt_files,
        request.markdown_files,
        request.text_files,
        request.csv_files,
        request.github_repositories,
        request.urls,
        request.codebases,
    ])

    if not has_sources:
        print("No reference content provided.")
        return False

    print("\nIngesting reference content into memory...")

    memory_manager.ingest(request)

    print("Reference content ingested successfully.")

    return True
