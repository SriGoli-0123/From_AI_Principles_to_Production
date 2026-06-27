# exercise10_2_latency_budget_solved.py

class LatencyBudgetExceededError(Exception):
    pass

# ================= SOLUTION WORK =================
def assert_latency_budget(durations: list[float], limit: float = 5.0):
    if not durations:
        return
    avg_latency = sum(durations) / len(durations)
    print(f"[Audit]: Average latency = {avg_latency:.2f}s (Budget limit = {limit:.2f}s)")
    if avg_latency > limit:
        raise LatencyBudgetExceededError(
            f"LatencyBudgetExceededError: System latency average of {avg_latency:.2f}s "
            f"exceeded budget threshold limit of {limit:.2f}s!"
        )
    print("[Audit]: Latency verification PASSED.")
# ================================================

# Test Case 1: Within budget
print("--- Test Case 1 (Within Budget) ---")
assert_latency_budget([1.2, 2.5, 3.1, 0.9, 1.8], limit=5.0)

# Test Case 2: Budget exceeded
print("\n--- Test Case 2 (Budget Exceeded) ---")
try:
    assert_latency_budget([4.5, 6.2, 5.1, 7.8, 3.9], limit=5.0)
except LatencyBudgetExceededError as e:
    print(f"Successfully caught expected budget failure exception:\n{e}")
