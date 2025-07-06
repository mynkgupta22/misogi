from typing import List, Optional
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DocumentProcessor:
    def __init__(self, persist_directory: str = "db"):
        self.persist_directory = persist_directory
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )
        self.embeddings = OpenAIEmbeddings()
        
    def load_document(self, file_path: str):
        """Load and split document into chunks"""
        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith('.docx'):
            loader = Docx2txtLoader(file_path)
        else:
            raise ValueError("Unsupported file format. Please use PDF or DOCX files.")
            
        documents = loader.load()
        chunks = self.text_splitter.split_documents(documents)
        return chunks

    def store_documents(self, chunks) -> Chroma:
        """Store document chunks in vector store"""
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        vectorstore.persist()
        return vectorstore

    def process_file(self, file_path: str) -> Chroma:
        """Process a file and store it in the vector store"""
        chunks = self.load_document(file_path)
        return self.store_documents(chunks)

    def get_vectorstore(self) -> Optional[Chroma]:
        """Get existing vector store if it exists"""
        if os.path.exists(self.persist_directory):
            return Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
        return None 