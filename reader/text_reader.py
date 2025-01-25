from langchain_community.document_loaders import TextLoader
from typing import Union, List
from langchain_core.documents import Document


def read_text(file_path: str, return_string: bool = False) -> Union[List[Document], str]:
    """
    Read the content of a text file using LangChain's TextLoader.
    
    Args:
        file_path: Path to the text file
        return_string: If True, returns the entire document as a single string.
                      If False, returns a list of LangChain Document objects (default)
    
    Returns:
        Either a string containing the entire document content (if return_string=True)
        or a list of LangChain Document objects (if return_string=False)
    
    Raises:
        Exception: If there's an error reading the file
    """
    try:
        loader = TextLoader(file_path)
        documents = loader.load()
        
        if return_string:
            # Combine all document page contents into a single string
            return "\n".join(doc.page_content for doc in documents)
        
        return documents
    except Exception as e:
        print(f"Error in read_text: {str(e)}")
        raise