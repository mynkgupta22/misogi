"""
Chroma vector store manager for medical document embeddings.
"""
from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings
from langchain_community.embeddings import HuggingFaceEmbeddings
from src.config import CHROMA_PERSIST_DIRECTORY

class ChromaManager:
    """Manage Chroma vector store for document embeddings."""
    
    def __init__(self):
        """Initialize the Chroma vector store."""
        self.client = chromadb.Client(Settings(
            persist_directory=CHROMA_PERSIST_DIRECTORY,
            anonymized_telemetry=False
        ))
        
        # Use sentence-transformers model for embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
        )
        
        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name="medical_documents",
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_documents(self, documents: List[Dict[str, str]]) -> None:
        """
        Add documents to the vector store.
        
        Args:
            documents: List of documents with text and metadata
        """
        # Extract text and metadata
        texts = [doc['text'] for doc in documents]
        metadatas = [doc['metadata'] for doc in documents]
        ids = [f"doc_{i}" for i in range(len(documents))]
        
        # Get embeddings
        embeddings = self.embeddings.embed_documents(texts)
        
        # Add to collection
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
    
    def similarity_search(
        self,
        query: str,
        n_results: int = 5
    ) -> List[Dict[str, str]]:
        """
        Search for similar documents.
        
        Args:
            query: Search query
            n_results: Number of results to return
            
        Returns:
            List of similar documents with scores
        """
        # Get query embedding
        query_embedding = self.embeddings.embed_query(query)
        
        # Search collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        
        # Format results
        documents = []
        for i in range(len(results['documents'][0])):
            doc = {
                'text': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'score': 1 - results['distances'][0][i]  # Convert distance to similarity score
            }
            documents.append(doc)
        
        return documents
    
    def get_collection_stats(self) -> Dict[str, int]:
        """Get statistics about the collection."""
        return {
            'total_documents': self.collection.count()
        } 