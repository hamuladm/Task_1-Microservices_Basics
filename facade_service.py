from fastapi import FastAPI
import uuid
import requests

app = FastAPI()


@app.post("/facade")
def post_handler(msg: str):
    id = uuid.uuid4()
    _ = requests.post(f"http://0.0.0.0:8081/logging?uuid={id}&msg={msg}")


@app.get("/facade")
def get_handler():
    log_res = requests.get("http://0.0.0.0:8081/logging")
    msg_res = requests.get("http://0.0.0.0:8082/messages")
    return f"{log_res.json()} : {msg_res.json()}"
