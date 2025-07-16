from typing import List, Dict, Any, Optional
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from app.services.document_processor import DocumentProcessor
from app.services.embeddings import MultimodalEmbeddingService
import spacy
from collections import defaultdict
import networkx as nx
import json

class SummarizationService:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.1,
            model_name="mixtral-8x7b-32768",
            max_tokens=4096
        )
        self.doc_processor = DocumentProcessor()
        self.embedding_service = MultimodalEmbeddingService()
        
        # Load spaCy model for entity extraction
        self.nlp = spacy.load("en_core_web_sm")
        
        # Initialize prompt templates
        self.executive_template = """Create an executive summary of the following content. Focus on key points, insights, and recommendations.

Content:
{content}

Format the summary with the following sections:
1. Overview
2. Key Findings
3. Recommendations
4. Next Steps

Summary:"""

        self.bullet_template = """Create a bullet-point summary of the following content. Focus on the most important points and insights.

Content:
{content}

Format as:
• Main points
• Supporting details
• Notable findings
• Action items

Summary:"""

        self.trend_template = """Analyze the following content and identify key trends, patterns, and insights.

Content:
{content}

Focus on:
1. Emerging trends
2. Recurring patterns
3. Notable changes
4. Future implications

Analysis:"""

        self.cross_doc_template = """Compare and synthesize information across multiple documents.

Documents:
{documents}

Provide:
1. Common themes
2. Key differences
3. Integrated insights
4. Overall conclusions

Synthesis:"""

    async def summarize_document(
        self,
        document_id: str,
        summary_type: str = "executive"
    ) -> Dict[str, Any]:
        """Generate a summary for a single document"""
        # Get document chunks
        chunks = await self.embedding_service.search(
            query=f"document_id:{document_id}",
            filter_conditions={"document_id": document_id},
            limit=50  # Get more chunks for full document summary
        )
        
        if not chunks:
            return {"summary": "Document not found"}
        
        # Combine chunks
        content = "\n\n".join([chunk["content"] for chunk in chunks])
        
        # Select template
        if summary_type == "bullet":
            template = self.bullet_template
        elif summary_type == "trend":
            template = self.trend_template
        else:  # executive
            template = self.executive_template
        
        # Create and run chain
        prompt = PromptTemplate(
            template=template,
            input_variables=["content"]
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        response = await chain.ainvoke({"content": content})
        
        return {
            "summary": response["text"],
            "document_id": document_id,
            "summary_type": summary_type
        }

    async def summarize_section(
        self,
        section: str,
        summary_type: str = "executive"
    ) -> Dict[str, Any]:
        """Generate a summary for a specific section"""
        # Get section chunks
        chunks = await self.embedding_service.search(
            query=f"section:{section}",
            filter_conditions={"section": section},
            limit=30
        )
        
        if not chunks:
            return {"summary": "Section not found"}
        
        # Combine chunks
        content = "\n\n".join([chunk["content"] for chunk in chunks])
        
        # Select template
        if summary_type == "bullet":
            template = self.bullet_template
        elif summary_type == "trend":
            template = self.trend_template
        else:  # executive
            template = self.executive_template
        
        # Create and run chain
        prompt = PromptTemplate(
            template=template,
            input_variables=["content"]
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        response = await chain.ainvoke({"content": content})
        
        return {
            "summary": response["text"],
            "section": section,
            "summary_type": summary_type
        }

    async def summarize_across_documents(
        self,
        document_ids: List[str],
        summary_type: str = "executive"
    ) -> Dict[str, Any]:
        """Generate a summary across multiple documents"""
        all_chunks = []
        for doc_id in document_ids:
            chunks = await self.embedding_service.search(
                query=f"document_id:{doc_id}",
                filter_conditions={"document_id": doc_id},
                limit=20
            )
            all_chunks.extend(chunks)
        
        if not all_chunks:
            return {"summary": "No documents found"}
        
        # Group chunks by document
        docs_content = defaultdict(list)
        for chunk in all_chunks:
            doc_id = chunk["metadata"]["document_id"]
            docs_content[doc_id].append(chunk["content"])
        
        # Format documents for template
        documents_text = "\n\n".join([
            f"Document {doc_id}:\n" + "\n".join(contents)
            for doc_id, contents in docs_content.items()
        ])
        
        # Create and run chain
        prompt = PromptTemplate(
            template=self.cross_doc_template,
            input_variables=["documents"]
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        response = await chain.ainvoke({"documents": documents_text})
        
        return {
            "summary": response["text"],
            "document_ids": document_ids,
            "summary_type": "cross_document"
        }

    async def extract_concepts(self, text: str) -> Dict[str, Any]:
        """Extract concepts and their relationships using spaCy"""
        doc = self.nlp(text)
        
        # Extract entities
        entities = [
            {
                "text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char
            }
            for ent in doc.ents
        ]
        
        # Build relationship graph
        G = nx.Graph()
        
        # Add entities as nodes
        for entity in entities:
            G.add_node(entity["text"], type=entity["label"])
        
        # Add relationships based on sentence co-occurrence
        for sent in doc.sents:
            sent_entities = [ent.text for ent in sent.ents]
            for i in range(len(sent_entities)):
                for j in range(i + 1, len(sent_entities)):
                    G.add_edge(sent_entities[i], sent_entities[j])
        
        # Convert graph to JSON-serializable format
        graph_data = {
            "nodes": [
                {
                    "id": node,
                    "label": node,
                    "type": G.nodes[node].get("type", "UNKNOWN")
                }
                for node in G.nodes()
            ],
            "edges": [
                {
                    "source": source,
                    "target": target
                }
                for source, target in G.edges()
            ]
        }
        
        return {
            "entities": entities,
            "graph": graph_data,
            "statistics": {
                "entity_count": len(entities),
                "relationship_count": len(G.edges())
            }
        }

    async def generate_concept_map(
        self,
        document_id: Optional[str] = None,
        section: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate a concept map for a document or section"""
        # Get content
        filter_conditions = {}
        if document_id:
            filter_conditions["document_id"] = document_id
        if section:
            filter_conditions["section"] = section
        
        chunks = await self.embedding_service.search(
            query="",  # Empty query to get all chunks
            filter_conditions=filter_conditions,
            limit=50
        )
        
        if not chunks:
            return {"error": "No content found"}
        
        # Combine chunks
        content = "\n\n".join([chunk["content"] for chunk in chunks])
        
        # Extract concepts and relationships
        concept_data = await self.extract_concepts(content)
        
        return {
            "document_id": document_id,
            "section": section,
            "concepts": concept_data
        } 