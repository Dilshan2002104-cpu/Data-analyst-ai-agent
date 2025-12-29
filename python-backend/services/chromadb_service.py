"""
ChromaDB Service for vector storage and semantic search
"""

import chromadb
from chromadb.config import Settings
import config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChromaDBService:
    def __init__(self):
        """Initialize ChromaDB client with persistent storage"""
        try:
            self.client = chromadb.PersistentClient(
                path=config.CHROMADB_PERSIST_DIR,
                settings=Settings(
                    anonymized_telemetry=False
                )
            )
            logger.info(f"ChromaDB initialized with persist directory: {config.CHROMADB_PERSIST_DIR}")
            
        except Exception as e:
            logger.error(f"Error initializing ChromaDB: {str(e)}")
            raise

    def create_collection(self, dataset_id):
        """
        Create or get a collection for a dataset
        
        Args:
            dataset_id (str): Unique identifier for the dataset
            
        Returns:
            Collection: ChromaDB collection object
        """
        try:
            collection_name = f"dataset_{dataset_id}"
            
            # Get or create collection
            collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"dataset_id": dataset_id}
            )
            
            logger.info(f"Collection created/retrieved: {collection_name}")
            return collection
            
        except Exception as e:
            logger.error(f"Error creating collection: {str(e)}")
            raise

    def add_documents(self, collection, documents, embeddings, metadatas=None, ids=None):
        """
        Add documents with embeddings to a collection
        
        Args:
            collection: ChromaDB collection
            documents (list): List of text documents
            embeddings (list): List of embedding vectors
            metadatas (list, optional): List of metadata dicts
            ids (list, optional): List of document IDs
            
        Returns:
            bool: Success status
        """
        try:
            if not ids:
                ids = [f"doc_{i}" for i in range(len(documents))]
            
            if not metadatas:
                metadatas = [{"index": i} for i in range(len(documents))]
            
            collection.add(
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Added {len(documents)} documents to collection")
            return True
            
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            raise

    def semantic_search(self, collection, query_embedding, top_k=5):
        """
        Perform semantic search using query embedding
        
        Args:
            collection: ChromaDB collection
            query_embedding (list): Query embedding vector
            top_k (int): Number of results to return
            
        Returns:
            dict: Search results with documents and metadata
        """
        try:
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )
            
            logger.info(f"Semantic search returned {len(results['documents'][0])} results")
            
            return {
                'documents': results['documents'][0],
                'metadatas': results['metadatas'][0],
                'distances': results['distances'][0]
            }
            
        except Exception as e:
            logger.error(f"Error performing semantic search: {str(e)}")
            raise

    def delete_collection(self, dataset_id):
        """
        Delete a collection for a dataset
        
        Args:
            dataset_id (str): Dataset identifier
            
        Returns:
            bool: Success status
        """
        try:
            collection_name = f"dataset_{dataset_id}"
            self.client.delete_collection(name=collection_name)
            
            logger.info(f"Collection deleted: {collection_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting collection: {str(e)}")
            return False

    def get_collection_count(self, collection):
        """
        Get the number of documents in a collection
        
        Args:
            collection: ChromaDB collection
            
        Returns:
            int: Number of documents
        """
        try:
            return collection.count()
        except Exception as e:
            logger.error(f"Error getting collection count: {str(e)}")
            return 0
