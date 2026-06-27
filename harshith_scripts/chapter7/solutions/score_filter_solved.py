# exercise7_1_score_filter_solved.py
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.embeddings import FakeEmbeddings
from langchain_core.documents import Document

# Initialize mock vector database
embeddings = FakeEmbeddings(size=1536)
db = InMemoryVectorStore(embeddings)

# Populate database
db.add_documents([
    Document(page_content="Policy Alpha: Keep passwords secret."),
    Document(page_content="Policy Beta: Access restricted to authorized admins.")
])

# ================= SOLUTION WORK =================
def similarity_search_with_threshold(db, query, threshold=0.7) -> list[Document]:
    # Fetch results with relevance scores
    results_with_scores = db.similarity_search_with_relevance_scores(query, k=3)
    
    # Filter documents based on threshold
    filtered_docs = [doc for doc, score in results_with_scores if score >= threshold]
    return filtered_docs
# ================================================

# Test search
query = "What is Policy Alpha?"
print(f"Query: {query}")
results = similarity_search_with_threshold(db, query, threshold=0.0) # Using 0.0 threshold to pass fake embeddings' low random scores
print(f"Found {len(results)} matches.")
for i, doc in enumerate(results):
    print(f"[{i}]: {doc.page_content}")
