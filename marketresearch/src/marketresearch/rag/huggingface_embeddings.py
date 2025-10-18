# src/marketresearch/rag/huggingface_embeddings.py
import os
import requests
from typing import List, Dict, Any
import json

class HuggingFaceEmbeddings:
    """HuggingFace Embeddings via API (no local models)"""
    
    def __init__(self):
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.api_url = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple documents"""
        embeddings = []
        for text in texts:
            embedding = self.embed_query(text)
            if embedding:
                embeddings.append(embedding)
        return embeddings
    
    def embed_query(self, text: str) -> List[float]:
        """Embed a single query"""
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={"inputs": text, "options": {"wait_for_model": True}}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"HuggingFace API error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Embedding error: {e}")
            return None