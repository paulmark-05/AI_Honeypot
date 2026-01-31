import requests
from config import GUVI_CALLBACK_URL

def send_final_callback(session_id, session):
    payload = {
        "sessionId": session_id,
        "scamDetected": True,
        "totalMessagesExchanged": session["turns"],
        "extractedIntelligence": session["intelligence"],
        "agentNotes": "Used urgency and financial redirection tactics"
    }

    requests.post(GUVI_CALLBACK_URL, json=payload, timeout=5)
