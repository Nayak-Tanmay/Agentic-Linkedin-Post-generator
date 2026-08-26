from langchain_community.document_loaders import PyPDFLoader


def pdf_loader(file_path: str):

    loader = PyPDFLoader(file_path)

    documents = loader.load()

    print(f"Loaded {len(documents)} pages from PDF")

    return documents