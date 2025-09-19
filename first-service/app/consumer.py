# app/consumer.py

import asyncio
from aiokafka import AIOKafkaConsumer
from app.config import KAFKA_BOOTSTRAP_SERVERS, TOPIC_NAME

async def consume():
    consumer = AIOKafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="fastapi-group"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print(f"Consumed message: {msg.value.decode('utf-8')}")
    finally:
        await consumer.stop()

# Background task for FastAPI
def start_consumer_loop():
    loop = asyncio.get_event_loop()
    loop.create_task(consume())
