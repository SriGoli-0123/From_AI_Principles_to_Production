# example1_minimal_graph.py
from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END

# 1. Define the shared state structure
class GraphState(TypedDict):
    # Annotating with 'add' means new data will be appended to the list
    log: Annotated[list[str], add]

# 2. Define the nodes (deterministic Python functions)
def first_node(state: GraphState) -> dict:
    print("[Node 1]: Processing...")
    return {"log": ["First Node processed"]}

def second_node(state: GraphState) -> dict:
    print("[Node 2]: Processing...")
    return {"log": ["Second Node processed"]}

# 3. Build the graph structure
workflow = StateGraph(GraphState)

# Add nodes to graph
workflow.add_node("node_one", first_node)
workflow.add_node("node_two", second_node)

# Connect nodes with edges
workflow.add_edge(START, "node_one")
workflow.add_edge("node_one", "node_two")
workflow.add_edge("node_two", END)

# 4. Compile the state machine
app = workflow.compile()

print("Executing graph...")
final_state = app.invoke({"log": ["Initialization"]})
print(f"Final State Log: {final_state['log']}")
