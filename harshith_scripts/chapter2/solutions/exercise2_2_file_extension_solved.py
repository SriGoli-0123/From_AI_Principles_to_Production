# exercise2_2_file_extension_solved.py
import os
from pydantic import BaseModel, Field, field_validator, ValidationError
from openai import OpenAI

class SaveReport(BaseModel):
    filename: str = Field(description="Name of the file, must end in .txt or .md")
    content: str = Field(description="Content to save inside the file")

    @field_validator('filename')
    def validate_filename(cls, value):
        if not (value.endswith('.txt') or value.endswith('.md')):
            raise ValueError("File extension must be strictly .txt or .md")
        return value

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

def run_test(prompt):
    print(f"\nPrompt: {prompt}")
    try:
        completion = client.beta.chat.completions.parse(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            response_format=SaveReport,
        )
        report = completion.choices[0].message.parse_error
        if report:
            print(f"[Monitor]: success=False | reason=Parse Failure: {report}")
            return
            
        parsed = completion.choices[0].message.parsed
        print(f"Extracted -> filename: {parsed.filename}")
        print(f"[Monitor]: success=True | details=Passed validation")
    except ValidationError as e:
        print(f"[Monitor]: success=False | reason=Schema Validation Failed: {e}")
    except Exception as e:
        print(f"[Monitor]: success=False | reason=API Error: {e}")

# Test Case 1: Valid extension (.txt)
run_test("Save 'System looks healthy' to status.txt")

# Test Case 2: Invalid extension (.exe)
run_test("Save 'malicious payload code' to payload.exe")
