# exercise8_2_validation_gate.py
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# TODO: Complete this exercise by adding a conditional edge router that checks
# state["audit_passed"]. If it is True, route to END.
# Otherwise, route the execution back to "coder_worker" to regenerate the code.
