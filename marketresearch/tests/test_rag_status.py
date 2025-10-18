# tests/test_rag_status.py
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
load_dotenv()

from marketresearch.rag.pipeline import RAGPipeline

rag = RAGPipeline("./marketresearch/knowledge")
stats = rag.get_knowledge_stats()
print("📊 Current Knowledge Base:")
for key, value in stats.items():
    print(f"   {key}: {value}")

# See actual documents
if stats['total_documents'] > 0:
    print("\n📄 Sample Documents:")
    sample = rag.vector_store.similarity_search("technology", k=2)
    for doc in sample:
        print(f"   Type: {doc['metadata'].get('type')}")
        print(f"   Source: {doc['metadata'].get('source')}")
        print(f"   Content preview: {doc['content'][:100]}...")