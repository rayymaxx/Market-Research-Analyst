# tests/debug_ingestion.py
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
load_dotenv()

def debug_ingestion():
    print("🔧 DEBUGGING GOOGLE EMBEDDINGS INGESTION")
    print("=" * 50)
    
    kb_path = "/home/rayymond/Market-Research-Analyst/marketresearch/knowledge"
    
    # 1. Check environment
    print("1. Checking Environment...")
    api_key = os.getenv("GEMINI_API_KEY")
    print(f"   GEMINI_API_KEY: {'✅ Set' if api_key else '❌ Missing'}")
    
    # 2. Check knowledge base structure
    print("\n2. Checking Knowledge Base Structure...")
    print(f"   Knowledge base path: {os.path.abspath(kb_path)}")
    print(f"   Path exists: {os.path.exists(kb_path)}")
    
    if os.path.exists(kb_path):
        print("   ✅ Knowledge base found! Contents:")
        for root, dirs, files in os.walk(kb_path):
            level = root.replace(kb_path, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f'{indent}{os.path.basename(root)}/')
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                print(f'{subindent}{file} ({file_size} bytes)')
    else:
        print("   ❌ Knowledge base not found!")
        return
    
    # 3. Test Google embeddings
    print("\n3. Testing Google Embeddings...")
    from marketresearch.rag.google_embeddings import GoogleEmbeddings
    
    embedder = GoogleEmbeddings()
    test_text = "This is a test document for embedding"
    print("   Sending test request to Google...")
    embedding = embedder.embed_query(test_text)
    
    if embedding and len(embedding) > 0:
        print(f"   ✅ Google embeddings working - vector length: {len(embedding)}")
    else:
        print("   ❌ Google embeddings failed - this will prevent ingestion")
        return
    
    # 4. Test ChromaDB ingestion
    print("\n4. Testing ChromaDB Ingestion...")
    from marketresearch.rag.chroma_store import ChromaVectorStore
    
    print("   Initializing ChromaVectorStore with Google embeddings...")
    try:
        vector_store = ChromaVectorStore(kb_path)
        count = vector_store.get_document_count()
        print(f"   Documents in collection: {count}")
        
        if count == 0:
            print("   ⚠️  No documents found. Checking files...")
            import glob
            company_files = glob.glob(f"{kb_path}/company_profiles/*.txt")
            print(f"   Company files available: {len(company_files)}")
        else:
            print("   ✅ Documents successfully ingested with Google embeddings!")
            
            # Test similarity search
            print("\n5. Testing Similarity Search...")
            results = vector_store.similarity_search("AI technology", k=2)
            print(f"   Search results: {len(results)} documents found")
            if results:
                print(f"   Top result similarity: {results[0]['similarity']:.3f}")
            
    except Exception as e:
        print(f"   ❌ Error during initialization: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_ingestion()