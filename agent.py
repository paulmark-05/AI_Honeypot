def agent_reply(history: list) -> str:
    """
    Naive human-like persona.
    Do NOT reveal detection.
    """
    last_message = history[-1]["text"].lower()

    if "upi" in last_message:
        return "Which UPI should I send to? It’s asking for confirmation."

    if "link" in last_message:
        return "The link isn’t opening properly. Can you resend?"

    if "account" in last_message:
        return "Why is my account being blocked suddenly?"

    return "I’m not sure I understand. Can you explain again?"
