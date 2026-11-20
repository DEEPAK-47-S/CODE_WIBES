"""Unit and integration tests for Phase 9: Customer Review Portal & Change Management."""
import uuid
import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.database.session import AsyncSessionLocal
from app.models.project import Project
from app.models.change_request import ChangeRequest
from app.models.approval import ApprovalRequest
from sqlalchemy import select


@pytest.mark.asyncio
async def test_in_scope_and_out_of_scope_change_requests():
    """Verify in-scope revision vs out-of-scope change requests with automatic Founder approval gate."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Create a test project
        async with AsyncSessionLocal() as db:
            proj = Project(name="SaaS Portal V1", status="in_progress")
            db.add(proj)
            await db.commit()
            await db.refresh(proj)
            proj_id = str(proj.id)

        # 1. In-scope change request
        resp_in_scope = await client.post(
            "/api/v1/change-requests",
            json={
                "project_id": proj_id,
                "title": "Fix navbar alignment on mobile",
                "description": "The logo wraps awkwardly on iPhone 14 screen.",
                "is_in_scope": True,
                "estimated_hours": 2,
            },
        )
        assert resp_in_scope.status_code == 200
        assert resp_in_scope.json()["is_in_scope"] is True
        cr_id = resp_in_scope.json()["change_request_id"]

        # 2. Out-of-scope change request (Must create Founder approval request!)
        resp_out_of_scope = await client.post(
            "/api/v1/change-requests",
            json={
                "project_id": proj_id,
                "title": "Add Real-Time Multi-Language Chatbot",
                "description": "Customer requested full multilingual support which was not in initial brief.",
                "is_in_scope": False,
                "estimated_hours": 25,
            },
        )
        assert resp_out_of_scope.status_code == 200
        assert resp_out_of_scope.json()["is_in_scope"] is False

        # Verify an approval request was automatically registered in DB
        async with AsyncSessionLocal() as db:
            res_app = await db.execute(
                select(ApprovalRequest).where(
                    ApprovalRequest.action_type == "out_of_scope_change_order"
                )
            )
            app_reqs = res_app.scalars().all()
            assert len(app_reqs) >= 1
            assert "Add Real-Time Multi-Language Chatbot" in app_reqs[-1].title

        # 3. Update change request status
        resp_patch = await client.patch(
            f"/api/v1/change-requests/{cr_id}/status",
            json={"status": "verified_qa", "resolution_notes": "Navbar padding fixed by Forge and tested by Sentinel."},
        )
        assert resp_patch.status_code == 200
        assert resp_patch.json()["current_status"] == "verified_qa"
