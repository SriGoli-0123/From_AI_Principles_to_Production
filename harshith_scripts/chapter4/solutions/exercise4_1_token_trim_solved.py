# exercise4_1_token_trim_solved.py

def trim_by_tokens(messages: list, max_tokens: int) -> list:
    char_limit = max_tokens * 4
    
    # Extract system messages
    system_messages = [m for m in messages if m.get("role") == "system"]
    non_system_messages = [m for m in messages if m.get("role") != "system"]
    
    # Base system cost
    system_char_count = sum(len(m.get("content", "")) for m in system_messages)
    
    if system_char_count >= char_limit:
        # System instructions alone exceed the budget! Keep only system.
        return system_messages
        
    current_char_count = system_char_count
    kept_non_system = []
    
    # Iterate from newest to oldest (reverse)
    for msg in reversed(non_system_messages):
        msg_len = len(msg.get("content", ""))
        if current_char_count + msg_len <= char_limit:
            kept_non_system.insert(0, msg) # Preserve original order
            current_char_count += msg_len
        else:
            break # Stop adding older messages
            
    return system_messages + kept_non_system

# Mock bloated chat history
history = [
    {"role": "system", "content": "System Instructions: Be helpful."},
    {"role": "user", "content": "Hello. I need to upload a very large report profile file to the main server database config folder."},
    {"role": "assistant", "content": "Ok. Send it."},
    {"role": "user", "content": "Report data content: " + "A"*500}, # Very large message
    {"role": "assistant", "content": "Successfully parsed and saved the report payload."}
]

print("Original message lengths:")
for msg in history:
    print(f"{msg['role']}: {len(msg['content'])} chars")

# Set token limit to 100 (which corresponds to 400 characters)
trimmed = trim_by_tokens(history, max_tokens=100)
print(f"\nTrimmed history message count: {len(trimmed)} (out of {len(history)})")
print("Remaining messages:")
for msg in trimmed:
    print(f"- {msg['role']}: {msg['content'][:60]}...")
