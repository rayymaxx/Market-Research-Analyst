# tests/test_integrated_crew.py
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
load_dotenv()

def test_integrated_crew():
    """Test the integrated crew with chains"""
    print("🧪 Testing Integrated Crew with Chains...")
    
    try:
        from marketresearch.crew import MarketResearchCrew
        
        # Initialize crew
        crew = MarketResearchCrew()
        
        # Test agent tools
        print("✅ Crew initialized successfully")
        print("\nAgent Tools:")
        
        agents_to_check = [
            "digitalIntelligenceGatherer",
            "quantitativeInsightsSpecialist", 
            "strategicCommunicationsExpert"
        ]
        
        for agent_name in agents_to_check:
            agent = getattr(crew, agent_name)()
            tool_names = [tool.name for tool in agent.tools] if agent.tools else []
            print(f"   - {agent_name}: {len(tool_names)} tools")
            for tool in tool_names:
                print(f"     * {tool}")
        
        # Test RAG factory
        stats = crew.chain_factory.rag_pipeline.get_knowledge_stats()
        print(f"\n📚 RAG Knowledge Base: {stats['total_documents']} documents")
        
        print("\n🎉 Integrated crew is ready!")
        return True
        
    except Exception as e:
        print(f"❌ Integrated crew test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_integrated_crew()