# src/marketresearch/rag/pipeline.py
from typing import List, Dict, Any
from .chroma_store import ChromaVectorStore

class RAGPipeline:
    """Enhanced RAG pipeline with ChromaDB and metadata support"""
    
    def __init__(self, knowledge_base_path: str = "./knowledge"):
        self.vector_store = ChromaVectorStore(knowledge_base_path)
    
    def retrieve_relevant_context(self, query: str, max_results: int = 3, 
                                doc_types: List[str] = None) -> str:
        """Retrieve relevant context with optional document type filtering"""
        filter_metadata = None
        if doc_types:
            filter_metadata = {"type": {"$in": doc_types}}
        
        results = self.vector_store.similarity_search(
            query, 
            k=max_results, 
            filter_metadata=filter_metadata
        )
        
        if not results:
            return ""
        
        context_parts = []
        for result in results:
            metadata = result['metadata']
            source_type = metadata.get('type', 'unknown')
            source_name = self._get_source_name(metadata)
            
            context_parts.append(f"--- {source_type.upper()} | {source_name} | Similarity: {result['similarity']:.2f} ---")
            context_parts.append(result['content'][:800] + "..." if len(result['content']) > 800 else result['content'])
        
        return "\n\n".join(context_parts)
    
    def _get_source_name(self, metadata: Dict) -> str:
        """Get readable source name from metadata"""
        if metadata.get('company'):
            return f"Company: {metadata['company']}"
        elif metadata.get('industry'):
            return f"Industry: {metadata['industry']}"
        elif metadata.get('topic'):
            return f"Topic: {metadata['topic']}"
        else:
            return metadata.get('source', 'Unknown')
    
    def smart_context_retrieval(self, chain_type: str, **kwargs) -> str:
        """Smart context retrieval based on chain type and inputs"""
        research_topic = kwargs.get('research_topic', '')
        company_name = kwargs.get('company_name', '')
        industry_name = kwargs.get('industry_name', '')
        
        # Build query from available inputs
        query_parts = []
        if research_topic:
            query_parts.append(research_topic)
        if company_name:
            query_parts.append(company_name)
        if industry_name:
            query_parts.append(industry_name)
        
        query = " ".join(query_parts) if query_parts else research_topic
        
        # Determine document types based on chain type
        doc_types_mapping = {
            "company_research": ["company_profile", "industry_report"],
            "industry_analysis": ["industry_report", "market_data"],
            "swot_analysis": ["company_profile", "industry_report", "market_data"],
            "competitive_benchmarking": ["company_profile", "market_data"],
            "market_trends": ["market_data", "industry_report"],
            "data_collection": ["market_data", "industry_report", "company_profile"],
            "executive_summary": ["industry_report", "market_data", "user_preference"],
            "research_report": ["industry_report", "market_data", "company_profile"],
            "strategic_recommendations": ["industry_report", "market_data", "user_preference"]
        }
        
        doc_types = doc_types_mapping.get(chain_type, None)
        
        return self.retrieve_relevant_context(query, max_results=3, doc_types=doc_types)
    
    def get_knowledge_stats(self) -> Dict[str, Any]:
        """Get knowledge base statistics"""
        total_docs = self.vector_store.get_document_count()
        company_docs = len(self.vector_store.get_documents_by_type("company_profile"))
        industry_docs = len(self.vector_store.get_documents_by_type("industry_report"))
        market_docs = len(self.vector_store.get_documents_by_type("market_data"))
        user_docs = len(self.vector_store.get_documents_by_type("user_preference"))
        
        return {
            "total_documents": total_docs,
            "company_profiles": company_docs,
            "industry_reports": industry_docs,
            "market_data": market_docs,
            "user_preferences": user_docs
        }