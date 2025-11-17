# src/core/asyncapi_spec.py
from pydantic import BaseModel

class OrderCreated(BaseModel):
    id: int
    product: str
    quantity: int

asyncapi_spec = {
    "asyncapi": "3.0.0",
    "info": {
        "title": "Order Service Messaging",
        "version": "1.0.0",
        "description": "Kafka topics for order events"
    },
    "servers": {
        "kafka": {
            "host": "localhost:9092",
            "protocol": "kafka",
            "description": "Development Kafka broker"
        }
    },
    "channels": {
        "orders.created": {
            "address": "orders.created",
            "messages": {
                "publish.message": {
                    "$ref": "#/components/messages/OrderCreated"
                }
            },
            "description": "Topic for newly created orders"
        }
    },
    "operations": {
        "orders.created.publish": {
            "action": "receive",
            "channel": {
                "$ref": "#/channels/orders.created"
            },
            "messages": [
                {"$ref": "#/channels/orders.created/messages/publish.message"}
            ]
        }
    },
    "components": {
        "messages": {
            "OrderCreated": {
                "name": "OrderCreated",
                "title": "Order Created",
                "summary": "Message sent when a new order is created",
                "payload": {
                    "type": "object",
                    "required": ["item", "quantity"],
                    "properties": {
                        "id": {"type": "integer", "description": "Order ID"},
                        "item": {"type": "string", "description": "Name of the item"},
                        "quantity": {"type": "integer", "description": "Quantity of the item"},
                    },
                },
            }
        }
    },
}
