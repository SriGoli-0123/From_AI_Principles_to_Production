# exercise9_1_math_verifier_solved.py
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class MathState(TypedDict):
    equation: str
    solution: str
    verified: bool
    attempts: int

def solver_node(state: MathState) -> dict:
    attempts = state.get("attempts", 0) + 1
    print(f"\n[Solver]: Solving equation: {state['equation']} (Attempt {attempts})...")
    # First attempt writes standard text, second attempt wraps in \boxed{}
    if attempts == 1:
        solution = "42"
    else:
        solution = "\\boxed{42}"
    return {"solution": solution, "attempts": attempts}

# ================= SOLUTION WORK =================
def verify_format(solution: str) -> bool:
    # Check if the solution is wrapped inside \boxed{...}
    return "\\boxed{" in solution and solution.endswith("}")

def validator_node(state: MathState) -> dict:
    sol = state.get("solution", "")
    is_valid = verify_format(sol)
    print(f"[Validator]: Inspecting solution format... Result: {is_valid}")
    return {"verified": is_valid}

def route_verifier(state: MathState) -> str:
    if state.get("verified") or state.get("attempts", 0) >= 3:
        print("[Router]: Terminating. Verifier passed or retry budget met.")
        return END
    print("[Router]: Verification failed! Routing back to solver...")
    return "solver"

# Assemble Graph
workflow = StateGraph(MathState)
workflow.add_node("solver", solver_node)
workflow.add_node("validator", validator_node)

workflow.add_edge(START, "solver")
workflow.add_edge("solver", "validator")
workflow.add_conditional_edges(
    "validator",
    route_verifier,
    {
        "solver": "solver",
        END: END
    }
)

app = workflow.compile()
# ================================================

print("Starting math validator agent...")
app.invoke({"equation": "x + 2 = 44", "solution": "", "verified": False, "attempts": 0})
