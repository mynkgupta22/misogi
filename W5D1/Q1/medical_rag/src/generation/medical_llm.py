"""
Medical response generator using OpenAI's GPT-3.5.
"""
from typing import List, Dict, Optional
from openai import OpenAI
from src.config import (
    OPENAI_API_KEY,
    LLM_MODEL,
    TEMPERATURE,
    MAX_TOKENS,
    SYSTEM_MESSAGES,
    QUERY_TYPES
)

class MedicalResponseGenerator:
    def __init__(self):
        """Initialize the medical response generator."""
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = "gpt-3.5-turbo"  # Use GPT-3.5 Turbo model
        self.temperature = TEMPERATURE
        self.max_tokens = MAX_TOKENS
        
    def _format_context(self, documents: List[Dict]) -> str:
        """
        Format retrieved documents into context string.
        
        Args:
            documents: List of retrieved documents
            
        Returns:
            Formatted context string
        """
        context = "Relevant medical literature:\n\n"
        for i, doc in enumerate(documents, 1):
            context += f"[Source {i}] {doc['text']}\n"
            context += f"Citation: {doc['metadata'].get('source', f'Source {i}')}\n\n"
        return context
        
    def generate_response(
        self,
        query: str,
        documents: List[Dict],
        query_type: str = QUERY_TYPES["GENERAL_MEDICAL"]
    ) -> Dict:
        """
        Generate a medical response using GPT-4.
        
        Args:
            query: User query
            documents: Retrieved relevant documents
            query_type: Type of medical query
            
        Returns:
            Dictionary containing response and metadata
        """
        # Get appropriate system message
        system_message = SYSTEM_MESSAGES.get(query_type, SYSTEM_MESSAGES[QUERY_TYPES["GENERAL_MEDICAL"]])
        
        # Format context
        context = self._format_context(documents)
        
        # Create messages
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"""Context: {context}\n\nQuestion: {query}\n\n
            Based on the provided medical literature, please provide a comprehensive answer.
            Include relevant citations and any necessary medical disclaimers."""}
        ]
        
        # Generate response
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        
        # Extract and format response
        answer = response.choices[0].message.content
        
        return {
            "answer": answer,
            "model": self.model,
            "query_type": query_type,
            "sources": [doc["metadata"].get("source", f"Source {i+1}") for i, doc in enumerate(documents)]
        }
        
    def generate_safety_check(self, response: str) -> Dict:
        """
        Perform safety check on generated response.
        
        Args:
            response: Generated medical response
            
        Returns:
            Dictionary containing safety assessment
        """
        safety_prompt = f"""
        Please analyze this medical response for safety and accuracy:
        
        {response}
        
        Evaluate the following:
        1. Are there any potentially harmful recommendations?
        2. Are all medical claims supported by the provided sources?
        3. Are appropriate disclaimers included?
        4. Is the information current and accurate?
        
        Provide a safety assessment and any concerns.
        """
        
        messages = [
            {"role": "system", "content": "You are a medical safety verification system. Your job is to identify potential safety issues in medical responses."},
            {"role": "user", "content": safety_prompt}
        ]
        
        safety_check = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.0,
            max_tokens=self.max_tokens
        )
        
        assessment = safety_check.choices[0].message.content
        
        return {
            "safety_assessment": assessment,
            "model": self.model
        } 