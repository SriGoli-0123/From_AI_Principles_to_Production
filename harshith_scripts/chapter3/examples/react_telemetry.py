# example2_react_telemetry.py
import json
import os
from openai import OpenAI

# Pure Python execution layer with telemetry
def execute_save_config(filename: str, content: str) -> tuple[str, bool]:
    if not filename.endswith(".json"):
        return "Failure: Filename must end with '.json' suffix.", False
    try:
        with open(filename, "w") as f:
            f.write(content)
        return "Success: Config saved.", True
    except Exception as e:
        return f"Failure: {str(e)}", False

# Define tool schema for the API
tools = [
    {
        "type": "function",
        "function": {
            "name": "save_config",
            "description": "Saves configuration content to a settings file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The target filename, must end in .json"
                    },
                    "content": {
                        "type": "string",
                        "description": "The configuration text to write"
                    }
                },
                "required": ["filename", "content"]
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

messages = [
    {"role": "system", "content": "You are a system manager. Always save your configs to settings.json"},
    {"role": "user", "content": "Save the host IP: '192.168.1.1' to config.txt"}
]

print(f"Starting Telemetry ReAct Loop using model: {model_name}...")
for step in range(5):
    print(f"\n--- Step {step + 1} ---")
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            tools=tools
        )
    except Exception as e:
        print(f"API Error: {e}")
        break
        
    msg = response.choices[0].message
    messages.append(msg)
    
    if msg.tool_calls:
        for tc in msg.tool_calls:
            print(f"Model calls: {tc.function.name} with args: {tc.function.arguments}")
            
            if tc.function.name == 'save_config':
                args = json.loads(tc.function.arguments)
                outcome, success = execute_save_config(
                    filename=args.get("filename", ""), 
                    content=args.get("content", "")
                )
                print(f"[Telemetry]: success={success} | details={outcome}")
                
                # Append telemetry result as tool response
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "name": tc.function.name,
                    "content": outcome
                })
    else:
        print(f"\nFinal Response: {msg.content}")
        break

# Clean up local settings file if it was created
if os.path.exists("settings.json"):
    os.remove("settings.json")
