# exercise8_2_validation_gate_solved.py
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class CodeState(TypedDict):
    code: str
    audit_passed: bool
    attempts: int

def coder_worker(state: CodeState) -> dict:
    attempts = state.get("attempts", 0) + 1
    print(f"\n[Coder Worker]: Writing python code (Attempt {attempts})...")
    # First attempt generates buggy code without 'def', second attempt writes valid code
    if attempts == 1:
        code_str = "print('Hello world')"
    else:
        code_str = "def hello(): print('Hello world')"
    return {"code": code_str, "attempts": attempts}

def auditor_worker(state: CodeState) -> dict:
    code = state.get("code", "")
    print(f"[Auditor Worker]: Inspecting code: '{code}'")
    # Code must contain 'def' to pass
    if "def" in code:
        print("[Auditor]: Validation PASSED.")
        return {"audit_passed": True}
    print("[Auditor]: Validation FAILED. No function definitions found.")
    return {"audit_passed": False}

# ================= SOLUTION WORK =================
def validation_router(state: CodeState) -> str:
    if state.get("audit_passed"):
        print("[Router]: Audit passed. Terminating graph.")
        return END
    print("[Router]: Audit failed! Re-routing back to coder_worker...")
    return "coder"

# Assemble Graph
workflow = StateGraph(CodeState)
workflow.add_node("coder", coder_worker)
workflow.add_node("auditor", auditor_worker)

workflow.add_edge(START, "coder")
workflow.add_edge("coder", "auditor")
workflow.add_conditional_edges(
    "auditor",
    validation_router,
    {
        "coder": "coder",
        END: END
    }
)

app = workflow.compile()
# ================================================

print("Starting validation loop...")
app.invoke({"code": "", "audit_passed": False, "attempts": 0})
