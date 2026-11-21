"""Tests for Enterprise Expansion: QA Security Scanner, Executive Morning Briefing, Client Portal, and Printable Docs."""
import uuid
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select

from app.main import app
from app.database.session import AsyncSessionLocal
from app.models.project import Project
from app.models.invoice import Invoice
from app.models.contract import Contract
from app.models.change_request import ChangeRequest
from app.models.approval import ApprovalRequest
from app.services.website_factory_service import WebsiteFactoryService
from app.services.quality_security_service import QualitySecurityService
from app.services.executive_briefing_service import ExecutiveBriefingService
from app.services.billing_contract_service import BillingContractService


@pytest.mark.asyncio
async def test_qa_and_security_audit_scanner():
    """Verify D04 QA and D10 CyberSecurity audit scanning, OWASP scoring, and report output."""
    async with AsyncSessionLocal() as db:
        # First generate a sample workspace
        factory = WebsiteFactoryService(db)
        proj_id = uuid.uuid4()
        await factory.create_isolated_project_workspace(
            project_id=proj_id,
            project_name="Vanguard Logistics",
            tech_stack="React + Tailwind + FastAPI",
            pages=["Home", "Tracking", "Contact"],
        )

        qa_service = QualitySecurityService(db)
        report = await qa_service.audit_project_workspace(proj_id)

        assert report["status"] in ("PASSED_STAGING_DEPLOYABLE", "PASSED_WITH_OBSERVATIONS")
        assert report["overall_score"] >= 80
        assert report["security_score"] >= 85
        assert report["owasp_top_10_compliant"] is True
        assert report["files_scanned_count"] >= 4
        assert "src/App.jsx" in report["files_scanned"]
        assert len(report["audited_by_departments"]) == 2


@pytest.mark.asyncio
async def test_executive_daily_briefing():
    """Verify NEXUS COO daily intelligence briefing compiles real-time KPIs and strategic priorities."""
    async with AsyncSessionLocal() as db:
        briefing_svc = ExecutiveBriefingService(db)
        briefing = await briefing_svc.generate_daily_briefing()

        assert "date" in briefing
        assert "CODE WIBES" in briefing["executive_summary"]
        assert "financials" in briefing
        assert "pipeline" in briefing
        assert "production" in briefing
        assert "governance" in briefing
        assert len(briefing["strategic_priorities"]) >= 3
        assert briefing["generated_by"]["agent"] == "Nexus"


@pytest.mark.asyncio
async def test_client_portal_endpoints():
    """Verify client portal data retrieval and change request submission."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Create a project in DB
        async with AsyncSessionLocal() as db:
            proj = Project(
                name="Tirupur Apparel Exports",
                description="B2B Fashion Garments ERP & Buyer Portal",
                status="in_progress",
            )
            db.add(proj)
            await db.commit()
            await db.refresh(proj)
            test_proj_id = proj.id

            # Add an invoice
            billing = BillingContractService(db)
            await billing.create_invoice(
                client_name="Tirupur Apparel Exports",
                project_id=test_proj_id,
                line_items=[{"description": "ERP Architecture", "amount": 75000.0}],
            )

        # 2. GET Client Portal Data
        resp = await client.get(f"/api/v1/client-portal/{test_proj_id}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["project"]["name"] == "Tirupur Apparel Exports"
        assert len(data["invoices"]) >= 1
        assert "qa_certification" in data

        # 3. POST Client Change Request
        cr_resp = await client.post(
            f"/api/v1/client-portal/{test_proj_id}/change-request",
            json={
                "title": "Add Multi-Currency Payment (USD / EUR)",
                "description": "International buyers require Stripe checkout in USD and EUR.",
                "priority": "high",
            },
        )
        assert cr_resp.status_code == 200
        cr_data = cr_resp.json()
        assert cr_data["status"] == "change_request_queued_for_founder_review"
        assert "approval_id" in cr_data

        # Check approval in DB
        async with AsyncSessionLocal() as db:
            app_uuid = uuid.UUID(cr_data["approval_id"])
            approval = (await db.execute(select(ApprovalRequest).where(ApprovalRequest.id == app_uuid))).scalar_one_or_none()
            assert approval is not None
            assert approval.action_type == "SCOPE_CHANGE_REQUEST"


@pytest.mark.asyncio
async def test_printable_invoice_and_contract_html():
    """Verify printable GST Tax Invoice and legal MSA contract HTML rendering."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        async with AsyncSessionLocal() as db:
            billing = BillingContractService(db)
            inv = await billing.create_invoice(
                client_name="Salem Steel Industries",
                line_items=[{"description": "Industrial IoT SCADA Dashboard", "amount": 80000.0}],
            )
            contract = await billing.create_service_contract(
                client_name="Salem Steel Industries",
                title="Industrial IoT Software Agreement",
                total_value_inr=94400.0,
            )
            inv_id = str(inv.id)
            contract_id = str(contract.id)

        # 1. Print Invoice HTML
        inv_resp = await client.get(f"/api/v1/billing/invoices/{inv_id}/print")
        assert inv_resp.status_code == 200
        assert "text/html" in inv_resp.headers["content-type"]
        assert "33AAACC1234F1Z5" in inv_resp.text  # GSTIN
        assert "Salem Steel Industries" in inv_resp.text
        assert "DEEPAKUMAR.S" in inv_resp.text

        # 2. Print Contract HTML
        contract_resp = await client.get(f"/api/v1/billing/contracts/{contract_id}/print")
        assert contract_resp.status_code == 200
        assert "text/html" in contract_resp.headers["content-type"]
        assert "MASTER SERVICE AGREEMENT" in contract_resp.text
        assert "Salem Steel Industries" in contract_resp.text
        assert "DEEPAKUMAR.S" in contract_resp.text
