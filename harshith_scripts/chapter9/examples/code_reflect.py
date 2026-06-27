# example2_code_reflect.py
import os
import sys
import io
import json
from typing import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

class CodeState(TypedDict):
    code_solution: str
    execution_error: str
    attempts: int

# Initialize model
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

# Coder Node
def coder_node(state: CodeState) -> dict:
    print(f"\n[Coder Node]: Writing script... (Attempt {state.get('attempts', 0) + 1})")
    
    prompt = (
        "Write a Python script that defines a variable 'my_list = [10, 20, 30]' and "
        "prints the average. Output ONLY executable Python code, no markdown wrappers."
    )
    if state.get("execution_error"):
        prompt += f"\n\nYour previous code failed with the following traceback error:\n{state['execution_error']}\nFix this error."
        
    response = llm.invoke(prompt)
    # Strip any potential markdown wrappers if the LLM disobeys instructions
    clean_code = response.content.replace("```python", "").replace("```", "").strip()
    return {"code_solution": clean_code, "attempts": state.get("attempts", 0) + 1}

# Deterministic validator node (runs code inside Python exec environment)
def execution_node(state: CodeState) -> dict:
    print("\n[Executor Node]: Running code...")
    code = state["code_solution"]
    
    # Redirect stdout to capture prints
    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()
    
    error_msg = ""
    try:
        # Execute generated code
        exec_globals = {}
        exec(code, exec_globals)
        print(f"Output: {buffer.getvalue().strip()}")
    except Exception as e:
        error_msg = f"Runtime Error: {type(e).__name__}: {str(e)}"
        print(f"Error caught: {error_msg}")
    finally:
        sys.stdout = old_stdout
        
    return {"execution_error": error_msg}

# Routing logic
def audit_router(state: CodeState) -> str:
    if not state["execution_error"] or state["attempts"] >= 3:
        return END
    return "coder"

workflow = StateGraph(CodeState)
workflow.add_node("coder", coder_node)
workflow.add_node("executor", execution_node)

workflow.add_edge(START, "coder")
workflow.add_edge("coder", "executor")
workflow.add_conditional_edges(
    "executor",
    audit_router,
    {
        "coder": "coder",
        END: END
    }
)

app = workflow.compile()

# Intentionally introduce error by forcing initial bad execution state to demonstrate recovery
print(f"Running Code-Reflection loop using model: {model_name}...")
app.invoke({"code_solution": "print(my_list[5])", "execution_error": "IndexError: list index out of range", "attempts": 1})
