"""Comprehensive automated tests for CODE WIBES commercial powerhouse features:
1. Prospecting & Web Audits
2. Multi-File Website Factory & Live Staging
3. Voice Call Scope Extraction
4. Billing, Invoicing & Legal Contracts
5. Semantic Vector Memory
6. Marketing & Thought Leadership
"""
import uuid
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select

from app.main import app
from app.database.session import AsyncSessionLocal
from app.models.project import Project
from app.models.approval import ApprovalRequest
from app.models.invoice import Invoice
from app.models.contract import Contract
from app.models.marketing_post import MarketingPost
from app.models.voice_call import VoiceCallRecord
from app.services.lead_audit_service import LeadAuditService
from app.services.website_factory_service import WebsiteFactoryService
from app.services.voice_service import VoiceService
from app.services.billing_contract_service import BillingContractService
from app.services.semantic_memory_service import SemanticMemoryService
from app.services.marketing_service import MarketingService


@pytest.mark.asyncio
async def test_lead_audit_and_founder_approval_pitch():
    """Verify website auditing, scoring heuristics, and Founder Approval interception for outreach."""
    async with AsyncSessionLocal() as db:
        audit_service = LeadAuditService(db)
        audit = await audit_service.audit_website(
            target_url="example.com",
            business_name="Apex Logistics Ltd",
        )
        assert audit.id is not None
        assert audit.overall_score > 0
        assert len(audit.proposed_solutions) >= 2
        assert "Audit Report: Apex Logistics Ltd" in audit.audit_report_html

        # Generate outreach pitch
        pitch_res = await audit_service.generate_outreach_pitch(audit.id)
        assert pitch_res["status"] == "awaiting_founder_approval"
        assert "approval_id" in pitch_res

        # Check DB approval request
        app_id = uuid.UUID(pitch_res["approval_id"])
        approval = (await db.execute(select(ApprovalRequest).where(ApprovalRequest.id == app_id))).scalar_one_or_none()
        assert approval is not None
        assert approval.action_type == "OUTBOUND_CLIENT_PROPOSAL"
        assert approval.status == "pending"


@pytest.mark.asyncio
async def test_website_factory_multi_file_and_staging():
    """Verify Website Factory 2.0 multi-file component generation, index.html staging, and zip export."""
    async with AsyncSessionLocal() as db:
        factory = WebsiteFactoryService(db)
        test_proj_id = uuid.uuid4()
        res = await factory.create_isolated_project_workspace(
            project_id=test_proj_id,
            project_name="Zenith Health Clinic",
            tech_stack="React + Tailwind + FastAPI",
            pages=["Home", "Specialists", "Appointments", "Contact"],
            features=["Online Booking", "Doctor Profiles", "WhatsApp QuickChat"],
        )
        assert res["status"] in ("workspace_ready", "codebase_ready")
        assert "public/index.html" in res["files_generated"]
        assert "src/App.jsx" in res["files_generated"]

        # Verify staging HTML rendering
        staging_html = await factory.get_staging_html(test_proj_id)
        assert "Zenith Health Clinic" in staging_html
        assert "CODE WIBES Staging Preview" in staging_html

        # Verify zip export
        zip_path = await factory.export_project_zip(test_proj_id)
        assert zip_path.exists()
        assert zip_path.suffix == ".zip"


