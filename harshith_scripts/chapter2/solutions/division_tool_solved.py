# division_tool_solved.py
import os
from pydantic import BaseModel, Field, ValidationError
from openai import OpenAI

class DivideNumbers(BaseModel):
    numerator: float = Field(description="The number to be divided")
    denominator: float = Field(description="The number to divide by, must not be zero")

def execute_division(numerator: float, denominator: float) -> tuple[float | None, bool]:
    if denominator == 0.0:
        return None, False
    return numerator / denominator, True

# Connect to local Ollama (run 'ollama run llama3' first)
if os.environ.get("OPENAI_API_KEY"):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    model_name = "gpt-4o-mini"
else:
    client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    model_name = "llama3"
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

prompt = "Divide 50 by 2"
print(f"Prompt: {prompt}")

try:
    completion = client.beta.chat.completions.parse(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        response_format=DivideNumbers,
    )
    args = completion.choices[0].message.parsed
    print(f"Extracted args -> numerator: {args.numerator}, denominator: {args.denominator}")
    
    result, success = execute_division(args.numerator, args.denominator)
    print(f"Result: {result} | Success: {success}")
    
    # Division by Zero test
    print("\nTesting division by zero: numerator=50, denominator=0...")
    result, success = execute_division(50, 0)
    print(f"Result: {result} | Success: {success}")
    
except ValidationError as e:
    print(f"Validation Error: {e}")
