from langchain_community.document_loaders import UnstructuredHTMLLoader


def read_html(page_url: str):
    loader = UnstructuredHTMLLoader(page_url)
    data = loader.load()
    return data
