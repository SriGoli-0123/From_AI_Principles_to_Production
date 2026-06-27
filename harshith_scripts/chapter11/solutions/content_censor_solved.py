# exercise11_1_content_censor_solved.py
from typing import TypedDict, Annotated, Sequence
from operator import add
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END

class GuardrailState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add]
    security_violation: bool

def writer_node(state: GuardrailState) -> dict:
    print("[Writer Node]: Generating response...")
    # Simulate response containing codename Orion
    return {"messages": [AIMessage(content="Welcome to our new server, running Project Orion codes.")]}

# ================= SOLUTION WORK =================
def censor_guardrail_node(state: GuardrailState) -> dict:
    print("[Guardrail Node]: Inspecting output for sensitive keywords...")
    last_msg = state["messages"][-1]
    text = last_msg.content
    
    if "Project Orion" in text:
        print("[Guardrail]: Keyword violation detected! Redacting...")
        clean_text = text.replace("Project Orion", "[REDACTED]")
        # Replace the AIMessage in state updates
        return {
            "messages": [AIMessage(content=clean_text)],
            "security_violation": True
        }
        
    return {"security_violation": False}
# ================================================

# Assemble Graph
workflow = StateGraph(GuardrailState)
workflow.add_node("writer", writer_node)
workflow.add_node("guardrail", censor_guardrail_node)

workflow.add_edge(START, "writer")
workflow.add_edge("writer", "guardrail")
workflow.add_edge("guardrail", END)

app = workflow.compile()

print("Running censor guardrail test...")
res = app.invoke({"messages": [HumanMessage(content="Query status")], "security_violation": False})
print(f"\nFinal State Security Violation: {res.get('security_violation')}")
print(f"Final Message Content: '{res['messages'][-1].content}'")
