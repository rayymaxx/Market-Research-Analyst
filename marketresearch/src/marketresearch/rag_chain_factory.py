# src/marketresearch/rag_chain_factory.py
from .rag.pipeline import RAGPipeline
from langchain.memory import ConversationBufferMemory

class RAGEnhancedChainFactory:
    """Simplified RAG factory without complex chains"""
    
    def __init__(self, knowledge_base_path: str = "./knowledge"):
        self.memory = ConversationBufferMemory(
            return_messages=True,
            memory_key="research_history"
        )
        self.rag_pipeline = RAGPipeline(knowledge_base_path)
        
        # Print knowledge base stats
        stats = self.rag_pipeline.get_knowledge_stats()
        print(f"✅ RAG Pipeline Initialized:")
        print(f"   📊 Total Documents: {stats['total_documents']}")
        print(f"   🏢 Company Profiles: {stats['company_profiles']}")
        print(f"   📈 Industry Reports: {stats['industry_reports']}")
        print(f"   📊 Market Data: {stats['market_data']}")
        print(f"   👤 User Preferences: {stats['user_preferences']}")
    
    def get_research_summary(self):
        """Get summary of research progress"""
        memory_vars = self.memory.load_memory_variables({})
        return f"Research sessions: {len(memory_vars.get('research_history', []))}"
    
    def smart_context_retrieval(self, query_type: str, **kwargs):
        """Get relevant context from RAG pipeline"""
        return self.rag_pipeline.smart_context_retrieval(query_type, **kwargs)