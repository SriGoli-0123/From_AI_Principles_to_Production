# exercise6_1_escalation_solved.py
import sys
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

class AuditState(TypedDict):
    task: str
    success: bool
    feedback: str

def agent_node(state: AuditState) -> dict:
    return {"task": "Write to Database"}

def update_db_node(state: AuditState) -> dict:
    print("[Database]: Writing database records... FAILED.")
    return {"success": False}

# ================= SOLUTION WORK =================
def escalate_node(state: AuditState) -> dict:
    print("\n[Escalation Node]: Critical warning issued. Awaiting human correction...")
    # System waits for the operator to override parameters or give feedback
    return {"feedback": "Developer intervened and resolved conflict."}

def database_router(state: AuditState) -> str:
    if state.get("success"):
        print("[Router]: Database write successful. Completing task.")
        return END
    print("[Router]: Database write failed! Routing to escalation_node...")
    return "escalate_node"

# Build Graph
workflow = StateGraph(AuditState)
workflow.add_node("agent", agent_node)
workflow.add_node("update_db", update_db_node)
workflow.add_node("escalate_node", escalate_node)

workflow.add_edge(START, "agent")
workflow.add_edge("agent", "update_db")
workflow.add_conditional_edges(
    "update_db",
    database_router,
    {
        "escalate_node": "escalate_node",
        END: END
    }
)
workflow.add_edge("escalate_node", END)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory, interrupt_before=["escalate_node"])
# ================================================

config = {"configurable": {"thread_id": "audit_session_1"}}

print("Starting audit execution...")
app.invoke({"task": "", "success": False, "feedback": ""}, config)

# Paused at escalate_node
state = app.get_state(config)
print(f"\nExecution PAUSED. Next node to execute: {state.next}")

# Simulate intervention (resuming)
print("\n[Operator]: Resuming execution...")
app.invoke(None, config)

# Print final state
final_state = app.get_state(config)
print(f"\nFinal State Feedback: {final_state.values.get('feedback')}")
