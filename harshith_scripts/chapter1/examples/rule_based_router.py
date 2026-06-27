# example1_rule_based_router.py

def share_status_api(button_pressed, current_time):
    # The developer had to hardcode every single condition manually
    if button_pressed == "night_mode":
        if current_time >= 20: # 8 PM
            action1 = "Dimming lights to 10%"
            action2 = "SMS Sent: 'Heading to bed.'"
            return [action1, action2]
        else:
            return "Too early for night mode."
    raise ValueError("Unknown command!")

# Test run with exact match
print("Testing with 'night_mode' at 9 PM (21):")
print(share_status_api("night_mode", 21))
# Output: ['Dimming lights to 10%', "SMS Sent: 'Heading to bed.'"]

try:
    print("\nTesting with messy voice command 'sleepy time':")
    print(share_status_api("sleepy time", 21))
except Exception as e:
    print(f"Error caught: {e}")
