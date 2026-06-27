# example2_tool_verifier.py
import os
import json
from pydantic import BaseModel, Field, ValidationError
from openai import OpenAI

# Define a schema for writing a configuration file
class WriteConfigFile(BaseModel):
    filename: str = Field(description="Name of the file, must end in .json")
    config_data: dict = Field(description="Key-value pairs of configurations")

# A pure, deterministic Python execution layer
def execute_write_config(filename: str, config_data: dict) -> tuple[str, bool]:
    # Pure Function check: Ensure deterministic rules are enforced programmatically
    if not filename.endswith(".json"):
        return "Error: Filename must end with .json", False
    try:
        # Simulate writing file
        output_payload = json.dumps(config_data, indent=2)
        print(f"\n[System File System]: Writing to file '{filename}' with content:\n{output_payload}")
        return f"Successfully wrote config to {filename}", True
    except Exception as e:
        return f"Error: Failed to write config. Details: {str(e)}", False

# Connect to local Ollama (run 'ollama run llama3' first)
if os.environ.get("OPENAI_API_KEY"):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    model_name = "gpt-4o-mini"
else:
    client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    model_name = "llama3"
    try:
        import urllib.request
        import json as json_lib
        with urllib.request.urlopen("http://localhost:11434/api/tags") as response:
            data = json_lib.loads(response.read().decode())
            models = [m["name"] for m in data.get("models", [])]
            if models and model_name not in models:
                preferred = [m for m in models if "llama3" in m]
                model_name = preferred[0] if preferred else models[0]
    except Exception:
        pass

prompt = "Save the user preferences: theme is dark, volume is 80 to settings.json"

try:
    print(f"Prompt: {prompt}")
    # 1. Reason & Plan parameter selection via structured outputs
    completion = client.beta.chat.completions.parse(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        response_format=WriteConfigFile,
    )
    tool_call = completion.choices[0].message.parsed
    print(f"\nAgent decided tool call parameters: {tool_call}")
    
    # 2. Execute deterministic function
    message, success = execute_write_config(
        filename=tool_call.filename, 
        config_data=tool_call.config_data
    )
    
    # 3. Print Boolean execution confirmation (First thread of the reliability rope)
    print(f"\n[Tool Execution Monitor]: success={success} | details={message}")

except ValidationError as e:
    print(f"\n[Tool Execution Monitor]: success=False | reason=Schema Validation Failed: {e}")
except Exception as e:
    print(f"\n[Error]: {e}")
