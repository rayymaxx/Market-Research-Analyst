# tests/test_isolated_issue.py
import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_chain_creation_only():
    """Test just chain creation without execution"""
    load_dotenv()
    
    from marketresearch.chains import ChainFactory
    
    print("🧪 Testing Chain Creation Only...")
    
    factory = ChainFactory()
    
    # Test chain creation for each type
    test_chains = [
        "swot_analysis",
        "company_research", 
        "executive_summary"
    ]
    
    for chain_type in test_chains:
        try:
            chain = factory.get_chain(chain_type)
            print(f"✅ {chain_type:25} - Chain created successfully")
            print(f"   Chain type: {type(chain)}")
            print(f"   LLM type: {type(chain.llm)}")
        except Exception as e:
            print(f"❌ {chain_type:25} - Chain creation failed: {e}")
    
    print("\n✅ Chain creation test completed!")

def test_chain_inspect_llm():
    """Inspect the LLM object in a chain"""
    load_dotenv()
    
    from marketresearch.chains import ChainFactory
    
    print("\n🧪 Inspecting Chain LLM...")
    
    factory = ChainFactory()
    chain = factory.get_chain("swot_analysis")
    
    print(f"Chain LLM attributes: {dir(chain.llm)}")
    print(f"LLM type: {type(chain.llm)}")
    
    # Check if model_manager exists
    if hasattr(chain.llm, 'model_manager'):
        print("✅ model_manager attribute exists")
    else:
        print("❌ model_manager attribute does not exist")

if __name__ == "__main__":
    test_chain_creation_only()
    test_chain_inspect_llm()