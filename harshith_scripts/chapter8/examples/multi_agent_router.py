# example1_multi_agent_router.py
import os
import json
from typing import TypedDict, Literal
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END

# Define routing destination schema
class RouterDecision(BaseModel):
    """Decide which specialist node is best suited for the task."""
    next_step: Literal["db_worker", "file_worker"] = Field(description="Target worker node")

# Define Graph State
class MultiAgentState(TypedDict):
    task: str
    worker_output: str

# Connect to local Ollama / OpenAI
if os.environ.get("OPENAI_API_KEY"):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    model_name = "gpt-4o-mini"
else:
    client_base_url = "http://localhost:11434/v1"
    model_name = "llama3"
    try:
        import urllib.request
        with urllib.request.urlopen("http://localhost:11434/api/tags") as response:
            data = json.loads(response.read().decode())
            models = [m["name"] for m in data.get("models", [])]
            if models and model_name not in models:
                preferred = [m for m in models if "llama3" in m]
                model_name = preferred[0] if preferred else models[0]
    except Exception:
        pass
    llm = ChatOpenAI(
        base_url=client_base_url,
        api_key="ollama",
        model=model_name,
        temperature=0
    )

router_llm = llm.with_structured_output(RouterDecision)

def supervisor_node(state: MultiAgentState) -> dict:
    print("\n[Supervisor]: Planning next routing step...")
    decision = router_llm.invoke(state["task"])
    print(f"[Supervisor]: Routing task to: {decision.next_step}")
    return {"worker_output": decision.next_step}

# Worker Nodes
def db_worker_node(state: MultiAgentState) -> dict:
    print("[DB Worker]: Querying database...")
    return {"worker_output": "Database query result: 20 active users."}

def file_worker_node(state: MultiAgentState) -> dict:
    print("[File Worker]: Saving file contents...")
    return {"worker_output": "File saved successfully."}

# Router edge evaluation
def route_edge(state: MultiAgentState) -> str:
    return state["worker_output"]

# Assemble Graph
workflow = StateGraph(MultiAgentState)
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("db_worker", db_worker_node)
workflow.add_node("file_worker", file_worker_node)

workflow.add_edge(START, "supervisor")
workflow.add_conditional_edges(
    "supervisor",
    route_edge,
    {
        "db_worker": "db_worker",
        "file_worker": "file_worker"
    }
)
workflow.add_edge("db_worker", END)
workflow.add_edge("file_worker", END)

app = workflow.compile()

# Invoke
print(f"Triggering DB request using model: {model_name}...")
app.invoke({"task": "Find how many users are active in the database", "worker_output": ""})
