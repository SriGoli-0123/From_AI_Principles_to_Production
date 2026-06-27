# example1_eval_pass_k.py
import os
import re
import json
from langchain_openai import ChatOpenAI

# 1. Define the test cases: Prompt -> Programmatic Ground Truth checker
dataset = [
    {"query": "Calculate 15 * 6", "expected": 90},
    {"query": "Subtract 40 from 100", "expected": 60},
    {"query": "Divide 81 by 9", "expected": 9}
]

# Initialize model
if os.environ.get("OPENAI_API_KEY"):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    model_name = "gpt-4o-mini"
else:
    client_base_url = "http://localhost:11434/v1"
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
    llm = ChatOpenAI(
        base_url=client_base_url,
        api_key="ollama",
        model=model_name,
        temperature=0.7
    )

def run_agent_solver(query: str) -> str:
    response = llm.invoke(f"Solve this math problem. Output ONLY the numerical digits of the answer:\n{query}")
    return response.content.strip()

# 2. Evaluate Pass@k (where k=3 attempts)
k = 3
total_cases = len(dataset)
passed_cases = 0

print(f"Starting Pass@k Evaluation Run using model: {model_name}...")
for idx, case in enumerate(dataset):
    print(f"\nEvaluating Case {idx + 1}: '{case['query']}'")
    success = False
    
    # Try k independent times
    for attempt in range(1, k + 1):
        output_str = run_agent_solver(case["query"])
        # Extract digits using regex
        match = re.search(r"\d+", output_str)
        ans = int(match.group()) if match else None
        
        # Verify
        if ans == case["expected"]:
            print(f"  Attempt {attempt}: SUCCESS (Returned {ans})")
            success = True
            break
        else:
            print(f"  Attempt {attempt}: FAILED (Returned '{output_str}')")
            
    if success:
        passed_cases += 1

pass_rate = (passed_cases / total_cases) * 100
print(f"\n--- Evaluation Results ---")
print(f"Pass@{k} Success Rate: {pass_rate:.1f}% ({passed_cases}/{total_cases})")
