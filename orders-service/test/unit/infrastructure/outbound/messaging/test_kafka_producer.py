import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from aiokafka.errors import KafkaConnectionError
import json
from src.domain.models.order import Order

@pytest.fixture
def kafka_producer():
    with patch('src.infrastructure.outbound.messaging.kafka_producer.AIOKafkaProducer') as MockProducer:
        mock_producer_instance = MagicMock()
        MockProducer.return_value = mock_producer_instance
        
        from src.infrastructure.outbound.messaging.kafka_producer import KafkaOrderProducer
        return KafkaOrderProducer()

@pytest.mark.asyncio
async def test_start_success(kafka_producer):
    with patch.object(kafka_producer, '_producer') as mock_producer:
        mock_producer.start = AsyncMock()
        
        await kafka_producer.start()
        
        mock_producer.start.assert_called_once()

@pytest.mark.asyncio
async def test_start_with_retries_success(kafka_producer):
    with patch.object(kafka_producer, '_producer') as mock_producer:
        # First two attempts fail, third succeeds
        mock_producer.start = AsyncMock(
            side_effect=[KafkaConnectionError("Failed"), KafkaConnectionError("Failed"), None]
        )
        
        with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            await kafka_producer.start(retries=3, delay=1)
        
        assert mock_producer.start.call_count == 3
        assert mock_sleep.call_count == 2

@pytest.mark.asyncio
async def test_start_max_retries_exceeded(kafka_producer):
    with patch.object(kafka_producer, '_producer') as mock_producer:
        mock_producer.start = AsyncMock(side_effect=KafkaConnectionError("Always fails"))
        
        with patch('asyncio.sleep', new_callable=AsyncMock):
            with pytest.raises(RuntimeError, match="Could not connect to Kafka after retries"):
                await kafka_producer.start(retries=2, delay=0.1)

@pytest.mark.asyncio
async def test_stop(kafka_producer):
    with patch.object(kafka_producer, '_producer') as mock_producer:
        mock_producer.stop = AsyncMock()
        
        await kafka_producer.stop()
        
        mock_producer.stop.assert_called_once()

@pytest.mark.asyncio
async def test_send_order_success(kafka_producer):
    order = Order(id=1, item="Test Item", quantity=2)
    expected_value = json.dumps(order.model_dump()).encode("utf-8")
    
    with patch.object(kafka_producer, '_producer') as mock_producer:
        mock_producer.send_and_wait = AsyncMock()
        
        await kafka_producer.send_order(order)
        
        mock_producer.send_and_wait.assert_called_once()
        # Check that the call was made with the expected topic and serialized order
        call_args = mock_producer.send_and_wait.call_args
        assert call_args[0][1] == expected_value  # Second argument should be the serialized order

@pytest.mark.asyncio
async def test_send_order_serialization(kafka_producer):
    order = Order(id=42, item="Laptop", quantity=1)
    
    with patch.object(kafka_producer, '_producer') as mock_producer:
        mock_producer.send_and_wait = AsyncMock()
        
        await kafka_producer.send_order(order)
        
        # Verify the serialized data
        call_args = mock_producer.send_and_wait.call_args
        serialized_data = call_args[0][1]
        deserialized = json.loads(serialized_data.decode("utf-8"))
        
        assert deserialized["id"] == 42
        assert deserialized["item"] == "Laptop"
        assert deserialized["quantity"] == 1