# exercise1_2_prompt_test_runner_solved.py
import os
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

# ================= SOLUTION WORK =================
# We write a prompt that forces the LLM to output exactly 'PUBLIC' or 'PRIVATE' without any punctuation or explanations.
system_prompt = """
You are a classification assistant. Your task is to output exactly one of these two words:
- 'PUBLIC': if the message is intended to be shared openly or posted to a public timeline.
- 'PRIVATE': if the message is intended to be kept secure, hidden, or sent to a private inbox.

Do not include any greetings, explanation, sentences, or punctuation. Output exactly one word: either PUBLIC or PRIVATE.
"""
# ================================================

test_cases = [
    {"input": "Put this on my public Twitter timeline", "expected": "PUBLIC"},
    {"input": "Whisper this quietly to Sarah's private inbox", "expected": "PRIVATE"}
]

print(f"Running Exercise 1.2 solved script using model: {model_name}...")
for idx, case in enumerate(test_cases):
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": case["input"]}
            ]
        )
        result = response.choices[0].message.content.strip().upper()
        # Clean up punctuation if any small models outputted them
        result = result.replace(".", "").replace('"', '').replace("'", "")
        
        if result == case["expected"]:
            print(f"Test Case {idx + 1}: PASSED (Got expected '{result}')")
        else:
            print(f"Test Case {idx + 1}: FAILED. Expected '{case['expected']}', got '{result}'")
    except Exception as e:
        print(f"Test Case {idx + 1}: ERROR - {e}")
