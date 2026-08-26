from pathlib import Path

from pydantic import BaseModel, Field


class UploadRequest(BaseModel):

    pdfs: list[str] = Field(default_factory=list)

    docx_files: list[str] = Field(default_factory=list)

    ppt_files: list[str] = Field(default_factory=list)

    markdown_files: list[str] = Field(default_factory=list)

    text_files: list[str] = Field(default_factory=list)

    csv_files: list[str] = Field(default_factory=list)

    github_repositories: list[str] = Field(default_factory=list)

    urls: list[str] = Field(default_factory=list)

    codebases: list[str] = Field(default_factory=list)

def validate_upload_request(
    request: UploadRequest,
):

    all_sources = (
        request.pdfs
        + request.docx_files
        + request.ppt_files
        + request.markdown_files
        + request.text_files
        + request.csv_files
        + request.github_repositories
        + request.urls
        + request.codebases
    )

    if len(all_sources) == 0:

        raise ValueError(
            "At least one knowledge source must be provided."
        )

    return True