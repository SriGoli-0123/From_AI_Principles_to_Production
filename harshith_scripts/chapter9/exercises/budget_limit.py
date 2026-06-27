# exercise9_2_budget_limit.py

class ReflectionBudgetExceededError(Exception):
    pass

# TODO: Complete this validation router logic.
# - If there is still an execution error (state["execution_error"]) and attempts >= 3:
#   Raise a ReflectionBudgetExceededError with a descriptive message.
# - If there is no error, return END.
# - Otherwise, return "coder" to retry.
