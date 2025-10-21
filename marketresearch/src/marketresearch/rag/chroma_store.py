# src/marketresearch/rag/chroma_store.py
import os
import chromadb
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
from typing import List, Dict, Any, Optional
from .google_embeddings import GoogleEmbeddings

class ChromaVectorStore:
    """ChromaDB vector store with metadata support"""
    
    def __init__(self, knowledge_base_path: str = "./knowledge", collection_name: str = "market_research"):
        self.knowledge_base_path = knowledge_base_path
        self.embeddings = GoogleEmbeddings()
        # Use environment variable or default to marketresearch/chroma_db
        chroma_path = os.getenv('CHROMA_DB_PATH', './chroma_db')
        if not os.path.isabs(chroma_path):
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            chroma_path = os.path.join(project_root, chroma_path.lstrip('./'))
        os.makedirs(chroma_path, exist_ok=True)
        self.client = chromadb.PersistentClient(path=chroma_path)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Market Research Knowledge Base"}
        )
        self._load_knowledge_base()
    
    def _load_knowledge_base(self):
        """Load and index knowledge base documents"""
        import glob
        
        # Check if collection is already populated
        if self.collection.count() > 0:
            print(f"✅ ChromaDB already has {self.collection.count()} documents")
            return
        
        documents = []
        metadatas = []
        ids = []
        
        # Load company profiles
        company_files = glob.glob(f"{self.knowledge_base_path}/company_profiles/*.txt", recursive=True)
        for file_path in company_files:
            content = self._load_file(file_path)
            if content:
                company_name = os.path.splitext(os.path.basename(file_path))[0]
                documents.append(content)
                metadatas.append({
                    "source": "company_profiles",
                    "company": company_name,
                    "file_path": file_path,
                    "type": "company_profile"
                })
                ids.append(f"company_{company_name}_{len(ids)}")
        
        # Load industry reports
        industry_files = glob.glob(f"{self.knowledge_base_path}/industry_reports/*.txt", recursive=True)
        for file_path in industry_files:
            content = self._load_file(file_path)
            if content:
                industry_name = os.path.splitext(os.path.basename(file_path))[0]
                documents.append(content)
                metadatas.append({
                    "source": "industry_reports", 
                    "industry": industry_name,
                    "file_path": file_path,
                    "type": "industry_report"
                })
                ids.append(f"industry_{industry_name}_{len(ids)}")
        
        # Load market data
        market_files = glob.glob(f"{self.knowledge_base_path}/market_data/*.txt", recursive=True)
        for file_path in market_files:
            content = self._load_file(file_path)
            if content:
                market_topic = os.path.splitext(os.path.basename(file_path))[0]
                documents.append(content)
                metadatas.append({
                    "source": "market_data",
                    "topic": market_topic,
                    "file_path": file_path,
                    "type": "market_data"
                })
                ids.append(f"market_{market_topic}_{len(ids)}")
        
        # Load user preferences
        user_pref_path = f"{self.knowledge_base_path}/user_preference.txt"
        if os.path.exists(user_pref_path):
            content = self._load_file(user_pref_path)
            if content:
                documents.append(content)
                metadatas.append({
                    "source": "user_preferences",
                    "file_path": user_pref_path,
                    "type": "user_preference"
                })
                ids.append(f"user_pref_{len(ids)}")
        
        # Add to ChromaDB
        if documents:
            print(f"📚 Adding {len(documents)} documents to ChromaDB...")
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            print(f"✅ Successfully indexed {len(documents)} documents")
        else:
            print("⚠️  No documents found in knowledge base")
    
    def _load_file(self, file_path: str) -> Optional[str]:
        """Load and clean file content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                return content if content else None
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return None
    
    def similarity_search(self, query: str, k: int = 5, filter_metadata: Dict = None) -> List[Dict[str, Any]]:
        """Search for similar documents with metadata filtering"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=k,
                where=filter_metadata  # Filter by metadata
            )
            
            documents = results['documents'][0] if results['documents'] else []
            metadatas = results['metadatas'][0] if results['metadatas'] else []
            distances = results['distances'][0] if results['distances'] else []
            
            search_results = []
            for i, (doc, metadata, distance) in enumerate(zip(documents, metadatas, distances)):
                search_results.append({
                    "content": doc,
                    "metadata": metadata,
                    "similarity": 1 - distance,  # Convert distance to similarity
                    "rank": i + 1
                })
            
            return search_results
            
        except Exception as e:
            print(f"ChromaDB search error: {e}")
            return []
    
    def get_document_count(self) -> int:
        """Get total number of documents"""
        return self.collection.count()
    
    def get_documents_by_type(self, doc_type: str) -> List[Dict]:
        """Get documents by type (company_profile, industry_report, market_data, user_preference)"""
        return self.similarity_search("", k=100, filter_metadata={"type": doc_type})