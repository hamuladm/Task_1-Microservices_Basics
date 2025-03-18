from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from utils import create_client
import uvicorn
import sys
import subprocess

app = FastAPI()
hz_port = sys.argv[1].split(":")[-1]
subprocess.Popen(
    ["hz", "start", "--port", f"{hz_port}"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)
client = create_client(sys.argv[1])
msg_map = client.get_map("msg_map")


class LogMessage(BaseModel):
    uuid: str
    msg: str


@app.post("/logging", status_code=status.HTTP_201_CREATED)
def post_handler(log_message: LogMessage):
    if msg_map.contains_key(log_message.uuid).result():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"UUID '{log_message.uuid}' already exists",
        )
    print(f"Received UUID: {log_message.uuid}, message: {log_message.msg}")
    msg_map.put(log_message.uuid, log_message.msg)
    return {"message": "Log created", "uuid": log_message.uuid}


@app.get("/logging", status_code=status.HTTP_200_OK)
def get_handler():
    keys = msg_map.key_set().result()
    if not keys:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No logs available"
        )

    logs = [msg_map.get(key).result() for key in keys]
    return {"logs": logs}


@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=int(sys.argv[2]))
