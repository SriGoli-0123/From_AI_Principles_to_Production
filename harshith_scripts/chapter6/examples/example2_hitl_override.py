# example2_hitl_override.py
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

class ReportState(TypedDict):
    recipient: str
    message: str

def generate_draft(state: ReportState) -> dict:
    return {"message": "Draft payload: Critical alert."}

def send_report(state: ReportState) -> dict:
    print(f"\n[Sender]: Message sent to {state['recipient']}!")
    print(f"Payload: '{state['message']}'")
    return {}

workflow = StateGraph(ReportState)
workflow.add_node("drafter", generate_draft)
workflow.add_node("sender", send_report)

workflow.add_edge(START, "drafter")
workflow.add_edge("drafter", "sender")
workflow.add_edge("sender", END)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory, interrupt_before=["sender"])

config = {"configurable": {"thread_id": "session_A"}}

# Trigger draft generation
app.invoke({"recipient": "ceo@company.com", "message": ""}, config)

# execution pauses. Print state
current_state = app.get_state(config)
print(f"\nDraft complete: recipient={current_state.values.get('recipient')}")
print(f"Message content: {current_state.values.get('message')}")

# Operator decides to edit the recipient before execution runs
new_recipient = "security_lead@company.com"
print(f"\n[Human Override]: Changing recipient to: {new_recipient}")

# Overwrite state variables
app.update_state(config, {"recipient": new_recipient})

# Resume execution
print("\nResuming sender...")
app.invoke(None, config)
