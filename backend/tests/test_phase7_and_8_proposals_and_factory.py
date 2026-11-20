"""Unit and integration tests for Phase 7 (Requirement Discovery & Proposals) and Phase 8 (Website Factory)."""
import os
import uuid
import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.database.session import AsyncSessionLocal
from app.services.requirement_proposal_service import RequirementProposalService
from app.services.website_factory_service import WebsiteFactoryService


@pytest.mark.asyncio
async def test_brief_creation_and_proposal_approval_lock():
    """Verify that generating a proposal places it in awaiting_approval and requests Founder sign-off."""
    async with AsyncSessionLocal() as db:
        prop_service = RequirementProposalService(db)

        # 1. Capture Brief
        brief = await prop_service.create_requirement_brief(
            client_name="Coimbatore Textiles Ltd",
            business_goals="Build an export e-commerce portal with global currency support",
            required_pages=["Home", "Catalog", "Inquiry", "About", "Contact"],
            required_features=["Multi-Currency", "Product Filter", "WhatsApp Direct Quote"],
        )
        assert brief.id is not None
        assert brief.client_name == "Coimbatore Textiles Ltd"
        assert len(brief.required_pages) == 5

        # 2. Generate Proposal
        proposal = await prop_service.generate_proposal_draft(
            brief_id=brief.id,
            estimated_hours=60,
            rate_per_hour_inr=1500.0,
        )
        assert proposal.status == "awaiting_approval"
        assert proposal.total_cost_inr == 90000.0
        assert proposal.approval_request_id is not None
        assert len(proposal.milestones) == 4
        assert len(proposal.acceptance_criteria) == 4


@pytest.mark.asyncio
async def test_website_factory_isolated_workspace():
    """Verify that WebsiteFactoryService creates isolated client workspaces with real build files."""
    async with AsyncSessionLocal() as db:
        factory = WebsiteFactoryService(db)
        project_id = uuid.uuid4()
        
        result = await factory.create_isolated_project_workspace(
            project_id=project_id,
            project_name="Kovai Logistics Portal",
            tech_stack="React + FastAPI + PostgreSQL",
        )
        assert result["status"] == "workspace_ready"
        workspace_path = result["workspace_path"]
        assert os.path.exists(workspace_path)
        assert os.path.exists(os.path.join(workspace_path, "manifest.json"))
        assert os.path.exists(os.path.join(workspace_path, "public", "index.html"))


@pytest.mark.asyncio
async def test_proposals_and_factory_api_endpoints():
    """Verify REST endpoints for briefs, proposal generation, and workspace creation."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. POST brief
        resp_brief = await client.post(
            "/api/v1/proposals/briefs",
            json={
                "client_name": "Salem Steel Forge",
                "business_goals": "B2B client inquiry and product specifications",
                "required_pages": ["Home", "Products", "Contact"],
                "required_features": ["Catalog PDF Download", "Inquiry Form"],
            },
        )
        assert resp_brief.status_code == 200
        brief_id = resp_brief.json()["brief_id"]

        # 2. POST generate proposal
        resp_prop = await client.post(
            "/api/v1/proposals/generate",
            json={"brief_id": brief_id, "estimated_hours": 30, "rate_per_hour_inr": 1000.0},
        )
        assert resp_prop.status_code == 200
        assert resp_prop.json()["status"] == "awaiting_founder_approval"
        assert resp_prop.json()["total_cost_inr"] == 30000.0

        # 3. POST create workspace
        proj_id = str(uuid.uuid4())
        resp_ws = await client.post(
            "/api/v1/proposals/workspaces/create",
            json={"project_id": proj_id, "project_name": "Salem Steel Workspace"},
        )
        assert resp_ws.status_code == 200
        assert resp_ws.json()["status"] == "workspace_ready"
