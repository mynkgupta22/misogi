import pytest
import json
import os
from app.models.intent_classifier import IntentClassifier
from app.models.rag_pipeline import RAGPipeline
from app.core.config import settings

@pytest.fixture
def intent_classifier():
    return IntentClassifier()

@pytest.fixture
def rag_pipeline():
    return RAGPipeline()

@pytest.fixture
def sample_documents():
    docs = {}
    for intent in ["technical", "billing", "feature"]:
        with open(f"app/data/{intent}_docs/documents.json", "r") as f:
            docs[intent] = json.load(f)
    return docs

def test_intent_classification(intent_classifier):
    test_queries = [
        ("How do I integrate the API?", "technical"),
        ("What are your pricing plans?", "billing"),
        ("When will dark mode be available?", "feature")
    ]
    
    for query, expected_intent in test_queries:
        intent, confidence = intent_classifier.classify(query)
        assert intent == expected_intent
        assert 0 <= confidence <= 1

def test_rag_pipeline(rag_pipeline, sample_documents):
    # Test document addition
    for intent, docs in sample_documents.items():
        rag_pipeline.add_documents(docs, intent)
    
    # Test context retrieval
    test_queries = [
        {
            "query": "How do I authenticate API requests?",
            "intent": "technical",
            "expected_keywords": ["API key", "Authorization", "Bearer"]
        },
        {
            "query": "What's included in the Pro plan?",
            "intent": "billing",
            "expected_keywords": ["Pro Plan", "$50", "Priority support"]
        },
        {
            "query": "What features are coming in Q2?",
            "intent": "feature",
            "expected_keywords": ["Q2", "collaboration", "marketplace"]
        }
    ]
    
    for test in test_queries:
        context = rag_pipeline.get_relevant_context(test["query"], test["intent"])
        
        # Check if context contains expected keywords
        for keyword in test["expected_keywords"]:
            assert keyword in context, f"Expected keyword '{keyword}' not found in context"
        
        # Test evaluation metrics
        metrics = rag_pipeline.evaluate_retrieval(test["query"], context, test["intent"])
        assert "context_length" in metrics
        assert "num_chunks" in metrics
        assert metrics["context_length"] > 0
        assert metrics["num_chunks"] > 0

def test_end_to_end(intent_classifier, rag_pipeline, sample_documents):
    # Add documents first
    for intent, docs in sample_documents.items():
        rag_pipeline.add_documents(docs, intent)
    
    # Test queries
    test_queries = [
        "How do I handle API errors?",
        "Can I get a refund?",
        "What integrations do you support?"
    ]
    
    for query in test_queries:
        # 1. Classify intent
        intent, confidence = intent_classifier.classify(query)
        assert intent in ["technical", "billing", "feature"]
        assert 0 <= confidence <= 1
        
        # 2. Get context
        context = rag_pipeline.get_relevant_context(query, intent)
        assert len(context) > 0
        
        # 3. Evaluate retrieval
        metrics = rag_pipeline.evaluate_retrieval(query, context, intent)
        assert metrics["context_length"] > 0
        assert metrics["num_chunks"] > 0 