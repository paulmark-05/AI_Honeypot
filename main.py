from fastapi import FastAPI, Header, HTTPException
from classifier import detect_scam
from agent import agent_reply
from extractor import extract_intelligence
from memory import get_session
from callback import send_final_callback
from config import API_KEY, MAX_AGENT_TURNS

app = FastAPI()


@app.post("/api/message")
def receive_message(payload: dict, x_api_key: str = Header(None)):
    # 1️⃣ API KEY CHECK
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # 2️⃣ SAFE PAYLOAD PARSING (VERY IMPORTANT FOR GUVI)
    session_id = payload.get("sessionId", "unknown-session")

    message_obj = payload.get("message", {})
    message_text = message_obj.get("text", "")

    sender = message_obj.get("sender", "scammer")
    timestamp = message_obj.get("timestamp", "")

    # 3️⃣ LOAD / CREATE SESSION
    session = get_session(session_id)

    # 4️⃣ APPEND MESSAGE SAFELY
    session["history"].append({
        "sender": sender,
        "text": message_text,
        "timestamp": timestamp
    })

    session["turns"] += 1

    # 5️⃣ EXTRACT INTELLIGENCE (SAFE EVEN IF TEXT IS EMPTY)
    extract_intelligence(message_text, session["intelligence"])

    # 6️⃣ SCAM DETECTION (ONLY ONCE)
    if not session["scamDetected"]:
        session["scamDetected"] = detect_scam(message_text)

    # 7️⃣ AGENT RESPONSE
    reply = "Okay."
    if session["scamDetected"]:
        reply = agent_reply(session["history"])

    # 8️⃣ FINAL CALLBACK (MANDATORY FOR GUVI)
    if session["turns"] >= MAX_AGENT_TURNS:
        send_final_callback(session_id, session)

    # 9️⃣ ALWAYS RETURN VALID JSON
    return {
        "status": "success",
        "scamDetected": session["scamDetected"],
        "reply": reply
    }
