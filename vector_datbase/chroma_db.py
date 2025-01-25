from uuid import uuid4
import chromadb
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from typing import List

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# Use the API key in your code
if openai_api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")


class ChromaDB:
    def __init__(self, collection_name: str, model_provider: str = 'openai'):
        if model_provider == 'openai':
            self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        else:
            raise ValueError(f"Unknown model provider: {model_provider}")
        self.persistent_client = chromadb.PersistentClient()
        collection = self.persistent_client.get_or_create_collection("collection_name")
        self.vector_store_from_client = Chroma(
            client=self.persistent_client,
            collection_name=collection_name,
            embedding_function=self.embeddings
        )
    
    def get_collections(self):
        return self.persistent_client.list_collections()
    
    def insert(self, docs: List[Document]):
        uuids = [str(uuid4()) for _ in range(len(docs))]
        self.vector_store_from_client.add_documents(documents=docs, ids=uuids)

    def query(self, query_text: str, top_k: int = 5):
        return self.vector_store_from_client.similarity_search(
                query_text,
                k=top_k
            )