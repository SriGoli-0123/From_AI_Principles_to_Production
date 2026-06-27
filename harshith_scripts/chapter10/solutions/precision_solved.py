# exercise10_1_precision_solved.py
from langchain_core.documents import Document

# ================= SOLUTION WORK =================
def calculate_precision_k(results: list[Document], expected_source: str) -> float:
    if not results:
        return 0.0
    hits = sum(1 for doc in results if doc.metadata.get("source_id") == expected_source)
    precision = (hits / len(results)) * 100
    return precision
# ================================================

# Mock search results for testing
results = [
    Document(page_content="Content 1", metadata={"source_id": "policy_A"}),
    Document(page_content="Content 2", metadata={"source_id": "policy_B"}),
    Document(page_content="Content 3", metadata={"source_id": "policy_C"})
]

expected = "policy_A"
print(f"Testing Precision@k for expected source '{expected}':")
precision_score = calculate_precision_k(results, expected)
print(f"Precision@{len(results)}: {precision_score:.1f}%")
