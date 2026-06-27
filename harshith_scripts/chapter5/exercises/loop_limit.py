# exercise5_2_loop_limit.py
from typing import TypedDict, Annotated, Sequence
from operator import add
from langchain_core.messages import BaseMessage
from langgraph.graph import END

# TODO: Add a counter field to the AgentState TypedDict
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add]

# TODO: Update the router function so that it stops execution (returns END)
# if the counter state variable is greater than or equal to 3.
def router(state: AgentState) -> str:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "execute_tools"
    return END
