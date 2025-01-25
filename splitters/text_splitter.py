# Import libraries
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_experimental.text_splitter import SemanticChunker
# from langchain_openai.embeddings import OpenAIEmbeddings



# Split text recursively
def recursive_text_spliter(documents: List[Document], chunk_size: int, chunk_overlap: int):
    """
    Split text recursively.
    
    Args:
        documents: Input documents to split
        chunk_size: Chunk size
        chunk_overlap: Chunk overlap
        
    Returns:
        List of split documents
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False
    )
    return text_splitter.split_documents(documents)


# # Split text sematically
# def semantic_text_spliter(documents: Document, breakpoint_threshold_type: str="percentile"):
#     """
#     Split text semantically using Ollama embeddings.
    
#     Args:
#         documents: Input documents to split
#         breakpoint_threshold_type: Breakpoint threshold type
        
#     Returns:
#         List of split documents
#     """
#     embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
#     text_splitter = SemanticChunker(
#         embeddings=embeddings,
#         breakpoint_threshold_type=breakpoint_threshold_type
#     )
#     return text_splitter.split_documents(documents)


# # Split text by charcter
# def character_text_spliter(documents: Document, seperator: str = "\n\n", chunk_size: int = 1000, chunk_overlap: int = 200):
#     """
#     Split text by charcter.
    
#     Args:
#         documents: Input documents to split
#         chunk_size: Chunk size
#         chunk_overlap: Chunk overlap
        
#     Returns:
#         List of split documents
#     """
#     text_splitter = CharacterTextSplitter(
#         separator=seperator,
#         chunk_size=chunk_size,
#         chunk_overlap=chunk_overlap,
#         length_function=len,
#         is_separator_regex=False,
#     )
#     return text_splitter.split_documents(documents)