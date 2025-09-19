# app/main.py

from fastapi import FastAPI
from app.producer import start_producer, stop_producer, send_message
from app.consumer import start_consumer_loop
from app.config import TOPIC_NAME

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await start_producer()
    start_consumer_loop()

@app.on_event("shutdown")
async def shutdown_event():
    await stop_producer()

@app.post("/publish")
async def publish_message(message: str):
    await send_message(TOPIC_NAME, message)
    return {"status": "message sent"}
