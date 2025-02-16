from fastapi import FastAPI

app = FastAPI()
msg_map = {}


@app.post("/logging")
def post_handler(uuid: str, msg: str):
    msg_map[uuid] = msg


@app.get("/logging")
def get_handler():
    return f"{list(msg_map.values())}"
