# exercise11_2_fallback_routing_solved.py
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class FallbackState(TypedDict):
    prompt: str
    response: str
    success: bool
    attempts: int

def small_model_node(state: FallbackState) -> dict:
    attempts = state.get("attempts", 0) + 1
    print(f"\n[Small Model Node]: Processing prompt... (Attempt {attempts})")
    # Simulate a parsing validation failure on small model
    return {"response": "Model response logic.", "success": False, "attempts": attempts}

def large_model_node(state: FallbackState) -> dict:
    print(f"\n[Large Model Node]: Escalate! Invoking larger reasoning model...")
    return {"response": "High-fidelity reasoning output.", "success": True}

# ================= SOLUTION WORK =================
def route_model(state: FallbackState) -> str:
    if state.get("success"):
        print("[Router]: Processing succeeded. Route to END.")
        return END
    print("[Router]: Small model failed parsing checks! Escalating to large_model_node...")
    return "large_model"

# Assemble Graph
workflow = StateGraph(FallbackState)
workflow.add_node("small_model", small_model_node)
workflow.add_node("large_model", large_model_node)

workflow.add_edge(START, "small_model")
workflow.add_conditional_edges(
    "small_model",
    route_model,
    {
        "large_model": "large_model",
        END: END
    }
)
workflow.add_edge("large_model", END)

app = workflow.compile()
# ================================================

print("Starting fallback router test...")
res = app.invoke({"prompt": "Calculate system parameters", "response": "", "success": False, "attempts": 0})
print(f"\nFinal State Success: {res.get('success')}")
print(f"Final State Response: '{res.get('response')}'")
