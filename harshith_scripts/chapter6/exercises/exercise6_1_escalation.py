# exercise6_1_escalation.py
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
    # Simulates a database write failure
    print("[Database]: Writing database records... FAILED.")
    return {"success": False}

# TODO: Define escalate_node(state: AuditState) -> dict
# This node is triggered when database write fails. It should print a warning
# and wait for intervention.
def escalate_node(state: AuditState) -> dict:
    pass

# TODO: Set up the graph and add a conditional router from update_db_node:
# - If success is True, route to END.
# - If success is False, route to escalate_node.
# - Configure the graph to interrupt BEFORE executing escalate_node.
