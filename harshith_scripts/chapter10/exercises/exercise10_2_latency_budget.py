# exercise10_2_latency_budget.py

class LatencyBudgetExceededError(Exception):
    pass

# TODO: Complete assert_latency_budget(durations, limit=5.0)
# - Compute average latency: sum(durations) / len(durations)
# - If average latency > limit, raise LatencyBudgetExceededError with details.
# - Otherwise, print a success message.
def assert_latency_budget(durations: list[float], limit: float = 5.0):
    pass
