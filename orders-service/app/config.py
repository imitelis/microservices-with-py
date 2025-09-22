# app/config.py
import os

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC_ORDERS = os.getenv("TOPIC_ORDERS", "orders.created")
SQLITE_DB_FILE = os.getenv("SQLITE_DB_FILE", "orders.db")
