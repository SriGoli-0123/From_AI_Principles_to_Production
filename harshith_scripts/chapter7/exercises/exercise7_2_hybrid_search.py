# exercise7_2_hybrid_search.py
from langchain_core.documents import Document

doc_dict = {
    "alpha": Document(page_content="Policy Alpha-X99: Passwords must contain numbers."),
    "beta": Document(page_content="Policy Beta-Y33: Multi-factor authentication is enabled."),
    "gamma": Document(page_content="Policy Gamma-Z22: Access restricted to corporate IP addresses.")
}

# TODO: Complete hybrid_retrieve(query: str, db_search_func)
# - Loop through the keys in ["alpha", "beta", "gamma"].
# - If the key is in the query (case insensitive), return that document from doc_dict immediately.
# - Otherwise, return the result of executing db_search_func(query).
def hybrid_retrieve(query: str, db_search_func) -> list[Document]:
    pass
