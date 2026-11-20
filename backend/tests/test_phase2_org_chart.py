"""Unit and integration tests for Phase 2: Org Chart and 100-Agent Profile Registry."""
import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.database.session import AsyncSessionLocal
from app.services.company_service import CompanyService
from app.agents.catalog import (
    DEPARTMENTS_CATALOG,
    build_full_agent_roster,
    DEPARTMENT_ROLES,
    NEXUS_PROFILE,
)


def test_catalog_structure_and_count():
    """Verify that catalog defines exactly 10 departments and 100 departmental profiles + NEXUS."""
    assert len(DEPARTMENTS_CATALOG) == 10
    assert len(DEPARTMENT_ROLES) == 10

    # Every department must have exactly 10 profiles (1 head + 9 specialists)
    for dept_code, roles in DEPARTMENT_ROLES.items():
        assert len(roles) == 10, f"Department {dept_code} must have 10 profiles"
        head_count = sum(1 for r in roles if r["is_head"])
        assert head_count == 1, f"Department {dept_code} must have exactly 1 Head"

    roster = build_full_agent_roster()
    # 1 NEXUS + 100 departmental profiles = 101 total
    assert len(roster) == 101


def test_required_profile_metadata():
    """Verify that every AI profile has complete non-negotiable metadata."""
    roster = build_full_agent_roster()
    for profile in roster:
        assert "code" in profile
        assert "name" in profile
        assert "role" in profile
        assert "system_instructions" in profile
        assert "model_preference" in profile
        assert "approval_mode" in profile
        assert len(profile["system_instructions"]) > 20


@pytest.mark.asyncio
async def test_sync_full_organization_in_database():
    """Verify that database seeding synchronizes all 10 departments and agents."""
    async with AsyncSessionLocal() as db:
        service = CompanyService(db)
        result = await service.sync_full_organization()
        assert result["status"] == "success"
        assert result["departments_count"] == 10
        assert result["agents_synced"] == 101

        # Check departments in DB
        depts = await service.get_departments()
        assert len(depts) >= 10

        # Check agents in DB
        agents = await service.get_agents()
        assert len(agents) >= 101


@pytest.mark.asyncio
async def test_org_chart_api_endpoint():
    """Verify that /api/v1/agents/org-chart returns the canonical company hierarchy."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/agents/org-chart")
        assert resp.status_code == 200
        data = resp.json()
        assert "founder" in data
        assert "central_manager" in data
        assert data["central_manager"]["name"] == "Nexus"
        assert "departments" in data
        assert len(data["departments"]) >= 10
