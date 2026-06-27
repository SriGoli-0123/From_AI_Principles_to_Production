# exercise1_3_retry_control_loop_solved.py
import time

def simulate_api_call(attempt):
    # Returns 429 (rate limit error) on attempts 1 and 2, and 200 (success) on attempt 3
    return 429 if attempt < 3 else 200

# ================= SOLUTION WORK =================
attempts = 0
max_attempts = 3
success = False

print("Starting retry control loop...")
while attempts < max_attempts:
    attempts += 1
    print(f"Calling API (Attempt {attempts}/{max_attempts})...")
    status = simulate_api_call(attempts)
    
    if status == 200:
        print("Success: API returned 200 Success. Task Complete!")
        success = True
        break
    elif status == 429:
        print("Transient error: 429 Rate Limit. Pausing for 1 second before retrying...")
        time.sleep(1)
    elif status == 404:
        raise RuntimeError("Fatal error: 404 Not Found. Halting immediately.")
    else:
        print(f"Unknown status: {status}. Halting.")
        break

if not success:
    print("Failure: Max attempts reached without success.")
# ================================================
