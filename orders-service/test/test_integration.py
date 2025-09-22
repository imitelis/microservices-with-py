import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient, ASGITransport

# Patch *before* importing anything that uses KafkaOrderProducer
@pytest.fixture(scope="module")
def app_with_mocked_kafka():
    with patch("app.main.KafkaOrderProducer") as MockProducer:
        mock_instance = MockProducer.return_value
        mock_instance.start = AsyncMock()
        mock_instance.stop = AsyncMock()
        mock_instance.send_order = AsyncMock()

        from app.main import create_app  # ← imported *after* patch
        app = create_app()
        return app

@pytest.mark.asyncio
async def test_health_check(app_with_mocked_kafka):
    transport = ASGITransport(app=app_with_mocked_kafka)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/docs")
        assert response.status_code == 200

