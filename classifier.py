SCAM_KEYWORDS = [
    "account blocked", "verify immediately", "upi", "bank",
    "urgent", "otp", "suspended", "kyc", "click link"
]

def detect_scam(text: str) -> bool:
    text = text.lower()
    return any(keyword in text for keyword in SCAM_KEYWORDS)
