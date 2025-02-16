uvicorn facade_service:app --host 0.0.0.0 --port 8080 --reload & 
uvicorn logging_service:app --host 0.0.0.0 --port 8081 --reload &
uvicorn messages_service:app --host 0.0.0.0 --port 8082 --reload &
