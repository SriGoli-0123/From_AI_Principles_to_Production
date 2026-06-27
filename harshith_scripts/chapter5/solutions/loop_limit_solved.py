# exercise5_2_loop_limit_solved.py
import os
import json
from typing import TypedDict, Annotated, Sequence
from operator import add
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

@tool
def calculate_square(number: int) -> int:
    """Calculates the square of an integer."""
    return number * number

tools = [calculate_square]
tool_node = ToolNode(tools)

# ================= SOLUTION WORK =================
# 2. Define state structure with counter
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add]
    counter: int # Keeps track of reasoning steps
# ================================================

# Initialize model bound to tools
if os.environ.get("OPENAI_API_KEY"):
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools(tools)
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
    model = ChatOpenAI(
        base_url=client_base_url,
        api_key="ollama",
        model=model_name,
        temperature=0
    ).bind_tools(tools)

# ================= SOLUTION WORK =================
# 4. Define node operations
def call_model(state: AgentState) -> dict:
    print(f"\n[Agent Node]: Invoking model (Step {state.get('counter', 0) + 1})...")
    response = model.invoke(state["messages"])
    # Increment counter state
    return {
        "messages": [response],
        "counter": state.get("counter", 0) + 1
    }

# Define conditional routing logic
def router(state: AgentState) -> str:
    # Safety Check: Limit steps to 3
    if state.get("counter", 0) >= 3:
        print("[Router]: Hard limit reached! Terminating loop to prevent infinite run.")
        return END
        
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        print("[Router]: Tool call detected. Directing to tools...")
        return "execute_tools"
    print("[Router]: No tools needed. Terminating graph.")
    return END
# ================================================

# Build Graph
workflow = StateGraph(AgentState)

workflow.add_node("agent", call_model)
workflow.add_node("execute_tools", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges(
    "agent",
    router,
    {
        "execute_tools": "execute_tools",
        END: END
    }
)
workflow.add_edge("execute_tools", "agent")

# Compile
app = workflow.compile()

# Invoke with counter initialized to 0
initial_state = {
    "messages": [
        SystemMessage(content="You are a calculation helper."),
        HumanMessage(content="What is the square of 12?")
    ],
    "counter": 0
}

print(f"Running LangGraph ReAct agent with loop limits using model: {model_name}...")
state_output = app.invoke(initial_state)
print(f"\nFinal Answer: {state_output['messages'][-1].content}")
