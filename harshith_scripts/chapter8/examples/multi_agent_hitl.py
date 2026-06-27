# example2_multi_agent_hitl.py
import sys
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

class OrchestrationState(TypedDict):
    user_request: str
    assigned_worker: str
    worker_log: str

# Nodes
def supervisor_router(state: OrchestrationState) -> dict:
    print("\n[Supervisor]: Assessing task routing...")
    return {"assigned_worker": "email_worker"}

def email_worker(state: OrchestrationState) -> dict:
    print(f"\n[Email Worker]: Executing assigned task. Logged action.")
    return {"worker_log": "Alert email dispatched."}

def support_worker(state: OrchestrationState) -> dict:
    print(f"\n[Support Worker]: Handling escalation support ticket.")
    return {"worker_log": "Support ticket created."}

# Routing function
def check_assignment(state: OrchestrationState) -> str:
    return state["assigned_worker"]

workflow = StateGraph(OrchestrationState)
workflow.add_node("supervisor", supervisor_router)
workflow.add_node("email_worker", email_worker)
workflow.add_node("support_worker", support_worker)

workflow.add_edge(START, "supervisor")
workflow.add_conditional_edges(
    "supervisor",
    check_assignment,
    {
        "email_worker": "email_worker",
        "support_worker": "support_worker"
    }
)
workflow.add_edge("email_worker", END)
workflow.add_edge("support_worker", END)

# In-memory checkpointer to pause execution
memory = MemorySaver()

# Interrupt BEFORE running the worker nodes
app = workflow.compile(
    checkpointer=memory,
    interrupt_before=["email_worker", "support_worker"]
)

config = {"configurable": {"thread_id": "session_B"}}
initial_input = {"user_request": "System crashed! We need support immediately.", "assigned_worker": "", "worker_log": ""}

print("Running supervisor routing stage...")
app.invoke(initial_input, config)

# Check state
current_state = app.get_state(config)
print(f"\n[Interrupt Gate]: Supervisor assigned task to worker: '{current_state.values.get('assigned_worker')}'")

# Human operator intervenes (auto-override flag for non-interactive runner)
if len(sys.argv) > 1 and sys.argv[1] == "--auto-override":
    override = "yes"
else:
    override = input("Override assignment? Type 'yes' to redirect to support: ").strip().lower()

if override == "yes":
    print("\n[Human Override]: Redirecting routing path to 'support_worker'...")
    app.update_state(config, {"assigned_worker": "support_worker"})

# Resume execution
print("\nResuming execution thread...")
final_output = app.invoke(None, config)
print(f"Final Execution Output Log: {final_output.get('worker_log')}")
