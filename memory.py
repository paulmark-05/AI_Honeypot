sessions = {}

def get_session(session_id):
    if session_id not in sessions:
        sessions[session_id] = {
            "history": [],
            "turns": 0,
            "scamDetected": False,
            "intelligence": {
                "bankAccounts": [],
                "upiIds": [],
                "phishingLinks": [],
                "phoneNumbers": [],
                "suspiciousKeywords": []
            }
        }
    return sessions[session_id]
