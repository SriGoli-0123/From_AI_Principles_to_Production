# example1_sliding_window.py

def trim_message_history(messages: list, keep_last_n: int) -> list:
    """Trims message history, keeping the system prompt and the last N messages."""
    system_messages = [msg for msg in messages if msg.get("role") == "system"]
    non_system_messages = [msg for msg in messages if msg.get("role") != "system"]
    
    if len(non_system_messages) <= keep_last_n:
        return messages
        
    # Prune non-system messages
    trimmed_history = non_system_messages[-keep_last_n:]
    
    # Reassemble with the system instruction at the head
    return system_messages + trimmed_history

# Mock a bloated chat history
history = [
    {"role": "system", "content": "You are a calculator agent."},
    {"role": "user", "content": "Add 2 and 2"},
    {"role": "assistant", "content": "Result is 4"},
    {"role": "user", "content": "Multiply that by 3"},
    {"role": "assistant", "content": "Result is 12"},
    {"role": "user", "content": "Subtract 5"},
    {"role": "assistant", "content": "Result is 7"}
]

print(f"Original history length: {len(history)} messages.")
trimmed = trim_message_history(history, keep_last_n=3)
print(f"Trimmed history length: {len(trimmed)} messages.")

print("\n--- Trimmed Context Structure ---")
for i, msg in enumerate(trimmed):
    print(f"[{i}] {msg['role']}: {msg['content']}")
