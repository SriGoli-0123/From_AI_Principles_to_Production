# exercise11_1_content_censor.py

# TODO: Complete censor_guardrail_node(state)
# - Read the final message content from state["messages"][-1].content.
# - If it contains the phrase "Project Orion", replace it with "[REDACTED]"
#   and set "security_violation" = True in state, then update the message history.
# - Otherwise, return {"security_violation": False}.
