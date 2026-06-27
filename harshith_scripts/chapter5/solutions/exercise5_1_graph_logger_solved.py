# exercise5_1_graph_logger_solved.py
from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END

class GraphState(TypedDict):
    log: Annotated[list[str], add]

def first_node(state: GraphState) -> dict:
    return {"log": ["First Node processed"]}

# ================= SOLUTION WORK =================
def logger_node(state: GraphState) -> dict:
    print(f"\n[Logger Node]: Current State Log -> {state['log']}")
    return {} # Logger node doesn't modify state
# ================================================

def second_node(state: GraphState) -> dict:
    return {"log": ["Second Node processed"]}

workflow = StateGraph(GraphState)
workflow.add_node("node_one", first_node)
workflow.add_node("logger", logger_node)
workflow.add_node("node_two", second_node)

# ================= SOLUTION WORK =================
workflow.add_edge(START, "node_one")
workflow.add_edge("node_one", "logger")
workflow.add_edge("logger", "node_two")
workflow.add_edge("node_two", END)
# ================================================

app = workflow.compile()
print("Executing solved graph logger...")
app.invoke({"log": ["Initialization"]})
