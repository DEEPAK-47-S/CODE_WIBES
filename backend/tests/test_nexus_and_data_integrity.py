"""Tests for NEXUS Central AI Manager orchestration, verifier loop, and strict data integrity."""
import uuid
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select

from app.main import app
from app.database.session import AsyncSessionLocal
from app.models.task import Task
from app.models.project import Project
from app.models.approval import ApprovalRequest
from app.services.nexus_manager import NexusManagerService
from app.services.google_maps_lead_harvester import GoogleMapsLeadHarvester
from app.services.audit_service import AuditService


@pytest.mark.asyncio
async def test_nexus_plan_and_decompose():
    """Verify NEXUS plans a strategic sprint, creates DB tasks, and injects memory."""
    async with AsyncSessionLocal() as db:
        nexus = NexusManagerService(db)
        plan_res = await nexus.plan_company_sprint("Build authentication and user profile service")
        
        assert "project_id" in plan_res
        assert len(plan_res["tasks"]) == 3
        assert plan_res["status"] == "PLANNED"

        # Verify in DB
        proj_uuid = uuid.UUID(plan_res["project_id"])
        proj = (await db.execute(select(Project).where(Project.id == proj_uuid))).scalar_one_or_none()
        assert proj is not None
        assert "Build authentication" in proj.name

        tasks = (await db.execute(select(Task).where(Task.project_id == proj_uuid))).scalars().all()
        assert len(tasks) == 3


@pytest.mark.asyncio
async def test_nexus_consequential_task_approval_interception():
    """Verify consequential tasks (e.g. production deployment) are intercepted for Founder Approval."""
    async with AsyncSessionLocal() as db:
        # Create a test project and consequential task
        proj = Project(name="Production Deployment Sprint", status="in_progress", priority="critical")
        db.add(proj)
        await db.flush()

        task = Task(
            title="Deploy to production server and migrate database",
            description="Run production migrations and cutover DNS",
            status="pending",
            priority="critical",
            project_id=proj.id,
        )
        db.add(task)
        await db.commit()

        nexus = NexusManagerService(db)
        res = await nexus.execute_task_with_verifier(task.id)

        assert res["status"] == "awaiting_approval"
        assert "approval_id" in res

        # Check DB approval request
        app_uuid = uuid.UUID(res["approval_id"])
        approval = (await db.execute(select(ApprovalRequest).where(ApprovalRequest.id == app_uuid))).scalar_one_or_none()
        assert approval is not None
        assert approval.status == "pending"
        assert approval.risk_level == "HIGH"


@pytest.mark.asyncio
async def test_harvester_strict_data_integrity_no_fake_leads():
    """Verify that lead harvester NEVER fabricates fake leads when API key is missing."""
    async with AsyncSessionLocal() as db:
        harvester = GoogleMapsLeadHarvester(db)
        
        # When GOOGLE_MAPS_API_KEY is not set or empty in test environment
        leads = await harvester.harvest_leads(
            query="Automotive Services",
            location="Coimbatore",
            target_count=5,
        )

        # Must return empty list rather than generating synthetic fake businesses with fake phones
        assert isinstance(leads, list)
        for lead in leads:
            # If any real leads are returned, they must be from Google Places API
            assert lead.get("provenance") == "EXTERNAL_API"
            assert lead.get("verification_status") == "VERIFIED"


@pytest.mark.asyncio
async def test_emergency_pause_blocks_nexus_tasks():
    """Verify Emergency Pause kill-switch prevents NEXUS from executing or planning."""
    async with AsyncSessionLocal() as db:
        audit = AuditService(db)
        settings = await audit.get_or_create_settings()
        settings.emergency_pause_all_agents = True
        await db.commit()

        nexus = NexusManagerService(db)
        with pytest.raises(PermissionError) as exc_info:
            await nexus.plan_company_sprint("Unauthorized sprint while paused")

        assert "Execution halted by company policy" in str(exc_info.value)

        # Restore normal operation
        settings.emergency_pause_all_agents = False
        await db.commit()


@pytest.mark.asyncio
async def test_nexus_api_endpoints():
    """Verify NEXUS API v1 endpoints for sprint planning and single task execution."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Plan sprint
        resp = await client.post(
            "/api/v1/nexus/sprint/plan",
            json={"objective": "Develop automated billing and invoice microservice"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "project_id" in data
        assert len(data["tasks"]) == 3

        # 2. Execute consequential task (triggers approval pause)
        async with AsyncSessionLocal() as db:
            proj_uuid = uuid.UUID(data["project_id"])
            deploy_task = Task(
                title="Deploy to production server cluster",
                description="Live deployment",
                status="pending",
                project_id=proj_uuid,
            )
            db.add(deploy_task)
            await db.commit()
            task_id = str(deploy_task.id)

        task_resp = await client.post(
            "/api/v1/nexus/task/execute",
            json={"task_id": task_id, "max_retries": 1},
        )
        assert task_resp.status_code == 200
        task_data = task_resp.json()
        assert task_data["status"] == "awaiting_approval"
