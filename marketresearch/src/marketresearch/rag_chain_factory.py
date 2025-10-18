# src/marketresearch/rag_chain_factory.py
from .chains import ChainFactory
from .rag.pipeline import RAGPipeline

class RAGEnhancedChainFactory(ChainFactory):
    """ChainFactory enhanced with smart RAG capabilities"""
    
    def __init__(self, knowledge_base_path: str = "./knowledge"):
        super().__init__()
        self.rag_pipeline = RAGPipeline(knowledge_base_path)
        
        # Print knowledge base stats
        stats = self.rag_pipeline.get_knowledge_stats()
        print(f"✅ RAG Pipeline Initialized:")
        print(f"   📊 Total Documents: {stats['total_documents']}")
        print(f"   🏢 Company Profiles: {stats['company_profiles']}")
        print(f"   📈 Industry Reports: {stats['industry_reports']}")
        print(f"   📊 Market Data: {stats['market_data']}")
        print(f"   👤 User Preferences: {stats['user_preferences']}")
    
    def execute_chain(self, chain_type: str, **kwargs):
        """Execute a chain with smart RAG context"""
        # Get relevant context based on chain type and inputs
        rag_context = self.rag_pipeline.smart_context_retrieval(chain_type, **kwargs)
        
        if rag_context:
            # Add RAG context to inputs
            kwargs['rag_context'] = rag_context
            
            # Augment the input prompt
            original_input = kwargs.get('input', '')
            if original_input:
                augmented_input = f"""Based on the following knowledge base context:

{rag_context}

{original_input}"""
                kwargs['input'] = augmented_input
        
        # Execute the chain
        return super().execute_chain(chain_type, **kwargs)