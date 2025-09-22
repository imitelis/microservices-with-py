# app/adapters/kafka_producer.py

import asyncio
from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaConnectionError
import json
from app.config import KAFKA_BOOTSTRAP_SERVERS, TOPIC_ORDERS
from app.domain.models import Order

class KafkaOrderProducer:
    def __init__(self):
        self._producer = AIOKafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS
        )

    async def start(self, retries=5, delay=3):
        for attempt in range(retries):
            try:
                await self._producer.start()
                print("success: Kafka producer connected.")
                return
            except KafkaConnectionError as e:
                print(f"warning: Kafka not ready (attempt {attempt + 1}/{retries}): {e}")
                await asyncio.sleep(delay)
        raise RuntimeError("error: Could not connect to Kafka after retries")

    async def stop(self):
        await self.producer.stop()

    async def send_order(self, order: Order):
        value = json.dumps(order.dict()).encode("utf-8")
        await self.producer.send_and_wait(TOPIC_ORDERS, value)
