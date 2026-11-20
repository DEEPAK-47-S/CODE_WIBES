"""Unit and integration tests for Phase 1: Security, Audit, and Governance Foundation."""
import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.database.session import AsyncSessionLocal
from app.services.audit_service import AuditService
from app.models.company_setting import CompanySetting


@pytest.mark.asyncio
async def test_audit_service_hash_computation():
    """Test deterministic SHA-256 computation for audit logs."""
    data = {"project": "CODE WIBES", "priority": "high"}
    h1 = AuditService.compute_hash(data)
    h2 = AuditService.compute_hash(data)
    assert h1 == h2
    assert len(h1) == 64


@pytest.mark.asyncio
async def test_company_settings_initialization_and_safety_defaults():
    """Verify that company settings initialize with strict safety defaults."""
    async with AsyncSessionLocal() as db:
        service = AuditService(db)
        settings = await service.get_or_create_settings()
        assert settings is not None
        # Default safety: production calling must be disabled
        assert settings.allow_production_calling is False
        assert settings.max_concurrent_models >= 1


@pytest.mark.asyncio
async def test_policy_engine_kill_switches():
    """Test policy verification under normal, external-action, and emergency-pause conditions."""
    async with AsyncSessionLocal() as db:
        service = AuditService(db)
        settings = await service.get_or_create_settings()

        # 1. Normal task when not paused
        settings.emergency_pause_all_agents = False
        allowed, reason = await service.verify_execution_policy("agent_task")
        assert allowed is True
        assert reason == "PERMITTED"

        # 2. External action blocked when disable_external_actions is True
        settings.disable_external_actions = True
        allowed, reason = await service.verify_execution_policy("outbound_call")
        assert allowed is False
        assert "BLOCKED" in reason

        # 3. Emergency pause blocks all agent tasks
        settings.emergency_pause_all_agents = True
        allowed, reason = await service.verify_execution_policy("agent_task")
        assert allowed is False
        assert "Emergency Pause is active" in reason

        # Reset back to operational state
        settings.emergency_pause_all_agents = False
        await db.commit()


@pytest.mark.asyncio
async def test_settings_api_endpoints():
    """Test GET and POST settings endpoints via FastAPI test client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # GET /api/v1/settings
        resp = await client.get("/api/v1/settings")
        assert resp.status_code == 200
        data = resp.json()
        assert "emergency_pause_all_agents" in data
        assert "disable_external_actions" in data

        # POST /api/v1/settings/emergency-pause
        resp_pause = await client.post("/api/v1/settings/emergency-pause")
        assert resp_pause.status_code == 200
        assert resp_pause.json()["emergency_pause_all_agents"] is True

        # POST /api/v1/settings/resume
        resp_resume = await client.post("/api/v1/settings/resume")
        assert resp_resume.status_code == 200
        assert resp_resume.json()["emergency_pause_all_agents"] is False
