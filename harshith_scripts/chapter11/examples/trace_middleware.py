# example1_trace_middleware.py
import time
from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END

# State holding logs and data
class TelemetryState(TypedDict):
    data: str
    trace_log: Annotated[list[str], add]

# Custom tracing wrapper (Middleware pattern)
def trace_node(node_name: str, node_func):
    def wrapped_node(state: TelemetryState) -> dict:
        start_time = time.time()
        print(f"\n[Trace Monitor]: Entering Node '{node_name}'...")
        
        # Execute actual node logic
        result = node_func(state)
        
        duration = time.time() - start_time
        log_entry = f"Node '{node_name}' executed in {duration:.4f}s"
        print(f"[Trace Monitor]: Exited Node '{node_name}'. Duration: {duration:.4f}s")
        
        # Inject trace log output into state update
        if "trace_log" in result:
            result["trace_log"].append(log_entry)
        else:
            result["trace_log"] = [log_entry]
        return result
    return wrapped_node

# Node functions
def fetch_data(state: TelemetryState) -> dict:
    time.sleep(0.1)
    return {"data": "Row values: system_ok"}

def process_data(state: TelemetryState) -> dict:
    time.sleep(0.05)
    return {"data": state["data"].upper()}

# Build graph with wrapped telemetry nodes
workflow = StateGraph(TelemetryState)
workflow.add_node("fetcher", trace_node("fetcher", fetch_data))
workflow.add_node("processor", trace_node("processor", process_data))

workflow.add_edge(START, "fetcher")
workflow.add_edge("fetcher", "processor")
workflow.add_edge("processor", END)

app = workflow.compile()

# Execute
print("Triggering graph run with local tracing...")
final_output = app.invoke({"data": "", "trace_log": []})
print(f"\n--- Final Compiled Trace Log ---")
for log in final_output["trace_log"]:
    print(f" - {log}")
