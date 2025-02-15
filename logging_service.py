from fastapi import FastAPI
from collections import defaultdict

app = FastAPI()
msg_map = defaultdict()


@app.post("/logging")
def post_handler(uuid: str, msg: str):
    msg_map[uuid] = msg


@app.get("/logging")
def get_handler():
    return f"{msg_map.values()}"
