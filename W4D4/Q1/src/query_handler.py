from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import Chroma
from typing import Dict, List

class QueryHandler:
    def __init__(self, vectorstore: Chroma):
        self.llm = ChatOpenAI(
            temperature=0,
            model="gpt-3.5-turbo"
        )
        self.retriever = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            return_source_documents=True
        )
    
    def get_response(self, query: str) -> Dict:
        """Get response for a query"""
        result = self.qa_chain({"question": query, "chat_history": []})
        
        # Extract source information
        sources = []
        for doc in result["source_documents"]:
            if hasattr(doc, 'metadata'):
                sources.append(doc.metadata)
        
        return {
            "answer": result["answer"],
            "sources": sources
        } 