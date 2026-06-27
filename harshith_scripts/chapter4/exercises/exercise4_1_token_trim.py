# exercise4_1_token_trim.py

# TODO: Complete this function.
# - It must calculate the character length of the system message (which cannot be deleted).
# - It must add non-system messages starting from the newest to oldest (from the right/end)
#   until adding another message would exceed the character limit (max_tokens * 4).
# - Reassemble and return system_messages + kept_non_system_messages (in their original order).
def trim_by_tokens(messages: list, max_tokens: int) -> list:
    char_limit = max_tokens * 4
    pass
