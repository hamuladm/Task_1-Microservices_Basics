from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import uuid
import requests
import random
import time
import uvicorn

LOGGING_SERVICES = [
    "http://localhost:8001",
    "http://localhost:8002",
    "http://localhost:8003",
]
MAX_TRIES = 10
DELAY = 2.0

app = FastAPI()


class MessageInput(BaseModel):
    msg: str


def get_service_url():
    services = random.sample(LOGGING_SERVICES, len(LOGGING_SERVICES))
    for service in services:
        try:
            res = requests.get(f"{service}/health", timeout=2)
            if res.status_code == 200:
                return service
        except requests.RequestException:
            continue
    raise HTTPException(status_code=503, detail="No available logging-service")


@app.post("/facade", status_code=status.HTTP_201_CREATED)
def post_handler(msg: MessageInput):
    id = str(uuid.uuid4())
    for _ in range(MAX_TRIES):
        try:
            service_url = get_service_url()
            res = requests.post(
                f"{service_url}/logging", json={"uuid": id, "msg": msg.msg}, timeout=5
            )
            if res.status_code == 201:
                return {"message": "Message logged successfully", "uuid": id}
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            time.sleep(DELAY)
    raise HTTPException(status_code=503, detail="All logging-services are unreachable")


@app.get("/facade", status_code=status.HTTP_200_OK)
def get_handler():
    for _ in range(MAX_TRIES):
        try:
            service_url = get_service_url()
            res = requests.get(f"{service_url}/logging", timeout=5)
            if res.status_code == 200:
                return {"logs": res.json()}
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            time.sleep(DELAY)
    raise HTTPException(status_code=503, detail="Failed to retrieve logs")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
