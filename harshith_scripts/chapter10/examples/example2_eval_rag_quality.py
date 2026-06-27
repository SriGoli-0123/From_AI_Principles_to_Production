# example2_eval_rag_quality.py
import os
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from langchain_core.embeddings import FakeEmbeddings

# Initialize and load index
if os.environ.get("OPENAI_API_KEY"):
    from langchain_openai import OpenAIEmbeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    model_info = "OpenAI text-embedding-3-small"
else:
    try:
        from langchain_community.embeddings import OllamaEmbeddings
        embeddings = OllamaEmbeddings(base_url="http://localhost:11434", model="nomic-embed-text")
        embeddings.embed_query("test")
        model_info = "Ollama nomic-embed-text"
    except Exception:
        embeddings = FakeEmbeddings(size=1536)
        model_info = "FakeEmbeddings (Fallback)"

db = InMemoryVectorStore(embeddings)

# Document corpus with source IDs
db.add_documents([
    Document(page_content="Policy doc A: Admins must enforce 2FA login verification.", metadata={"source_id": "policy_A"}),
    Document(page_content="Policy doc B: Security keys must be stored in secure vaults.", metadata={"source_id": "policy_B"}),
    Document(page_content="Policy doc C: Access is logged to central directories.", metadata={"source_id": "policy_C"})
])

# RAG evaluation cases: query -> expected source document
rag_eval_dataset = [
    {"query": "How do administrators log in?", "expected_source": "policy_A"},
    {"query": "Where do we store backup keys?", "expected_source": "policy_B"}
]

print(f"Evaluating Retrieval Recall using: {model_info}...")
successful_retrievals = 0

for case in rag_eval_dataset:
    # Query vector store (k=2 results)
    results = db.similarity_search(case["query"], k=2)
    retrieved_sources = [doc.metadata.get("source_id") for doc in results]
    
    # Check if expected source is present in retrieved chunks
    if case["expected_source"] in retrieved_sources:
        print(f"Query: '{case['query']}' -> SUCCESS (Found {case['expected_source']})")
        successful_retrievals += 1
    else:
        print(f"Query: '{case['query']}' -> FAILED (Retrieved: {retrieved_sources})")

recall = (successful_retrievals / len(rag_eval_dataset)) * 100
print(f"\nRetrieval Recall@2: {recall:.1f}%")
