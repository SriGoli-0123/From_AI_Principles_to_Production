# exercise9_2_budget_limit_solved.py
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class CodeState(TypedDict):
    code_solution: str
    execution_error: str
    attempts: int

class ReflectionBudgetExceededError(Exception):
    pass

def coder_node(state: CodeState) -> dict:
    attempts = state.get("attempts", 0) + 1
    print(f"\n[Coder]: Coding attempt {attempts}...")
    # Node always fails to test the budget router raise exception behavior
    return {"code_solution": "print(x)", "execution_error": "NameError: name 'x' is not defined", "attempts": attempts}

# ================= SOLUTION WORK =================
def budget_router(state: CodeState) -> str:
    # If error exists and attempts >= 3, raise custom exception
    if state.get("execution_error") and state.get("attempts", 0) >= 3:
        raise ReflectionBudgetExceededError(
            f"ReflectionBudgetExceededError: Self-correction budget exceeded after {state['attempts']} attempts. "
            f"Last execution error: {state['execution_error']}"
        )
    
    if not state.get("execution_error"):
        print("[Router]: Success. Terminating.")
        return END
        
    print("[Router]: Error present. Budget not met. Re-routing back to coder...")
    return "coder"

# Assemble Graph
workflow = StateGraph(CodeState)
workflow.add_node("coder", coder_node)

workflow.add_edge(START, "coder")
workflow.add_conditional_edges(
    "coder",
    budget_router,
    {
        "coder": "coder",
        END: END
    }
)

app = workflow.compile()
# ================================================

print("Starting budget-aware code generation loop...")
try:
    app.invoke({"code_solution": "", "execution_error": "Initial failure trigger", "attempts": 0})
except ReflectionBudgetExceededError as e:
    print(f"\n[System Log]: Successfully caught expected exception:\n{e}")