@pytest.mark.asyncio
async def test_billing_invoicing_and_contract_lifecycle():
    """Verify GST invoice calculation, payment settlement auto-onboarding, and legal MSA generation."""
    async with AsyncSessionLocal() as db:
        billing = BillingContractService(db)

        # 1. Create Project
        proj = Project(name="Custom CRM Portal", status="pending_payment", priority="high")
        db.add(proj)
        await db.commit()

        # 2. Generate Invoice: ₹50,000 subtotal + 18% GST = ₹59,000
        line_items = [
            {"description": "UI/UX Architecture & Design System", "amount": 20000.0},
            {"description": "FastAPI & React Engineering", "amount": 30000.0},
        ]
        invoice = await billing.create_invoice(
            client_name="Kovai Manufacturing Corp",
            line_items=line_items,
            project_id=proj.id,
            gst_rate_pct=18.0,
        )
        assert invoice.subtotal == 50000.0
        assert invoice.gst_amount == 9000.0
        assert invoice.total_amount == 59000.0
        assert invoice.status == "draft"
        assert "rzp.io" in invoice.payment_link

        # 3. Pay invoice and check auto-onboarding
        pay_res = await billing.mark_invoice_paid(invoice.id, "PAY-REF-TXN-8849")
        assert pay_res["status"] == "paid"
        assert pay_res["onboarding"] == "onboarding_initiated"

        # Verify project is now in_progress
        updated_proj = (await db.execute(select(Project).where(Project.id == proj.id))).scalar_one()
        assert updated_proj.status == "in_progress"

        # 4. Create Contract
        contract = await billing.create_service_contract(
            client_name="Kovai Manufacturing Corp",
            title="Master Service Agreement: CRM Portal",
            total_value_inr=59000.0,
            project_id=proj.id,
        )
        assert "CW-MSA-" in contract.contract_number
        assert "DEEPAKUMAR.S" in contract.terms_text

        # Sign contract
        sign_res = await billing.founder_sign_contract(contract.id)
        assert sign_res["status"] == "founder_approved"


@pytest.mark.asyncio
async def test_semantic_memory_vector_search():
    """Verify vector embedding generation and cosine similarity search over company memory."""
    from app.services.memory_service import MemoryService
    async with AsyncSessionLocal() as db:
        mem_service = MemoryService(db)
        semantic = SemanticMemoryService(db)

        # Index two distinct memories with real foreign keys
        mem1 = await mem_service.store_memory(
            tier="constitution",
            namespace="rules",
            key="rule-prov-test",
            content="Strict data provenance: Never display mock leads or simulated revenue in the CRM.",
        )
        mem2 = await mem_service.store_memory(
            tier="department",
            namespace="engineering",
            key="rule-ui-test",
            content="Frontend UI components must use Tailwind CSS and responsive flexbox layouts.",
        )

        await semantic.index_memory(
            memory_id=mem1.id,
            content=mem1.content,
            namespace="constitution",
        )
        await semantic.index_memory(
            memory_id=mem2.id,
            content=mem2.content,
            namespace="engineering",
        )

        # Search for governance
        results = await semantic.search("fake data and simulated lead policy", limit=2)
        assert len(results) > 0
        assert any("provenance" in r["content"].lower() for r in results)



@pytest.mark.asyncio
async def test_marketing_service_and_approval():
    """Verify social media thought leadership generation and Founder Approval gate."""
    async with AsyncSessionLocal() as db:
        marketing = MarketingService(db)
        post = await marketing.generate_thought_leadership_post(
            platform="linkedin",
            topic="Autonomous AI Software Development",
            key_insight="Strict human-in-the-loop governance guarantees production safety.",
        )
        assert post.id is not None
        assert post.status == "draft"
        assert len(post.hashtags) > 0
        assert "#CODEWIBES" in post.hashtags

        # Verify Approval Request was created
        apps = (await db.execute(
            select(ApprovalRequest).where(ApprovalRequest.action_type == "PUBLISH_MARKETING_POST")
        )).scalars().all()
        assert len(apps) > 0

        # Approve and publish
        pub_res = await marketing.approve_and_publish(post.id)
        assert pub_res["status"] == "published"


@pytest.mark.asyncio
async def test_voice_scope_extraction_from_call():
    """Verify analyzing voice call transcript extracts customer brief and proposal."""
    async with AsyncSessionLocal() as db:
        voice = VoiceService(db)
        # Create completed voice call record
        call = VoiceCallRecord(
            phone_number_masked="+91 98****1234",
            is_test_call=True,
            provider="ElevenLabs",
            conversation_id=f"conv-{uuid.uuid4().hex[:8]}",
            call_duration_seconds=50,
            status="completed",
            summary="Client requested a 4-page responsive corporate website.",
            transcript_redacted="Client: 'We need a modern corporate website with portfolio and contact form.'",
        )
        db.add(call)
        await db.commit()

        # Extract scope
        extracted = await voice.extract_requirements_from_call(call.id)
        assert extracted["status"] == "extracted"
        assert "brief_id" in extracted
        assert "proposal_id" in extracted
        assert extracted["total_inr"] > 0
