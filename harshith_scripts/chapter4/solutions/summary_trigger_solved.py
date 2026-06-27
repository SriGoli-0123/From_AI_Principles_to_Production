# exercise4_2_summary_trigger_solved.py
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
    except Exception:
        return "Summary generation failed."

def manage_summary_trigger(messages: list, running_summary: str) -> tuple[list, str]:
    # Extract system and non-system messages
    system_messages = [m for m in messages if m.get("role") == "system"]
    raw_messages = [m for m in messages if m.get("role") != "system"]
    
    # If the non-system message history is greater than 6, summarize the first 4
    if len(raw_messages) > 6:
        print("\n[Memory System]: Pruning limit hit! Summarizing the oldest 4 messages...")
        to_summarize = raw_messages[:4]
        remaining = raw_messages[4:]
        
        # Generate new summary
        new_summary = generate_summary(to_summarize, running_summary)
        
        # Construct summary instruction message
        summary_instruction = {
            "role": "system",
            "content": f"Here is a summary of facts from the conversation so far: {new_summary}"
        }
        
        # Reassemble
        new_messages = system_messages + [summary_instruction] + remaining
        return new_messages, new_summary
        
    return messages, running_summary

# Mock a conversation that grows step-by-step
conversation = [
    {"role": "system", "content": "You are a customer support agent."},
    {"role": "user", "content": "My order number is #4939"},
    {"role": "assistant", "content": "Thank you, order #4939 found."},
    {"role": "user", "content": "I purchased a red backpack"},
    {"role": "assistant", "content": "Understood, order contains one red backpack."},
    {"role": "user", "content": "It has not arrived yet"},
    {"role": "assistant", "content": "I apologize, shipping is currently delayed."},
    # At this point, we have 6 non-system messages
]

running_summary = ""

print(f"Initial non-system message count: {len([m for m in conversation if m['role'] != 'system'])}")
conversation, running_summary = manage_summary_trigger(conversation, running_summary)

# Let's add 2 more messages to trigger the pruning (now total 8 non-system)
conversation.append({"role": "user", "content": "Can I get a refund instead?"})
conversation.append({"role": "assistant", "content": "Let me check our refund policy."})

print(f"\nNon-system message count after additions: {len([m for m in conversation if m['role'] != 'system'])}")
conversation, running_summary = manage_summary_trigger(conversation, running_summary)

print(f"\nFinal memory summary: {running_summary}")
print("\nFinal message history structure:")
for i, msg in enumerate(conversation):
    print(f"[{i}] {msg['role']}: {msg['content'][:60]}...")
