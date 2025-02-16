from fastapi import FastAPI
import uuid
import requests
import time

app = FastAPI()
MAX_TRIES = 10
DELAY = 2.


@app.post("/facade")
def post_handler(msg: str):
    id = uuid.uuid4()
    for _ in range(MAX_TRIES):
        try:
            _ = requests.post(f"http://0.0.0.0:8081/logging?uuid={id}&msg={msg}")
            return {"Sent": "OK"}
        except Exception:
            time.sleep(DELAY)
    return {"message": "Logging service unreachable"}


@app.get("/facade")
def get_handler():
    log_res = requests.get("http://0.0.0.0:8081/logging")
    msg_res = requests.get("http://0.0.0.0:8082/messages")
    return f"{log_res.json()} : {msg_res.json()}"
