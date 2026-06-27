# exercise7_1_score_filter.py
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.embeddings import FakeEmbeddings
from langchain_core.documents import Document

embeddings = FakeEmbeddings(size=1536)
db = InMemoryVectorStore(embeddings)

# TODO: Write a function similarity_search_with_threshold(db, query, threshold=0.7)
# - Use db.similarity_search_with_relevance_scores(query, k=3)
# - Loop through (doc, score) tuples and only return the doc list where score >= threshold.
def similarity_search_with_threshold(db, query, threshold=0.7) -> list[Document]:
    pass
