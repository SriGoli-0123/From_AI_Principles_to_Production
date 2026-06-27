# example1_draft_critic.py
import os
import json
from typing import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

# Define Graph State
class ReflectionState(TypedDict):
    draft: str
    critique: str
    retry_count: int

# Initialize model
if os.environ.get("OPENAI_API_KEY"):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
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
        temperature=0.2
    )

# Node 1: Generator
def generator_node(state: ReflectionState) -> dict:
    print(f"\n[Writer Node]: Drafting response... (Attempt {state.get('retry_count', 0) + 1})")
    
    prompt = (
        "Write a concise summary of the benefits of renewable energy. "
        "It must be exactly two sentences long."
    )
    if state.get("critique"):
        prompt += f"\n\nPrevious Critique to address:\n{state['critique']}"
        
    response = llm.invoke(prompt)
    return {"draft": response.content, "retry_count": state.get("retry_count", 0) + 1}

# Node 2: Critic (LLM self-reflection)
def critic_node(state: ReflectionState) -> dict:
    print("\n[Critic Node]: Evaluating draft against instructions...")
    draft = state["draft"]
    
    critique_prompt = (
        "Evaluate the following summary against these rules:\n"
        "1. Must discuss renewable energy benefits.\n"
        "2. Must be exactly two sentences long.\n\n"
        f"Draft: {draft}\n\n"
        "If it violates any rule, output 'FAIL: [detailed explanation of violation]'. "
        "If it is correct, output 'PASS'."
    )
    
    response = llm.invoke(critique_prompt)
    print(f"[Critic Node] Evaluation: {response.content}")
    return {"critique": response.content}

# Conditional edge routing logic
def router(state: ReflectionState) -> str:
    if "PASS" in state["critique"] or state["retry_count"] >= 3:
        print("[Router]: Process complete. Terminating.")
        return END
    print("[Router]: Critique failed. Routing to retry...")
    return "writer"

# Assemble Graph
workflow = StateGraph(ReflectionState)
workflow.add_node("writer", generator_node)
workflow.add_node("critic", critic_node)

workflow.add_edge(START, "writer")
workflow.add_edge("writer", "critic")
workflow.add_conditional_edges(
    "critic",
    router,
    {
        "writer": "writer",
        END: END
    }
)

app = workflow.compile()

# Execute
print(f"Running Draft-Critic loop using model: {model_name}...")
app.invoke({"draft": "", "critique": "", "retry_count": 0})
