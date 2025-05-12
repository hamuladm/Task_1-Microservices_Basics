from fastapi import FastAPI, status
import threading
import hazelcast
import sys
import uvicorn

app = FastAPI()
messages = []
client = hazelcast.HazelcastClient(
    cluster_members=["127.0.0.1:5701", "127.0.0.1:5702", "127.0.0.1:5703"]
)
queue = client.get_queue("msg_queue")


def consume_messages():
    while True:
        msg = queue.take().result()
        messages.append(msg)


threading.Thread(target=consume_messages, daemon=True).start()


@app.get("/messages", status_code=status.HTTP_200_OK)
def get_handler():
    return {"logs": messages}


@app.get("/health", status_code=status.HTTP_200_OK)
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=int(sys.argv[1]))
