from typing import Tuple, Dict, List
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from app.core.config import settings

class IntentClassifier:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.intents = ["technical", "billing", "feature"]
        
        # Sample queries per intent for zero-shot classification
        self.sample_queries: Dict[str, List[str]] = {
            "technical": [
                "How do I integrate the API?",
                "Getting error 404 when calling endpoint",
                "Documentation for authentication",
                "How to implement OAuth?",
                "API rate limits",
            ],
            "billing": [
                "How much does the premium plan cost?",
                "Can I get a refund?",
                "Payment method update",
                "Billing cycle information",
                "Cancel subscription",
            ],
            "feature": [
                "Can you add dark mode?",
                "When will mobile support be available?",
                "Planning to add export functionality",
                "Feature comparison with competitors",
                "New feature request",
            ]
        }
        
        # Pre-compute embeddings for sample queries
        self.sample_embeddings = {
            intent: self.model.encode(queries)
            for intent, queries in self.sample_queries.items()
        }
    
    def classify(self, query: str) -> Tuple[str, float]:
        """
        Classify the intent of a query using semantic similarity.
        
        Args:
            query: The user's query string
            
        Returns:
            Tuple of (intent, confidence_score)
        """
        # Get query embedding
        query_embedding = self.model.encode([query])[0]
        
        # Calculate similarity with each intent's samples
        intent_scores = {}
        for intent, embeddings in self.sample_embeddings.items():
            # Calculate cosine similarity with all samples
            similarities = cosine_similarity([query_embedding], embeddings)[0]
            # Take the maximum similarity as the score for this intent
            intent_scores[intent] = float(np.max(similarities))
        
        # Get the highest scoring intent
        max_intent = max(intent_scores.items(), key=lambda x: x[1])
        intent, confidence = max_intent
        
        return intent, confidence
    
    def evaluate_response(self, query: str, response: str, intent: str) -> Dict:
        """
        Evaluate the quality of the response.
        
        Args:
            query: Original user query
            response: Generated response
            intent: Classified intent
            
        Returns:
            Dictionary with evaluation metrics
        """
        # Encode query and response
        query_embedding = self.model.encode([query])[0]
        response_embedding = self.model.encode([response])[0]
        
        # Calculate response relevance using cosine similarity
        relevance = float(cosine_similarity([query_embedding], [response_embedding])[0][0])
        
        # Calculate context utilization (simplified metric)
        context_score = relevance * 0.8  # Simplified metric
        
        return {
            "response_relevance": relevance,
            "context_utilization": context_score,
            "intent_confidence": self.classify(query)[1]
        } 