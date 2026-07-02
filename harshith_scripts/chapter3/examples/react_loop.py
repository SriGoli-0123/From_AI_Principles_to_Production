# react_loop.py
import os
import json
from openai import OpenAI

# 1. Define a local deterministic tool function
def read_local_file(filepath: str) -> str:
    if not os.path.exists(filepath):
        return f"Error: File '{filepath}' not found."
    try:
        with open(filepath, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error: Cannot read file. Details: {str(e)}"

tool_registry = {"read_local_file": read_local_file}

# 2. Define the tool schema for the API
tools = [
    {
        "type": "function",
        "function": {
            "name": "read_local_file",
            "description": "Reads the contents of a local text file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "The path to the file to read"
                    }
                },
                "required": ["filepath"]
            }
        }
    }
]

# Connect to local Ollama (run 'ollama run llama3' first)
if os.environ.get("OPENAI_API_KEY"):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    model_name = "gpt-4o-mini"
else:
    client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
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

# Setup dummy files for testing
with open("directory.txt", "w") as f:
    f.write("The secret code is hidden in secret.txt")
with open("secret.txt", "w") as f:
    f.write("SecretCode_99")

# Message history
messages = [
    {"role": "system", "content": "You are a file lookup agent. Use the tools provided to find the secret code."},
    {"role": "user", "content": "Read directory.txt first to locate the secret code, then read that file and output the code."}
]

print(f"Starting ReAct Loop using model: {model_name}...")
step = 0
while step < 5:
    step += 1
    print(f"\n--- ReAct Step {step} ---")
    
    # Send history to model
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        tools=tools
    )
    
    msg = response.choices[0].message
    messages.append(msg)
    
    # Check if model completed the task or needs tool execution
    if msg.tool_calls:
        for tool_call in msg.tool_calls:
            print(f"Agent calls tool: {tool_call.function.name} with args: {tool_call.function.arguments}")
            
            # Execute tool locally in Python
            if tool_call.function.name == 'read_local_file':
                args = json.loads(tool_call.function.arguments)
                obs = read_local_file(args.get("filepath", ""))
                print(f"Observation: {obs}")
                
                # Append observation to history as tool message
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_call.function.name,
                    "content": str(obs)
                })
    else:
        print(f"\nAgent Final Answer: {msg.content}")
        break
else:
    print("[System]: Loop hit step limit without finishing.")

# Clean up local dummy files
if os.path.exists("directory.txt"):
    os.remove("directory.txt")
if os.path.exists("secret.txt"):
    os.remove("secret.txt")
