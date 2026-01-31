from fastapi import FastAPI, Header, HTTPException, Request
from classifier import detect_scam
from agent import agent_reply
from extractor import extract_intelligence
from memory import get_session
from callback import send_final_callback
from config import API_KEY, MAX_AGENT_TURNS
import json

app = FastAPI()


@app.post("/api/message")
async def receive_message(
    request: Request,
    x_api_key: str = Header(None)
):
    # 1️⃣ API KEY CHECK
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # 2️⃣ READ RAW BODY (NO FASTAPI VALIDATION)
    try:
        body_bytes = await request.body()
        payload = json.loads(body_bytes) if body_bytes else {}
    except Exception:
        payload = {}

    # 3️⃣ SAFE EXTRACTION
    session_id = payload.get("sessionId", "unknown-session")

    message_obj = payload.get("message", {})
    if not isinstance(message_obj, dict):
        message_obj = {}

    message_text = message_obj.get("text", "")
    sender = message_obj.get("sender", "scammer")
    timestamp = message_obj.get("timestamp", "")

    # 4️⃣ SESSION
    session = get_session(session_id)

    session["history"].append({
        "sender": sender,
        "text": message_text,
        "timestamp": timestamp
    })
    session["turns"] += 1

    # 5️⃣ EXTRACTION (SAFE EVEN IF EMPTY)
    extract_intelligence(message_text, session["intelligence"])

    # 6️⃣ SCAM DETECTION
    if not session["scamDetected"]:
        session["scamDetected"] = detect_scam(message_text)

    # 7️⃣ AGENT RESPONSE
    reply = "Okay."
    if session["scamDetected"]:
        reply = agent_reply(session["history"])

    # 8️⃣ FINAL CALLBACK
    if session["turns"] >= MAX_AGENT_TURNS:
        send_final_callback(session_id, session)

    # 9️⃣ ALWAYS RETURN VALID JSON
    return {
        "status": "success",
        "scamDetected": session["scamDetected"],
        "reply": reply
    }
