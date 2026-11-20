"""Unit and integration tests for Phase 4: Durable Task Engine and Founder Approvals."""
import uuid
import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.database.session import AsyncSessionLocal
from app.services.approval_service import ApprovalService
from app.models.task import Task
from app.models.approval import TaskDependency


@pytest.mark.asyncio
async def test_approval_request_lifecycle_reject_flow():
    """Verify that an action request awaits approval and can be rejected by the Founder."""
    async with AsyncSessionLocal() as db:
        # Create a consequential task
        task = Task(title="Deploy to Live Production Server", status="running", priority="high")
        db.add(task)
        await db.commit()
        await db.refresh(task)

        service = ApprovalService(db)

        # 1. Agent submits approval request
        req = await service.create_request(
            action_type="production_deploy",
            title="Deploy release v1.0 to production",
            task_id=task.id,
            description="All tests passed; requesting production deployment approval.",
            preview_payload={"target_domain": "codewibes.com", "commit": "4a9c0b9"},
            risk_level="CRITICAL",
        )
        assert req.status == "pending"

        # Check task transitioned to awaiting_approval
        await db.refresh(task)
        assert task.status == "awaiting_approval"

        # 2. Founder rejects request
        decided = await service.decide_request(
            request_id=req.id,
            approved=False,
            founder_feedback="Need one more accessibility audit before production.",
        )
        assert decided.status == "rejected"
        assert decided.founder_feedback == "Need one more accessibility audit before production."

        # Check task transitioned to rejected
        await db.refresh(task)
        assert task.status == "rejected"


@pytest.mark.asyncio
async def test_approval_request_lifecycle_approve_flow():
    """Verify that a proposal draft can be approved by the Founder."""
    async with AsyncSessionLocal() as db:
        task = Task(title="Send Quotation to Enterprise Client", status="running", priority="medium")
        db.add(task)
        await db.commit()
        await db.refresh(task)

        service = ApprovalService(db)

        # 1. Agent requests approval
        req = await service.create_request(
            action_type="send_proposal",
            title="Send Quotation #1042 for ₹1,50,000",
            task_id=task.id,
            preview_payload={"client": "Apex Logistics", "total_inr": 150000},
            risk_level="HIGH",
        )
        assert req.status == "pending"

        # 2. Founder approves
        decided = await service.decide_request(
            request_id=req.id,
            approved=True,
            founder_feedback="Approved for client delivery.",
        )
        assert decided.status == "approved"
        await db.refresh(task)
        assert task.status == "approved"


@pytest.mark.asyncio
async def test_task_dependency_graph():
    """Verify task dependencies block execution until prerequisite tasks are completed."""
    async with AsyncSessionLocal() as db:
        parent_task = Task(title="Database Schema Migration", status="running", priority="high")
        child_task = Task(title="Backend API Route Implementation", status="created", priority="high")
        db.add_all([parent_task, child_task])
        await db.commit()
        await db.refresh(parent_task)
        await db.refresh(child_task)

        # Add dependency: child depends on parent
        dep = TaskDependency(task_id=child_task.id, depends_on_task_id=parent_task.id)
        db.add(dep)
        await db.commit()

        service = ApprovalService(db)

        # 1. Child task cannot run while parent is 'running'
        can_run, reason = await service.can_task_run(child_task.id)
        assert can_run is False
        assert "Blocked by dependency" in reason

        # 2. Complete parent task
        parent_task.status = "completed"
        await db.commit()

        # 3. Child task is now unblocked
        can_run, reason = await service.can_task_run(child_task.id)
        assert can_run is True
        assert "All dependencies completed" in reason


@pytest.mark.asyncio
async def test_approvals_api_endpoints():
    """Verify pending approvals query and decision processing via REST API."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Submit approval request via API
        resp_post = await client.post(
            "/api/v1/approvals",
            json={
                "action_type": "external_email",
                "title": "Send Cold Email to 5 Qualified Prospects",
                "description": "Reviewed copy for Coimbatore SME campaign.",
                "risk_level": "HIGH",
            },
        )
        assert resp_post.status_code == 200
        req_id = resp_post.json()["request_id"]

        # Fetch pending approvals
        resp_pending = await client.get("/api/v1/approvals/pending")
        assert resp_pending.status_code == 200
        pending_list = resp_pending.json()
        assert any(item["id"] == req_id for item in pending_list)

        # Founder decides request via API
        resp_decide = await client.post(
            f"/api/v1/approvals/{req_id}/decide",
            json={"approved": True, "founder_feedback": "Approved with max 5 emails."},
        )
        assert resp_decide.status_code == 200
        assert resp_decide.json()["status"] == "approved"
