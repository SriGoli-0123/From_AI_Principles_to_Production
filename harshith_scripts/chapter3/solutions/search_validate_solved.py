# exercise3_2_search_validate_solved.py
import os
import json
from openai import OpenAI

records = {
    101: "User profile details",
    102: "Payment gateway options",
    103: "Critical system event log containing key information"
}

# ================= SOLUTION WORK =================
def get_record(record_id: int) -> tuple[str, bool]:
    if record_id not in records:
        return f"Failure: Record ID {record_id} not found in database.", False
    return f"Success: Found record: {records[record_id]}", True

# Define tool schema for OpenAI
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_record",
            "description": "Fetches a database record by its ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "record_id": {
                        "type": "integer",
                        "description": "The record ID to query"
                    }
                },
                "required": ["record_id"]
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
    {
        "role": "system", 
        "content": (
            "You are a database auditor. Query record IDs starting from 100\n"
            "sequentially until you find a record containing the word 'critical'.\n"
            "Once found, stop and output the content of that record."
        )
    },
    {"role": "user", "content": "Begin audit."}
]

print(f"Starting ReAct Search Loop using model: {model_name}...")
for step in range(5):
    print(f"\n--- Audit Step {step + 1} ---")
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        tools=tools
    )
    msg = response.choices[0].message
    messages.append(msg)
    
    if msg.tool_calls:
        for tc in msg.tool_calls:
            print(f"Model calls: {tc.function.name} with args: {tc.function.arguments}")
            
            if tc.function.name == 'get_record':
                args = json.loads(tc.function.arguments)
                outcome, success = get_record(args.get("record_id", 0))
                print(f"[Database]: success={success} | result={outcome}")
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "name": tc.function.name,
                    "content": outcome
                })
    else:
        print(f"\nAudit Final Response:\n{msg.content}")
        break
# ================================================
