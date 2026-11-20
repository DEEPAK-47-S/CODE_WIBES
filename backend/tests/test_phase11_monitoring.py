"""Unit and integration tests for Phase 11: Production Monitoring & System Observability."""
import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.database.session import AsyncSessionLocal
from app.services.monitoring_service import MonitoringService


@pytest.mark.asyncio
async def test_monitoring_service_diagnostics():
    """Verify that MonitoringService checks DB connectivity, latency, and kill switches."""
    async with AsyncSessionLocal() as db:
        service = MonitoringService(db)
        health = await service.get_system_health()
        assert "status" in health
        assert "database" in health
        assert health["database"]["connected"] is True
        assert health["database"]["latency_ms"] >= 0
        assert "governance_kill_switches" in health


@pytest.mark.asyncio
async def test_system_health_api_endpoint():
    """Verify GET /health/system endpoint returns structured diagnostics."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/health/system")
        assert resp.status_code == 200
        data = resp.json()
        assert "database" in data
        assert "governance_kill_switches" in data
        assert data["database"]["connected"] is True
