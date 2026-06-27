# example2_model_optimizer.py
import os
import json
from langchain_openai import ChatOpenAI

# Mock accuracy database derived from Chapter 10 evaluations
model_evaluations = {
    "gpt-4o": {"accuracy": 0.98, "cost_per_1k": 0.005},
    "gpt-4o-mini": {"accuracy": 0.94, "cost_per_1k": 0.00015}
}

def invoke_optimized_model(prompt: str, target_accuracy: float = 0.90) -> str:
    selected_model = "gpt-4o"
    
    if model_evaluations["gpt-4o-mini"]["accuracy"] >= target_accuracy:
        selected_model = "gpt-4o-mini"
        
    print(f"\n[Optimizer]: Target Accuracy is {target_accuracy * 100}%")
    print(f"[Optimizer]: Selecting model '{selected_model}' based on cost evaluation metrics.")
    print(f"[Optimizer]: Cost difference: {model_evaluations['gpt-4o']['cost_per_1k'] / model_evaluations['gpt-4o-mini']['cost_per_1k']:.1f}x cheaper.")
    
    # Initialize and call selected model
    if os.environ.get("OPENAI_API_KEY"):
        llm = ChatOpenAI(model=selected_model, temperature=0)
        model_name = selected_model
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
        print(f"[Optimizer]: Local fallback model selected: '{model_name}'")
        
    response = llm.invoke(prompt)
    return response.content

# Test Optimizer with low accuracy tolerance
response = invoke_optimized_model("Explain database indexing in 1 sentence.", target_accuracy=0.90)
print(f"Response: {response}")
