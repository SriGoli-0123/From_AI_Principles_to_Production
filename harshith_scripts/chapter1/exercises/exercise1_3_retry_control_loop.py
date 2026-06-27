# retry_control_loop.py
import time

def simulate_api_call(attempt):
    # Simulates returning 429 on the first two attempts, then succeeding on the third
    if attempt < 3:
        return 429
    return 200

attempts = 0
max_attempts = 3
# ================= STUDENT WORK =================
# TODO: Write a loop that invokes simulate_api_call() up to max_attempts times.
# - If the API returns a transient error code (429), pause for 1 second and retry.
# - If the API returns a fatal error code (like 404), raise a RuntimeError and halt immediately.
# - If the API returns 200 Success, break and print "Task Complete".
# ================================================
