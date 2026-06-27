# prompt_test_runner.py
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# ================= STUDENT WORK =================
# TODO: Write instructions in the system prompt to force the LLM to output
# exactly 'PUBLIC' or 'PRIVATE' based on the user's input.
# No explanations, no greetings, no punctuation.
system_prompt = """
"""
# ================================================

test_cases = [
    {"input": "Put this on my public Twitter timeline", "expected": "PUBLIC"},
    {"input": "Whisper this quietly to Sarah's private inbox", "expected": "PRIVATE"}
]

for idx, case in enumerate(test_cases):
    response = client.chat.completions.create(
        model="llama3",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": case["input"]}
        ]
    )
    result = response.choices[0].message.content.strip().upper()
    if result == case["expected"]:
        print(f"Test Case {idx + 1}: PASSED")
    else:
        print(f"Test Case {idx + 1}: FAILED. Expected '{case['expected']}', got '{result}'")
