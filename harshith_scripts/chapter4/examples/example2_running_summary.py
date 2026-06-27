# example2_running_summary.py
import os
import json
from openai import OpenAI

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

def generate_summary(history_to_compress: list, current_summary: str = "") -> str:
    """Invokes a fast model to update a summary of the conversation history."""
    history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history_to_compress])
    
    summary_prompt = (
        f"Provide a concise summary of the conversation history. "
        f"Incorporate the previous summary if provided.\n\n"
        f"Previous Summary: {current_summary}\n\n"
        f"New Messages:\n{history_str}\n\n"
        f"Updated Summary:"
    )
    
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": summary_prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"[Error]: {e}")
        return "Memory summary failed."

# Simulate context migration
bloated_history = [
    {"role": "user", "content": "Hello, my name is Alex and I use a green laptop."},
    {"role": "assistant", "content": "Nice to meet you, Alex!"},
    {"role": "user", "content": "I need you to remember that my server IP is 192.168.1.50"},
    {"role": "assistant", "content": "Understood. Server IP is registered as 192.168.1.50."}
]

print("Generating running summary...")
running_summary = generate_summary(bloated_history)
print(f"\nSaved Working Memory: {running_summary}")

# Next execution uses system message containing the summary + new messages
system_prompt_with_memory = (
    "You are a system administrator.\n"
    f"Here is a summary of facts from the conversation so far: {running_summary}"
)

next_messages = [
    {"role": "system", "content": system_prompt_with_memory},
    {"role": "user", "content": "What is my server IP again?"}
]

try:
    final_response = client.chat.completions.create(
        model=model_name,
        messages=next_messages
    )
    print(f"\nAgent response using memory summary: {final_response.choices[0].message.content}")
except Exception as e:
    print(f"[Error]: {e}")
