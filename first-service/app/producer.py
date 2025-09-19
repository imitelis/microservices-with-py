# app/producer.py

from aiokafka import AIOKafkaProducer
from app.config import KAFKA_BOOTSTRAP_SERVERS

producer = None

async def start_producer():
    global producer
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()

async def stop_producer():
    await producer.stop()

async def send_message(topic: str, message: str):
    if producer is None:
        raise Exception("Producer not initialized")
    await producer.send_and_wait(topic, message.encode("utf-8"))
