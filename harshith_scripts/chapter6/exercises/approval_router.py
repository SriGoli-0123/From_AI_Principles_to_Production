# exercise6_2_approval_router.py
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# TODO: Complete this exercise by adding a conditional edge router that checks
# the state["approved"] key. If approved is True, route to execute_action;
# otherwise, route to END.
