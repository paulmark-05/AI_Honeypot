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
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    session_id = payload["sessionId"]
    message = payload["message"]["text"]

    session = get_session(session_id)
    session["history"].append(payload["message"])
    session["turns"] += 1

    extract_intelligence(message, session["intelligence"])

    if not session["scamDetected"]:
        session["scamDetected"] = detect_scam(message)

    reply = "Okay."
    if session["scamDetected"]:
        reply = agent_reply(session["history"])

    if session["turns"] >= MAX_AGENT_TURNS:
        send_final_callback(session_id, session)

    return {
        "status": "success",
        "scamDetected": session["scamDetected"],
        "reply": reply
    }
