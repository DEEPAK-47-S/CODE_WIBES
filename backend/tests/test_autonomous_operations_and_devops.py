"""Tests for Autonomous Operations Scheduler, DevOps Bundle, Customer Reviews, and Inbound Voice."""
import uuid
import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.database.session import AsyncSessionLocal
from app.models.invoice import Invoice
from app.models.project import Project
from app.services.devops_service import DevOpsService
from app.services.billing_contract_service import BillingContractService


@pytest.mark.asyncio
async def test_devops_bundle_generation():
    """Verify Atlas (D06 DevOps Lead) produces production Docker, Nginx, and GitHub Actions CI/CD."""
    async with AsyncSessionLocal() as db:
        devops = DevOpsService(db)
        proj_id = uuid.uuid4()
        res = await devops.generate_production_devops_bundle(
            project_id=proj_id,
            project_name="Erode Textiles Portal",
            domain="textiles.codewibes.com",
        )

        assert res["status"] == "devops_bundle_generated"
        assert "Dockerfile" in res["files_generated"]
        assert "docker/nginx.conf" in res["files_generated"]
        assert "docker-compose.yml" in res["files_generated"]
        assert ".github/workflows/deploy.yml" in res["files_generated"]


@pytest.mark.asyncio
async def test_autonomous_company_pulse():
    """Verify NEXUS COO autonomous heartbeat background pulse."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/api/v1/nexus/pulse")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "pulse_completed_successfully"
        assert "metrics" in data
        assert "pulse_timestamp" in data
        assert "NEXUS" in data["orchestrated_by"]


@pytest.mark.asyncio
async def test_customer_reviews_and_testimonials():
    """Verify authentic customer reviews with paid invoice provenance."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Create a paid invoice for verified client verification
        async with AsyncSessionLocal() as db:
            billing = BillingContractService(db)
            inv = await billing.create_invoice(
                client_name="Kovai Hydraulics Ltd",
                line_items=[{"description": "Production SCADA System", "amount": 90000.0}],
            )
            await billing.mark_invoice_paid(inv.id, "TEST-VERIFY-PAYMENT")
            inv_id = str(inv.id)

        # 1. Submit Review with paid invoice ID
        review_resp = await client.post(
            "/api/v1/reviews/submit",
            json={
                "client_name": "Kovai Hydraulics Ltd",
                "rating_stars": 5,
                "review_title": "Exceptional AI Engineering Speed",
                "review_text": "CODE WIBES delivered our production manufacturing portal with full Docker staging in 48 hours.",
                "invoice_id": inv_id,
                "allowed_for_marketing": True,
            },
        )
        assert review_resp.status_code == 200
        review_data = review_resp.json()
        assert review_data["status"] == "review_recorded"
        assert review_data["is_verified_client"] is True

        # 2. Query Verified Testimonials (Zero Fake Data)
        testim_resp = await client.get("/api/v1/reviews/verified-testimonials")
        assert testim_resp.status_code == 200
        testimonials = testim_resp.json()
        assert len(testimonials) >= 1
        assert any(t["client_name"] == "Kovai Hydraulics Ltd" for t in testimonials)
        assert testimonials[0]["provenance"] == "100% Verified Paid Counterparty"


@pytest.mark.asyncio
async def test_inbound_voice_twiml():
    """Verify inbound telephony XML endpoint returns TwiML with bilingual greeting."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/api/v1/voice/twiml-inbound")
        assert resp.status_code == 200
        assert "application/xml" in resp.headers["content-type"]
        assert "<Response>" in resp.text
        assert "CODE WIBES TECHNOLOGIES" in resp.text
        assert "வணக்கம்" in resp.text
