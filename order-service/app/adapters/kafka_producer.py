# app/adapters/kafka_producer.py

from aiokafka import AIOKafkaProducer
import json
from app.config import KAFKA_BOOTSTRAP_SERVERS, TOPIC_ORDERS
from app.domain.models import Order

class KafkaOrderProducer:
    def __init__(self):
        self.producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def send_order(self, order: Order):
        value = json.dumps(order.dict()).encode("utf-8")
        await self.producer.send_and_wait(TOPIC_ORDERS, value)
