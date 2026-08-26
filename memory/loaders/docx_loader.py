from langchain_community.document_loaders import Docx2txtLoader


def docx_loader(file_path: str):

    loader = Docx2txtLoader(file_path)

    documents = loader.load()

    print(f"Loaded DOCX: {file_path}")

    return documents