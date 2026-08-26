from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader


def codebase_loader(folder_path: str):

    loader = DirectoryLoader(
        folder_path,
        glob="**/*",
        loader_cls=TextLoader,
        silent_errors=True,
    )

    documents = loader.load()

    print(f"Loaded {len(documents)} code files")

    return documents