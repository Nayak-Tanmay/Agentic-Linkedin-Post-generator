from langchain_community.document_loaders import GitLoader


def github_loader(repo_path: str):

    loader = GitLoader(
        repo_path=repo_path,
        branch="main",
    )

    documents = loader.load()

    print(f"Loaded GitHub Repository")

    return documents