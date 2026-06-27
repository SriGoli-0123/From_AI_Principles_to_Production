# exercise10_1_precision.py
from langchain_core.documents import Document

# TODO: Complete the calculate_precision_k(results, expected_source) function.
# - Loop through each document in the 'results' list.
# - Count how many documents have a metadata 'source_id' that equals the expected_source.
# - Calculate and return the precision percentage: (hits / len(results)) * 100.
def calculate_precision_k(results: list[Document], expected_source: str) -> float:
    pass
