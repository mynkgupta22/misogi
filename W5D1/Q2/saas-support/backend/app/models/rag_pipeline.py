from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings
from app.core.config import settings

class RAGPipeline:
    def __init__(self):
        self.client = chromadb.Client(Settings(
            persist_directory=settings.CHROMA_PERSIST_DIR,
            is_persistent=True
        ))
        
        # Initialize collections for each intent
        self.collections = {}
        for intent, config in settings.VECTOR_STORE_SETTINGS.items():
            try:
                self.collections[intent] = self.client.get_or_create_collection(
                    name=config["collection_name"],
                    metadata={"intent": intent}
                )
            except Exception as e:
                print(f"Error initializing collection for {intent}: {e}")
                
    def add_documents(self, documents: List[Dict[str, Any]], intent: str):
        """
        Add documents to the appropriate collection based on intent.
        
        Args:
            documents: List of documents with 'content' and 'metadata' fields
            intent: The intent category for these documents
        """
        if intent not in self.collections:
            raise ValueError(f"Invalid intent: {intent}")
            
        collection = self.collections[intent]
        
        # Prepare documents for insertion
        ids = [str(i) for i in range(len(documents))]
        texts = [doc["content"] for doc in documents]
        metadatas = [doc.get("metadata", {}) for doc in documents]
        
        # Add documents to collection
        collection.add(
            documents=texts,
            ids=ids,
            metadatas=metadatas
        )
        
    def get_relevant_context(self, query: str, intent: str, n_results: int = 3) -> str:
        """
        Retrieve relevant context for a query from the appropriate collection.
        
        Args:
            query: The user's query
            intent: The classified intent
            n_results: Number of results to retrieve
            
        Returns:
            Concatenated relevant context
        """
        if intent not in self.collections:
            return ""
            
        collection = self.collections[intent]
        
        # Query the collection
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        # Combine relevant documents into context
        if results and results['documents']:
            contexts = results['documents'][0]  # Get first query results
            # Combine contexts with metadata
            combined_context = "\n\n".join(
                f"Document {i+1}:\n{doc}"
                for i, doc in enumerate(contexts)
            )
            return combined_context
            
        return ""
        
    def evaluate_retrieval(self, query: str, retrieved_context: str, intent: str) -> Dict[str, float]:
        """
        Evaluate the quality of retrieved context.
        
        Args:
            query: Original query
            retrieved_context: Retrieved context
            intent: Classified intent
            
        Returns:
            Dictionary with evaluation metrics
        """
        # For MVP, implement simple metrics
        context_length = len(retrieved_context.split())
        
        return {
            "context_length": context_length,
            "num_chunks": len(retrieved_context.split("\n\n")),
        } 