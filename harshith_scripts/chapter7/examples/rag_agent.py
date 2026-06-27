# example2_rag_agent.py
import os
import json
from typing import TypedDict, Annotated, Sequence
from operator import add
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_core.embeddings import FakeEmbeddings

# 1. Build Vector Database
if os.environ.get("OPENAI_API_KEY"):
    from langchain_openai import OpenAIEmbeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    model_name = "gpt-4o-mini"
else:
    try:
        from langchain_community.embeddings import OllamaEmbeddings
        embeddings = OllamaEmbeddings(base_url="http://localhost:11434", model="nomic-embed-text")
        embeddings.embed_query("test") # Force validation query
    except Exception:
        embeddings = FakeEmbeddings(size=1536)
        
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

db = InMemoryVectorStore(embeddings)
db.add_documents([
    Document(page_content="System policy alpha: Passwords must be updated every 90 days."),
    Document(page_content="System policy beta: Multi-factor authentication is required for all admins."),
    Document(page_content="System policy gamma: API access is restricted to corporate IP addresses.")
])

# 2. Define the Retrieval Tool
@tool
def query_system_policies(search_query: str) -> str:
    """Searches the company systems policy handbook for relevant regulations."""
    # Deterministic layer check: pure Python search execution
    results = db.similarity_search(search_query, k=1)
    if not results:
        return "No relevant system policies found."
    return "\n".join([doc.page_content for doc in results])

tools = [query_system_policies]
tool_node = ToolNode(tools)

# 3. Define Graph State and Nodes
class RAGState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add]

if os.environ.get("OPENAI_API_KEY"):
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools(tools)
else:
    model = ChatOpenAI(
        base_url=client_base_url,
        api_key="ollama",
        model=model_name,
        temperature=0
    ).bind_tools(tools)

def call_agent(state: RAGState) -> dict:
    print("\n[Agent Node]: Analyzing query...")
    response = model.invoke(state["messages"])
    return {"messages": [response]}

def router(state: RAGState) -> str:
    last_msg = state["messages"][-1]
    if last_msg.tool_calls:
        return "run_tools"
    return END

# 4. Assemble Graph
workflow = StateGraph(RAGState)
workflow.add_node("agent", call_agent)
workflow.add_node("run_tools", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", router, {"run_tools": "run_tools", END: END})
workflow.add_edge("run_tools", "agent")

app = workflow.compile()

# Execute
user_query = [
    SystemMessage(content="You are a corporate compliance agent. Answer questions using the handbook search tool."),
    HumanMessage(content="How often do we need to reset passwords?")
]

print(f"Running RAG Agent using model: {model_name}...")
final_state = app.invoke({"messages": user_query})
print(f"\nFinal Response: {final_state['messages'][-1].content}")
