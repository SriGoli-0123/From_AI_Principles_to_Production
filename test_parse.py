import os
from openai import OpenAI
from pydantic import BaseModel, Field

class CalculateSum(BaseModel):
    a: int = Field(description="First integer")
    b: int = Field(description="Second integer")

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

try:
    completion = client.beta.chat.completions.parse(
        model="llama3.1:latest",
        messages=[
            {"role": "user", "content": "Please calculate the sum of 145 and 289."}
        ],
        response_format=CalculateSum,
    )
    result = completion.choices[0].message.parsed
    print(f"Parsed directly: {result}")
    print(f"a: {result.a}, b: {result.b}")
except Exception as e:
    print(f"Error occurred: {e}")
