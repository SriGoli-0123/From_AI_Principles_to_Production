# exercise8_1_shared_rag_lookup_solved.py
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class OrchestrationState(TypedDict):
    query: str
    rag_output: str
    final_output: str

def supervisor_node(state: OrchestrationState) -> dict:
    print("[Supervisor]: Delegating task to RAG Worker...")
    return {}

def rag_worker(state: OrchestrationState) -> dict:
    print("[RAG Worker]: Checking index...")
    # Mock result (simulate "not found")
    if "password" in state["query"].lower():
        return {"rag_output": "Passwords must be 12 chars long."}
    return {"rag_output": "Error: Policy details not found in index."}

def writer_worker(state: OrchestrationState) -> dict:
    print("[Writer Worker]: Formatting final answer...")
    return {"final_output": f"Answer formatted: {state['rag_output']}"}

def escalation_worker(state: OrchestrationState) -> dict:
    print("[Escalation Worker]: Alerting human supervisors about missing info.")
    return {"final_output": "Escalated: No policy records found."}

# ================= SOLUTION WORK =================
def route_rag_result(state: OrchestrationState) -> str:
    if "not found" in state.get("rag_output", "").lower():
        print("[Router]: RAG search returned 'not found'. Directing to escalation_worker...")
        return "escalation"
    print("[Router]: RAG search successful. Directing to writer_worker...")
    return "writer"

workflow = StateGraph(OrchestrationState)
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("rag_worker", rag_worker)
workflow.add_node("writer_worker", writer_worker)
workflow.add_node("escalation_worker", escalation_worker)

workflow.add_edge(START, "supervisor")
workflow.add_edge("supervisor", "rag_worker")
workflow.add_conditional_edges(
    "rag_worker",
    route_rag_result,
    {
        "writer": "writer_worker",
        "escalation": "escalation_worker"
    }
)
workflow.add_edge("writer_worker", END)
workflow.add_edge("escalation_worker", END)

app = workflow.compile()
# ================================================

print("--- Test Case 1 (Successful lookup) ---")
res1 = app.invoke({"query": "What are password requirements?", "rag_output": "", "final_output": ""})
print(f"Outcome: {res1.get('final_output')}")

print("\n--- Test Case 2 (Failed lookup) ---")
res2 = app.invoke({"query": "How many coffee machines do we have?", "rag_output": "", "final_output": ""})
print(f"Outcome: {res2.get('final_output')}")
