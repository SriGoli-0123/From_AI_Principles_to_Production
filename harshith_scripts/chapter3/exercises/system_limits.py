# exercise3_1_system_limits.py

# A mock tool execution function that always fails validation
def mock_bad_tool() -> tuple[str, bool]:
    return "Error: Invalid argument value.", False

# TODO: Implement a ReAct loop wrapper that increments a failed_attempts counter
# whenever a tool call returns a validation failure (success=False).
# If the same tool fails 3 times in a row, break the loop immediately
# and print "Hard stop: Too many consecutive tool failures." to prevent wasting API tokens.

failed_attempts = 0

# Simulate a loop running 5 steps
for step in range(5):
    print(f"Loop Step {step + 1}")
    
    # Simulate intercepting a tool call and executing it
    message, success = mock_bad_tool()
    
    # ================= STUDENT WORK =================
    # Add your counter check here:
    # ================================================
