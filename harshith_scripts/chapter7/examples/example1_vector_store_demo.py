# example1_vector_store_demo.py
import os
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from langchain_core.embeddings import FakeEmbeddings

# 1. Initialize embedding model (swappable local/OpenAI fallback)
if os.environ.get("OPENAI_API_KEY"):
    from langchain_openai import OpenAIEmbeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    model_info = "OpenAI text-embedding-3-small"
else:
    try:
        from langchain_community.embeddings import OllamaEmbeddings
        embeddings = OllamaEmbeddings(base_url="http://localhost:11434", model="nomic-embed-text")
        embeddings.embed_query("test") # Force validation query
        model_info = "Ollama nomic-embed-text"
    except Exception:
        embeddings = FakeEmbeddings(size=1536)
        model_info = "FakeEmbeddings (Fallback)"

# 2. Initialize in-memory database
vector_store = InMemoryVectorStore(embeddings)

# 3. Load documents
docs = [
    Document(page_content="Server configuration error code 404 indicates a file is not found on the virtual host directory."),
    Document(page_content="Server configuration error code 500 indicates an unhandled internal exception in the backend code."),
    Document(page_content="Database credentials should be stored in environment variables, never hardcoded in settings.json.")
]

print(f"Indexing documents in vector store using: {model_info}...")
vector_store.add_documents(docs)

# 4. Search
query = "What does error 500 mean?"
print(f"\nQuerying: '{query}'")
results = vector_store.similarity_search(query, k=1)

print("\n--- Match Found ---")
for i, match in enumerate(results):
    print(f"Match [{i}]: {match.page_content}")
