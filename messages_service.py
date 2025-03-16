from fastapi import FastAPI, status
import uvicorn

app = FastAPI()


@app.get("/messages", status_code=status.HTTP_200_OK)
def get_handler():
    return {"message": "Not implemented yet"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002)
