from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

class HRRAGSystem:
    def __init__(self):
        self.pc = Pinecone(
            api_key= st.secrets["pinecone_api_key"])
            