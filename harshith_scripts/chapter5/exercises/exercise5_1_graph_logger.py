# exercise5_1_graph_logger.py
from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END

class GraphState(TypedDict):
    log: Annotated[list[str], add]

def first_node(state: GraphState) -> dict:
    return {"log": ["First Node processed"]}

# TODO: Define a logger_node function that receives state, prints the current state log to the console,
# and returns an empty dictionary (since it doesn't modify state).
def logger_node(state: GraphState) -> dict:
    pass

def second_node(state: GraphState) -> dict:
    return {"log": ["Second Node processed"]}

# TODO: Add the logger node to the graph and wire the edges so that the execution flow goes:
# START -> node_one -> logger -> node_two -> END
workflow = StateGraph(GraphState)
workflow.add_node("node_one", first_node)
workflow.add_node("node_two", second_node)

workflow.add_edge(START, "node_one")
workflow.add_edge("node_one", "node_two")
workflow.add_edge("node_two", END)

app = workflow.compile()
app.invoke({"log": ["Initialization"]})
