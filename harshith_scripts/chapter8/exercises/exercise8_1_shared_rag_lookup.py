# exercise8_1_shared_rag_lookup.py
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class OrchestrationState(TypedDict):
    query: str
    rag_output: str
    final_output: str

# TODO: Define a conditional router check function route_rag_result(state)
# - If "not found" (case insensitive) is inside state["rag_output"], route to "escalation_worker".
# - Otherwise, route to "writer_worker".
def route_rag_result(state: OrchestrationState) -> str:
    pass
