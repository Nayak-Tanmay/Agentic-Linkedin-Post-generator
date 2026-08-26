from langchain_community.document_loaders import WebBaseLoader


def url_loader(url: str):

    loader = WebBaseLoader(url)

    documents = loader.load()

    print(f"Loaded URL: {url}")

    return documents