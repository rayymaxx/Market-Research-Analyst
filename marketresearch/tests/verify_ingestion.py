# tests/verify_ingestion.py
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
load_dotenv()

def verify_ingestion():
    from marketresearch.rag.pipeline import RAGPipeline
    
    print("🔍 Verifying Data Ingestion...")
    
    rag = RAGPipeline("./marketresearch/knowledge")
    stats = rag.get_knowledge_stats()
    
    print(f"✅ Knowledge Base Status:")
    print(f"   Total Documents: {stats['total_documents']}")
    print(f"   Company Profiles: {stats['company_profiles']}")
    print(f"   Industry Reports: {stats['industry_reports']}") 
    print(f"   Market Data: {stats['market_data']}")
    print(f"   User Preferences: {stats['user_preferences']}")
    
    if stats['total_documents'] == 0:
        print("\n❌ No documents found! Please check:")
        print("   - knowledge/company_profiles/ has .txt files")
        print("   - knowledge/industry_reports/ has .txt files") 
        print("   - knowledge/market_data/ has .txt files")
        print("   - File permissions are correct")
    else:
        print("\n🎉 Data successfully ingested!")

if __name__ == "__main__":
    verify_ingestion()