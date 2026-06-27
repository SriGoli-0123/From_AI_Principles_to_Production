# example3_autonomous_share_agent.py
import os
import re
from openai import OpenAI

# Connect to local Ollama (run 'ollama run llama3' first)
if os.environ.get("OPENAI_API_KEY"):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    model_name = "gpt-4o-mini"
else:
    client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    model_name = "llama3"
    # Fallback: dynamically pick any installed local model if llama3 isn't available
    try:
        import urllib.request
        import json
        with urllib.request.urlopen("http://localhost:11434/api/tags") as response:
            data = json.loads(response.read().decode())
            models = [m["name"] for m in data.get("models", [])]
            if models and model_name not in models:
                preferred = [m for m in models if "llama3" in m]
                model_name = preferred[0] if preferred else models[0]
    except Exception:
        pass

# 1. Define the tool
def get_weather(location):
    return f"The weather in {location} is 72 degrees and sunny."

tool_registry = {"get_weather": get_weather}

# 2. Main Memory (Message History)
messages = [
    {
        "role": "system", 
        "content": (
            "You are a weather agent. To fetch weather, output exactly:\n"
            "CALL: get_weather(location)\n"
            "When you have the final answer, output:\n"
            "STOP: [your final answer]"
        )
    },
    {"role": "user", "content": "What is the weather in Paris?"}
]

# 3. Main Feedback Control Loop
print("Starting weather agent loop...")
for step in range(3):
    print(f"\n--- Loop Step {step + 1} ---")
    try:
        response = client.chat.completions.create(model=model_name, messages=messages)
    except Exception as e:
        print("\n[Error]: Could not connect to API or run model.")
        print(f"Make sure local Ollama is running and '{model_name}' is downloaded.")
        print("Run: ollama pull llama3")
        raise e
        
    output = response.choices[0].message.content
    print(f"Agent Output: {output}")
    messages.append({"role": "assistant", "content": output})
    
    if "STOP:" in output:
        print("[System]: Task Complete. Halting.")
        break
    elif "CALL:" in output:
        # Extract function name and argument robustly handling spacing
        match = re.search(r"CALL\s*:\s*(\w+)\s*\(\s*([^)]+?)\s*\)", output)
        if match:
            func_name = match.group(1)
            arg = match.group(2).strip("'\" ")
            
            # Execute tool locally in Python
            print(f"[System]: Executing tool '{func_name}' with arg '{arg}'...")
            result = tool_registry[func_name](arg)
            print(f"Observation: {result}")
            
            # Feed result back into memory
            messages.append({"role": "user", "content": f"Observation: {result}"})
