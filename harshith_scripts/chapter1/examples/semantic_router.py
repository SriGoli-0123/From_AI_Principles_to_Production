# example2_semantic_router.py
import os
from openai import OpenAI

# Connect to local Ollama (run 'ollama run llama3' first)
# For OpenAI: swap base_url and use your OpenAI API key
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

def semantic_router(user_speech):
    system_prompt = (
        "You are a routing agent. Read the user's request and format it\n"
        "into a clean JSON response with two keys: 'destination' and 'clean_message'.\n"
        "Options for destination: 'Instagram', 'Discord', 'SMS'.\n"
        "You must output valid JSON."
    )
    
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_speech}
            ],
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content
    except Exception as e:
        print("\n[Error]: Could not connect to API or run model.")
        print(f"Make sure local Ollama is running and '{model_name}' is downloaded.")
        print("Run: ollama pull llama3")
        raise e

# Test run with messy human input
user_input = "Yo, beam this photo over to my Discord server and tell them check out this dog"
print(semantic_router(user_input))
