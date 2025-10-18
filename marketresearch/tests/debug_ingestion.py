# tests/debug_ingestion_fixed.py
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
load_dotenv()

def debug_ingestion_fixed():
    print("🔧 DEBUGGING INGESTION ISSUES - FIXED VERSION")
    print("=" * 50)
    
    # Use the correct path
    kb_path = "./marketresearch/knowledge"
    
    # 1. Check environment
    print("1. Checking Environment...")
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    print(f"   HUGGINGFACE_API_KEY: {'✅ Set' if api_key else '❌ Missing'}")
    
    # 2. Check knowledge base structure with correct path
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
        print("   ❌ Knowledge base not found at that path!")
        print("   Available paths:")
        for root, dirs, files in os.walk("."):
            if "knowledge" in root:
                print(f"   - {root}")
    
    # 3. Test embeddings first (since this was failing)
    print("\n3. Testing Embeddings...")
    from marketresearch.rag.huggingface_embeddings import HuggingFaceEmbeddings
    
    embedder = HuggingFaceEmbeddings()
    test_text = "This is a test document for embedding"
    print("   Sending test request to HuggingFace...")
    embedding = embedder.embed_query(test_text)
    
    if embedding and len(embedding) > 0:
        print(f"   ✅ Embeddings working - vector length: {len(embedding)}")
    else:
        print("   ❌ Embeddings failed - this will prevent ingestion")
        return
    
    # 4. Test file loading with correct path
    print("\n4. Testing File Loading...")
    from marketresearch.rag.chroma_store import ChromaVectorStore
    
    print("   Initializing ChromaVectorStore...")
    try:
        vector_store = ChromaVectorStore(kb_path)
        count = vector_store.get_document_count()
        print(f"   Documents in collection: {count}")
        
        if count == 0:
            print("   ⚠️  No documents found. Let's check why...")
            
            # Manually test file loading
            import glob
            print("\n   Manual file check:")
            company_files = glob.glob(f"{kb_path}/company_profiles/*.txt")
            print(f"   Company files: {len(company_files)}")
            for f in company_files[:3]:  # Show first 3
                print(f"     - {os.path.basename(f)}")
                
        else:
            print("   ✅ Documents successfully ingested!")
            
    except Exception as e:
        print(f"   ❌ Error during initialization: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_ingestion_fixed()