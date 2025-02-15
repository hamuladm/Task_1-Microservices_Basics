from fastapi import FastAPI

app = FastAPI()

@app.get("/messages")
def get_handler():
    return "Not implemented yet"
