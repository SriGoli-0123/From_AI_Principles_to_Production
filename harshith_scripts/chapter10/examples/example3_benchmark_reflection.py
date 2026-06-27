# example3_benchmark_reflection.py
import os
import time
import json
from langchain_openai import ChatOpenAI

# Initialize model
if os.environ.get("OPENAI_API_KEY"):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
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
        temperature=0
    )

# Complex grammar constraint task
query = "Write a sentence describing the server status. The sentence must contain exactly seven words, and cannot use the word 'online'."

def run_single_pass() -> tuple[float, bool, str]:
    start_time = time.time()
    response = llm.invoke(query)
    elapsed = time.time() - start_time
    words = response.content.split()
    success = len(words) == 7 and "online" not in response.content.lower()
    return elapsed, success, response.content

def run_reflection_pass() -> tuple[float, bool, str]:
    start_time = time.time()
    draft = llm.invoke(query).content
    
    # Reflection step
    words = draft.split()
    success = len(words) == 7 and "online" not in draft.lower()
    
    if not success:
        # Critic instructions
        critique = f"Review your draft: '{draft}'. It has {len(words)} words instead of 7. Rewrite it."
        revised = llm.invoke(critique).content
        elapsed = time.time() - start_time
        words_rev = revised.split()
        final_success = len(words_rev) == 7 and "online" not in revised.lower()
        return elapsed, final_success, revised
    
    return time.time() - start_time, True, draft

print(f"Benchmarking Agent Performance using model: {model_name}...")
t_single, s_single, text_s = run_single_pass()
print(f"\n[Single Pass]: Success={s_single} | Time={t_single:.2f}s | Output: '{text_s}'")

t_ref, s_ref, text_r = run_reflection_pass()
print(f"[Reflection]:  Success={s_ref} | Time={t_ref:.2f}s | Output: '{text_r}'")
