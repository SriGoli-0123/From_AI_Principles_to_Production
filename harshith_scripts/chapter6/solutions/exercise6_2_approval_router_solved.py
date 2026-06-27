# exercise6_2_approval_router_solved.py
import sys
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

class SimpleState(TypedDict):
    input_text: str
    action_item: str
    approved: bool

def agent_node(state: SimpleState) -> dict:
    return {"action_item": "RESTART_MAIN_SERVER"}

def execute_action(state: SimpleState) -> dict:
    print(f"\n[Execution Node]: Running critical operation: {state['action_item']}")
    return {}

# ================= SOLUTION WORK =================
def approval_router(state: SimpleState) -> str:
    if state.get("approved"):
        print("[Router]: Operation approved. Directing to executor...")
        return "executor"
    print("[Router]: Operation rejected by human! Routing to END.")
    return END

# Build Graph
workflow = StateGraph(SimpleState)
workflow.add_node("agent", agent_node)
workflow.add_node("executor", execute_action)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges(
    "agent",
    approval_router,
    {
        "executor": "executor",
        END: END
    }
)
workflow.add_edge("executor", END)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory, interrupt_before=["executor"])
# ================================================

config = {"configurable": {"thread_id": "session_B"}}

print("Starting critical action graph...")
app.invoke({"input_text": "Maintenance check", "action_item": "", "approved": False}, config)

# execution pauses at the interrupt boundary before executor
state = app.get_state(config)
print(f"\nExecution PAUSED. Next node: {state.next}")

# Simulate User Response: Rejecting the action
print("\n[Human Operator]: Rejecting the action (approved=False)...")
app.update_state(config, {"approved": False})

# Resume
print("Resuming graph...")
app.invoke(None, config)
