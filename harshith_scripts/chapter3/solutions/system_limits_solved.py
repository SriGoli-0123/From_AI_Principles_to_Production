# system_limits_solved.py

def mock_bad_tool() -> tuple[str, bool]:
    return "Error: Invalid argument value.", False

failed_attempts = 0

print("Starting Loop with safety validation counter...")
for step in range(5):
    print(f"\nLoop Step {step + 1}")
    
    # Execute tool
    message, success = mock_bad_tool()
    print(f"Tool status: success={success} | details={message}")
    
    # ================= SOLUTION WORK =================
    if not success:
        failed_attempts += 1
        print(f"Consecutive failures: {failed_attempts}/3")
        if failed_attempts >= 3:
            print("Hard stop: Too many consecutive tool failures. Exiting loop.")
            break
    else:
        failed_attempts = 0
    # ================================================
