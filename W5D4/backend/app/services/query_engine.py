from typing import List, Dict, Any, Optional
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from app.services.embeddings import MultimodalEmbeddingService
import json

class QueryEngine:
    def __init__(self):
        self.embedding_service = MultimodalEmbeddingService()
        self.llm = ChatGroq(
            temperature=0.1,
            model_name="mixtral-8x7b-32768",
            max_tokens=4096
        )
        
        # Initialize prompt templates
        self.qa_template = """You are a helpful research assistant. Use the following context to answer the question. 
        If you cannot answer the question based on the context, say so.

        Context:
        {context}

        Question: {question}

        Answer:"""
        
        self.decompose_template = """Break down the complex query into simpler subqueries that can be answered independently.
        Return the subqueries as a JSON array of strings.

        Complex Query: {query}

        Rules:
        1. Each subquery should be self-contained
        2. Order subqueries logically
        3. Include specific details from the original query
        4. Maximum 3-4 subqueries

        Return ONLY the JSON array of subqueries, no other text."""

    async def _get_relevant_chunks(
        self,
        query: str,
        filter_conditions: Optional[Dict[str, Any]] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant chunks from vector store"""
        results = await self.embedding_service.search(
            query=query,
            filter_conditions=filter_conditions,
            limit=limit
        )
        return results

    def _format_context(self, chunks: List[Dict[str, Any]]) -> str:
        """Format retrieved chunks into context string"""
        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            content = chunk["content"]
            metadata = chunk["metadata"]
            source = metadata.get("source", "Unknown")
            page = metadata.get("page", "N/A")
            
            context_parts.append(
                f"[{i}] From {source} (Page {page}):\n{content}\n"
            )
        
        return "\n\n".join(context_parts)

    async def simple_query(
        self,
        query: str,
        filter_conditions: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Process a simple query using retrieved context"""
        # Get relevant chunks
        chunks = await self._get_relevant_chunks(query, filter_conditions)
        
        if not chunks:
            return {
                "answer": "I couldn't find any relevant information to answer your question.",
                "sources": []
            }
        
        # Format context
        context = self._format_context(chunks)
        
        # Create and run chain
        prompt = PromptTemplate(
            template=self.qa_template,
            input_variables=["context", "question"]
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        # Get response
        response = await chain.ainvoke({
            "context": context,
            "question": query
        })
        
        # Format sources
        sources = [
            {
                "source": chunk["metadata"].get("source"),
                "page": chunk["metadata"].get("page"),
                "score": chunk["score"]
            }
            for chunk in chunks
        ]
        
        return {
            "answer": response["text"],
            "sources": sources
        }

    async def decomposed_query(
        self,
        query: str,
        filter_conditions: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Process a complex query by breaking it down into subqueries"""
        # First, decompose the query
        decompose_prompt = PromptTemplate(
            template=self.decompose_template,
            input_variables=["query"]
        )
        decompose_chain = LLMChain(llm=self.llm, prompt=decompose_prompt)
        
        decompose_response = await decompose_chain.ainvoke({"query": query})
        try:
            subqueries = json.loads(decompose_response["text"])
        except json.JSONDecodeError:
            return await self.simple_query(query, filter_conditions)
        
        # Process each subquery
        subquery_responses = []
        for subquery in subqueries:
            response = await self.simple_query(subquery, filter_conditions)
            subquery_responses.append({
                "subquery": subquery,
                "response": response
            })
        
        # Aggregate results
        aggregate_prompt = PromptTemplate(
            template="""Based on the answers to the subqueries below, provide a comprehensive answer to the original question.

            Original Question: {original_query}

            Subquery Results:
            {subquery_results}

            Provide a coherent response that synthesizes all the information:""",
            input_variables=["original_query", "subquery_results"]
        )
        
        aggregate_chain = LLMChain(llm=self.llm, prompt=aggregate_prompt)
        
        # Format subquery results
        subquery_results = "\n\n".join([
            f"Subquery: {r['subquery']}\nAnswer: {r['response']['answer']}"
            for r in subquery_responses
        ])
        
        final_response = await aggregate_chain.ainvoke({
            "original_query": query,
            "subquery_results": subquery_results
        })
        
        # Collect all sources
        all_sources = []
        for response in subquery_responses:
            all_sources.extend(response["response"]["sources"])
        
        return {
            "answer": final_response["text"],
            "sources": all_sources,
            "subqueries": subquery_responses
        } 