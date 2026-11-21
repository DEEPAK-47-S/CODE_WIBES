"""Comprehensive automated tests for Autonomous Auto-Pilot and API Key Management:
1. Settings API Keys database persistence
2. WhatsApp Click-to-Chat & multi-channel proposition
3. Full 10-department autonomous client acquisition and delivery pipeline
"""
import uuid
import pytest
from sqlalchemy import select

from app.database.session import AsyncSessionLocal
from app.models.company_setting import CompanySetting
from app.models.lead import Lead
from app.models.approval import ApprovalRequest
from app.services.audit_service import AuditService
from app.services.communication_service import CommunicationService
from app.services.autopilot_service import AutopilotService


@pytest.mark.asyncio
async def test_settings_api_keys_persistence():
    """Verify that credentials entered in Frontend are saved and retrievable from PostgreSQL."""
    async with AsyncSessionLocal() as db:
        audit_svc = AuditService(db)
        settings = await audit_svc.get_or_create_settings()

        settings.google_maps_api_key = "AIzaSyTestGoogleMapsKey2026"
        settings.elevenlabs_api_key = "test_elevenlabs_secret_token"
        settings.whatsapp_api_token = "EAAQtestWhatsAppToken"
        settings.whatsapp_phone_number_id = "109876543210"
        settings.razorpay_key_id = "rzp_test_12345678"
        settings.razorpay_key_secret = "secret_rzp_token_xyz"
        await db.commit()

        # Re-fetch from DB
        res = await db.execute(select(CompanySetting))
        saved = res.scalar_one()
        assert saved.google_maps_api_key == "AIzaSyTestGoogleMapsKey2026"
        assert saved.elevenlabs_api_key == "test_elevenlabs_secret_token"
        assert saved.whatsapp_api_token == "EAAQtestWhatsAppToken"
        assert saved.razorpay_key_id == "rzp_test_12345678"


@pytest.mark.asyncio
async def test_communication_whatsapp_drafting():
    """Verify WhatsApp message composition and wa.me deep-link generation."""
    async with AsyncSessionLocal() as db:
        lead = Lead(
            company_name="Coimbatore Pumps & Motors",
            place_id=f"pl-wa-{uuid.uuid4().hex[:8]}",
            industry="Industrial Pumps",
            district="Coimbatore",
            phone="+91 94433 11223",
            website="coimbatorepumps.in",
            source="EXTERNAL_API",
            status="new",
        )
        db.add(lead)
        await db.commit()
        await db.refresh(lead)

        comm_svc = CommunicationService(db)
        wa_res = await comm_svc.draft_whatsapp_outreach(
            lead_id=lead.id,
            audit_score=68,
        )

        assert wa_res["status"] == "awaiting_founder_approval"
        assert "wa.me/919443311223" in wa_res["click_to_chat_url"]
        assert "CODE WIBES" in wa_res["message"]

        # Check DB Approval Request
        app_uuid = uuid.UUID(wa_res["approval_id"])
        approval = (await db.execute(select(ApprovalRequest).where(ApprovalRequest.id == app_uuid))).scalar_one()
        assert approval.action_type == "WHATSAPP_CLIENT_OUTREACH"
        assert approval.status == "pending"


@pytest.mark.asyncio
async def test_autopilot_full_company_pipeline():
    """Verify end-to-end execution of the 10-department autonomous pipeline."""
    async with AsyncSessionLocal() as db:
        autopilot = AutopilotService(db)
        result = await autopilot.run_full_company_pipeline(
            business_name="Kovai Precision Tools",
            website_url="kovaiprecision.in",
            phone="+91 98400 99887",
            location="Coimbatore, Tamil Nadu",
            category="Precision Tool Manufacturing",
        )

        assert result["status"] == "success"
        assert result["business_name"] == "Kovai Precision Tools"
        assert len(result["pipeline_log"]) >= 7
        assert "staging_preview_url" in result
        assert "http://127.0.0.1:8000/staging/" in result["staging_preview_url"]
        assert "invoice_number" in result
        assert result["total_inr"] > 0
        assert "contract_number" in result
        assert "wa.me" in result["whatsapp_click_to_chat"]
