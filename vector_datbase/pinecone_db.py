import os
import time
import getpass
from vector_datbase.pinecone_db import Pinecone as pc, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from typing import List, Dict


class Pinecone:
    """
    Class to manage interaction with Pinecone vector database using LangChain.
    """
    def __init__(self, index_name: str, pinecone_api_key: str = "", pinecone_env: str = "", model: str = "text-embedding-3-large"):
        """
        Initialize the Pinecone connection and set up the vector store.

        :param index_name: The name of the Pinecone index (table).
        :param pinecone_api_key: API key for Pinecone.
        :param pinecone_env: Pinecone environment (db) name.
        :param model: OpenAI embedding model to use. Defaults to "text-embedding-3-large".
        """
        os.environ["PINECONE_API_KEY"] = pinecone_api_key
        os.environ["PINECONE_ENV"] = pinecone_env

        # Initialize Pinecone
        pc.init(api_key=pinecone_api_key, environment=pinecone_env)

        # Create or retrieve index
        self.index_name = index_name
        existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]
        if index_name not in existing_indexes:
            pc.create_index(
                name=index_name,
                dimension=3072,  #NOTE: Assuming 3072-dimensional embeddings for OpenAI model
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )
            while not pc.describe_index(index_name).status["ready"]:
                time.sleep(1)
        self.index = pc.Index(index_name)

        # Set up embeddings and vector store
        self.embeddings = OpenAIEmbeddings(model=model)
        self.vector_store = PineconeVectorStore(index=self.index, embedding=self.embeddings)

    def insert(self, docs: List[Document]):
        """
        Embed and insert documents into the Pinecone vector database.

        :param docs: List of document strings to store.
        """
        try:
            ids = [f"doc-{i}" for i in range(len(docs))]
            self.vector_store.add_texts(docs, ids)
            print(f"Successfully inserted {len(docs)} documents into {self.index_name}")
        except Exception as e:
            print(f"Error while inserting documents into Pinecone: {e}")

    def query(self, query_text: str, top_k: int = 5, meta_only: bool = False):
        """
        Query the Pinecone index with a search query.

        :param query_text: Text to search for.
        :param top_k: Number of top results to retrieve.
        :return: List of query results with metadata.
        """
        try:
            results = self.vector_store.similarity_search(query_text, top_k=top_k)
            if meta_only:
                results = [result.metadata for result in results]
            else:
                results = [result.page_content for result in results]
            return results
        except Exception as e:
            print(f"Error while querying Pinecone: {e}")
            return []