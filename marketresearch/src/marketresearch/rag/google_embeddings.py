# src/marketresearch/rag/google_embeddings.py
import os
import google.generativeai as genai
from typing import List

class GoogleEmbeddings:
    """Google Gemini Embeddings - zero CPU usage, cloud-based"""
    
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = "models/text-embedding-004"
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple documents via Google API"""
        embeddings = []
        for text in texts:
            try:
                result = genai.embed_content(
                    model=self.model,
                    content=text[:2000],  # Limit for API
                    task_type="retrieval_document"
                )
                embeddings.append(result['embedding'])
            except Exception as e:
                print(f"Embedding error: {e}")
                embeddings.append([0.0] * 768)  # Fallback
        return embeddings
    
    def embed_query(self, text: str) -> List[float]:
        """Embed query via Google API"""
        try:
            result = genai.embed_content(
                model=self.model,
                content=text[:2000],
                task_type="retrieval_query"
            )
            return result['embedding']
        except Exception as e:
            print(f"Query embedding error: {e}")
            return [0.0] * 768