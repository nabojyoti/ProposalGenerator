import os
import traceback
from typing import Any, List
from langchain_core.documents import Document
from downloader.file_download import html_downloader
from reader.pdf_reader import read_pdf
from reader.html_reader import read_html
from reader.text_reader import read_text
from splitters.text_splitter import recursive_text_spliter
from extractor.details_extractor import extract_letter_details
from vector_datbase.chroma_db import ChromaDB
from utils.formatter import create_uuid



# Register details of NGO
def register_ngo(configs: dict[str, Any]):
    """Register NGO details and proposal letters in vector databases.

    Args:
        configs: Configuration containing:
            - name: Name of the NGO
            - ngo_details: List of file paths of NGO details
            - proposal_letters: List of file paths of proposal letters

    Returns:
        dict: Status of the registration process
    """
    try:
        # Create an identifier for the NGO
        index_name = str(create_uuid(configs["name"]))
        # Read and store NGO details in vector database
        docs: List[Document] = []
        for file_path in configs["ngo_details"]:
            data = []
            if file_path.endswith('.pdf'):
                data = read_pdf(file_path)
            elif file_path.endswith('.txt'):
                data = read_text(file_path)
            elif file_path.endswith('.html'):
                filename = html_downloader(file_path)
                if filename is None:
                    continue
                data = read_html(filename)
            else:
                raise ValueError(f"Unsupported file format: {file_path}")
            docs.extend(data)
        if len(docs) == 0:
            raise FileNotFoundError("Files related to the NGO details are not found!")
        docs = recursive_text_spliter(docs, 1000, 200)
        details_db = ChromaDB(collection_name=index_name + '_details')
        details_db.insert(docs)
        # Read and store proposal letters in vector database
        proposal_docs: List[Document] = []
        for file_path in configs["proposal_letters"]:
            if file_path.endswith('.pdf'):
                data = read_pdf(file_path)
            elif file_path.endswith('.txt'):
                data = read_text(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_path}")
            proposal_docs.extend(data)
        if len(proposal_docs) == 0:
            raise ValueError("No proposal letters are provided!")
        proposal_docs = recursive_text_spliter(proposal_docs, 1000, 200)
        letters_db = ChromaDB(collection_name=index_name + '_letters')
        letters_db.insert(proposal_docs)
        # Read and store proposal letters metadata in vector database
        meta_docs: List[Document] = []
        for file_path in configs["proposal_letters"]:
            if file_path.endswith('.pdf'):
                data = read_pdf(file_path, return_string=True)
            elif file_path.endswith('.txt'):
                data = read_text(file_path, return_string=True)
            else:
                raise ValueError(f"Unsupported file format: {file_path}")
            extracted_data = extract_letter_details(data)
            document = Document(
                page_content=extracted_data['topic'],
                metadata={"timeline": extracted_data['timeline'], "budget": extracted_data['budget']}
            )
            meta_docs.append(document)
        if len(meta_docs) == 0:
            raise ValueError("No proposal letters are provided!")
        meta_db = ChromaDB(collection_name=index_name + '_meta')
        meta_db.insert(meta_docs)
        # Return success message
        return {"status": "success", "message": "Registration completed successfully!"}
    except Exception as e:
        # Return error message
        return {"status": "error", "message": traceback.format_exc()}