# exercise4_2_summary_trigger.py

# TODO: Complete this summary logic.
# - If the length of raw_messages (excluding the system message) is greater than 6:
#   1. Slice the first 4 messages.
#   2. Pass them to generate_summary() to produce a condensed string.
#   3. Remove those 4 messages from raw_messages.
#   4. Reassemble messages list: [system] + [summary_message] + remaining_messages.
def manage_summary_trigger(messages: list, running_summary: str) -> tuple[list, str]:
    pass
