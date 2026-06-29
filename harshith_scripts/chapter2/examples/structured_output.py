# structured_output.py
import os
from pydantic import BaseModel, Field
from openai import OpenAI

# 1. Define the schema using Pydantic
class CalculateSum(BaseModel):
    a: int = Field(description="First integer")
    b: int = Field(description="Second integer")

# 2. Connect to local Ollama (run 'ollama run llama3' first)
if os.environ.get("OPENAI_API_KEY"):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    model_name = "gpt-4o-mini"
else:
    client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    model_name = "llama3"
    # Fallback to any installed local model if llama3 isn't available
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

print(f"Invoking model '{model_name}' with structured output constraint...")
try:
    completion = client.beta.chat.completions.parse(
        model=model_name,
        messages=[
            {"role": "user", "content": "Please calculate the sum of 145 and 289."}
        ],
        response_format=CalculateSum,
    )
    result = completion.choices[0].message.parsed
    print(f"Parsed Pydantic Object: {result}")
    print(f"a: {result.a}, b: {result.b}")
except Exception as e:
    print(f"Error: {e}")
