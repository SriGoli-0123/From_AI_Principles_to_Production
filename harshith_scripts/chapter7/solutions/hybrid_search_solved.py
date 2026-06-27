# exercise7_2_hybrid_search_solved.py
from langchain_core.documents import Document

doc_dict = {
    "alpha": Document(page_content="Policy Alpha-X99: Passwords must contain numbers."),
    "beta": Document(page_content="Policy Beta-Y33: Multi-factor authentication is enabled."),
    "gamma": Document(page_content="Policy Gamma-Z22: Access restricted to corporate IP addresses.")
}

# Mock database search fallback function
def mock_db_search(query: str) -> list[Document]:
    print("[Vector Store Fallback]: Searching database semantically...")
    return [Document(page_content="Default corporate document fallback context.")]

# ================= SOLUTION WORK =================
def hybrid_retrieve(query: str, db_search_func) -> list[Document]:
    for key in ["alpha", "beta", "gamma"]:
        if key in query.lower():
            print(f"[Hybrid Router]: Match found for keyword '{key}'! Routing to exact document.")
            return [doc_dict[key]]
    
    # Fallback to semantic search
    return db_search_func(query)
# ================================================

# Test Case 1: Keyword query
print("Querying exact keyword 'What is Policy Beta?':")
result1 = hybrid_retrieve("What is Policy Beta?", mock_db_search)
print(f"Result: {result1[0].page_content}")

# Test Case 2: General query (fallback)
print("\nQuerying general request 'How do I secure my login?':")
result2 = hybrid_retrieve("How do I secure my login?", mock_db_search)
print(f"Result: {result2[0].page_content}")
