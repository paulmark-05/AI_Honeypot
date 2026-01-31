import re

def extract_intelligence(text: str, store: dict):
    store["bankAccounts"] += re.findall(r"\b\d{9,18}\b", text)
    store["upiIds"] += re.findall(r"[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}", text)
    store["phishingLinks"] += re.findall(r"https?://\S+", text)
    store["phoneNumbers"] += re.findall(r"\+91\d{10}", text)

    keywords = ["urgent", "verify", "blocked", "suspended"]
    for k in keywords:
        if k in text.lower():
            store["suspiciousKeywords"].append(k)
