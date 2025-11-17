# src/core/asyncapi_utils.py
import yaml

# src/core/asyncapi_utils.py
def generate_asyncapi_spec(topic: str, model: type, bootstrap_servers: str = "localhost:9092") -> dict:
    """Generate AsyncAPI spec dynamically from topic, Pydantic model, and bootstrap server info."""
    message_name = topic.replace(".", "_").title()

    payload_schema = {
        "type": "object",
        "properties": {},
        "required": []
    }

    for name, field in model.model_fields.items():  # <-- Pydantic v2
        # Determine type
        python_type = getattr(field.annotation, "__origin__", field.annotation)  # unwrap Optional/Annotated
        if python_type in [int]:
            json_type = "integer"
        elif python_type in [float]:
            json_type = "number"
        elif python_type in [bool]:
            json_type = "boolean"
        else:
            json_type = "string"

        payload_schema["properties"][name] = {"type": json_type}
        payload_schema["required"].append(name)

    spec = {
        "asyncapi": "3.0.0",
        "info": {
            "title": "Order Service Messaging",
            "version": "1.0.0",
            "description": f"Kafka topic {topic}"
        },
        "servers": {
            "kafka": {
                "host": bootstrap_servers,
                "protocol": "kafka",
                "description": "Kafka broker"
            }
        },
        "channels": {
            topic: {
                "address": topic,
                "description": f"Topic for {topic} events",
                "messages": {
                    "publish.message": {"$ref": f"#/components/messages/{message_name}"}
                }
            }
        },
        "operations": {
            f"{topic}.publish": {
                "action": "receive",
                "channel": {"$ref": f"#/channels/{topic}"},
                "messages": [{"$ref": f"#/channels/{topic}/messages/publish.message"}]
            }
        },
        "components": {
            "messages": {
                message_name: {
                    "name": message_name,
                    "title": message_name,
                    "summary": f"Message sent on {topic}",
                    "payload": payload_schema
                }
            }
        }
    }

    return spec

def asyncapi_yaml_from_spec(spec: dict) -> str:
    """Return YAML string from spec dictionary"""
    return yaml.safe_dump(spec, sort_keys=False)
