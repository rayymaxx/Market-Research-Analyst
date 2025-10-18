# tests/test_rag_chroma.py
import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_rag_chroma():
    """Test ChromaDB RAG pipeline"""
    load_dotenv()
    
    print("🧪 Testing ChromaDB RAG Pipeline...")
    
    from marketresearch.rag.pipeline import RAGPipeline
    
    # Initialize RAG pipeline
    rag = RAGPipeline("./marketresearch/knowledge")
    
    # Test knowledge base stats
    stats = rag.get_knowledge_stats()
    print(f"📊 Knowledge Base Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    if stats['total_documents'] > 0:
        # Test smart context retrieval
        test_queries = [
            ("company_research", {"research_topic": "Electric Vehicles", "company_name": "Tesla"}),
            ("industry_analysis", {"research_topic": "Renewable Energy", "industry_name": "Solar"}),
            ("market_trends", {"research_topic": "AI Technology"})
        ]
        
        for chain_type, inputs in test_queries:
            context = rag.smart_context_retrieval(chain_type, **inputs)
            print(f"\n🔍 {chain_type} context length: {len(context)} chars")
            if context:
                print(f"   First 200 chars: {context[:200]}...")
    
    print("✅ ChromaDB RAG pipeline test completed!")

def test_rag_enhanced_factory():
    """Test RAG-enhanced chain factory"""
    load_dotenv()
    
    print("\n🧪 Testing RAG-Enhanced Chain Factory...")
    
    from marketresearch.rag_chain_factory import RAGEnhancedChainFactory
    
    # Initialize factory
    factory = RAGEnhancedChainFactory("./knowledge")
    
    # Test a chain with RAG
    try:
        result = factory.execute_chain(
            "market_trends",
            research_topic="Electric Vehicle Market",
            current_date="2024-01-01",
            format_instructions="Provide market trends analysis",
            input="Analyze current market trends and opportunities",
            market_data={}
        )
        print(f"✅ RAG-enhanced chain executed successfully")
        print(f"   Model: {factory.get_model_for_chain('market_trends')}")
    except Exception as e:
        print(f"❌ RAG-enhanced chain failed: {e}")

if __name__ == "__main__":
    test_rag_chroma()
    test_rag_enhanced_factory()