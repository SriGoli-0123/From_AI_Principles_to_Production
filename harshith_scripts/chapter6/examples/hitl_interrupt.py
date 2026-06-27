# example1_hitl_interrupt.py
import sys
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

# 1. Define State and Nodes
class SimpleState(TypedDict):
    input_text: str
    action_item: str
    approved: bool

def agent_node(state: SimpleState) -> dict:
    print("\n[Agent Node]: Planning task...")
    return {"action_item": "DELETE_CONFIG_FILE"}

def execute_action(state: SimpleState) -> dict:
    print(f"\n[Execution Node]: Running: {state['action_item']}")
    return {"approved": True}

# 2. Build and Compile Graph with Checkpointer
workflow = StateGraph(SimpleState)
workflow.add_node("agent", agent_node)
workflow.add_node("executor", execute_action)

workflow.add_edge(START, "agent")
workflow.add_edge("agent", "executor")
workflow.add_edge("executor", END)

# In-memory checkpointer to persist state history
memory = MemorySaver()

# Compile with interrupt before executor node
app = workflow.compile(
    checkpointer=memory,
    interrupt_before=["executor"]
)

# 3. Running the interrupted program
config = {"configurable": {"thread_id": "1"}}
print("Starting execution...")

# First run: Stops at the interrupt boundary
events = app.stream({"input_text": "Clean server config"}, config)
for event in events:
    print(f"Graph Log: {event}")

# The graph is now paused. Inspect state:
state = app.get_state(config)
print(f"\nGraph is PAUSED. Current proposed action: {state.values.get('action_item')}")

# Programmatic intervention loop (or automatic default for non-interactive test)
if len(sys.argv) > 1 and sys.argv[1] == "--auto-approve":
    user_approval = "yes"
else:
    user_approval = input("Type 'yes' to approve action: ").strip().lower()

if user_approval == "yes":
    print("\nResuming graph execution...")
    # Resuming with None tells the checkpointer to continue from the saved thread
    events = app.stream(None, config)
    for event in events:
         print(f"Graph Log: {event}")
else:
    print("\n[System]: Action rejected. Aborting execution.")
