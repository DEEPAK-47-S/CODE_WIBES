"""Unit and integration tests for Phase 5 (Lead CRM & Places Policy) and Phase 6 (Voice Calling & TRAI Compliance)."""
import uuid
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.exc import IntegrityError

from app.main import app
from app.database.session import AsyncSessionLocal
from app.models.lead import Lead
from app.services.voice_service import VoiceService
from app.services.audit_service import AuditService


@pytest.mark.asyncio
async def test_lead_place_id_deduplication():
    """Verify that Google Places place_id enforces unique canonical lead records."""
    async with AsyncSessionLocal() as db:
        unique_pid = f"ChIJ_{uuid.uuid4().hex[:16]}"
        lead1 = Lead(
            company_name="Apex Coimbatore Tech",
            place_id=unique_pid,
            city="Coimbatore",
            district="Coimbatore",
            status="new",
        )
        db.add(lead1)
        await db.commit()

        # Attempt inserting duplicate place_id
        lead2 = Lead(
            company_name="Apex Coimbatore Duplicate",
            place_id=unique_pid,
            city="Coimbatore",
            district="Coimbatore",
            status="new",
        )
        db.add(lead2)
        with pytest.raises(IntegrityError):
            await db.commit()


@pytest.mark.asyncio
async def test_voice_calling_compliance_gates():
    """Verify that production calling is blocked without compliance verification, but test mode works."""
    async with AsyncSessionLocal() as db:
        audit_service = AuditService(db)
        settings = await audit_service.get_or_create_settings()
        
        # Ensure external actions enabled for test
        settings.disable_external_actions = False
        settings.allow_production_calling = False
        await db.commit()

        voice_service = VoiceService(db)

        # 1. Production call must be blocked
        res_prod = await voice_service.initiate_voice_call(
            phone_number="+919876543210",
            is_test_call=False,
        )
        assert res_prod["status"] == "blocked"
        assert "Production commercial calling is disabled" in res_prod["reason"]

        # 2. Test call succeeds
        res_test = await voice_service.initiate_voice_call(
            phone_number="+919876543210",
            is_test_call=True,
        )
        assert res_test["status"] == "completed"
        assert "call_id" in res_test
        assert res_test["duration"] > 0


@pytest.mark.asyncio
async def test_opt_out_suppression_enforcement():
    """Verify that opt-out suppression marks lead as do_not_contact and halts calls."""
    async with AsyncSessionLocal() as db:
        lead = Lead(
            company_name="Opt Out Test Enterprise",
            phone="+919999888877",
            status="new",
        )
        db.add(lead)
        await db.commit()
        await db.refresh(lead)

        voice_service = VoiceService(db)

        # Enforce opt-out
        res_opt = await voice_service.record_opt_out(lead_id=lead.id, reason="Requested via phone")
        assert res_opt["status"] == "suppressed"
        assert res_opt["lead_status"] == "do_not_contact"

        # Subsequent call attempt must be blocked
        res_call = await voice_service.initiate_voice_call(
            phone_number=lead.phone,
            lead_id=lead.id,
            is_test_call=True,
        )
        assert res_call["status"] == "blocked"
        assert "Do-Not-Contact" in res_call["reason"]


@pytest.mark.asyncio
async def test_voice_api_endpoints():
    """Verify test-call and opt-out endpoints via REST API."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Test call endpoint
        resp_call = await client.post(
            "/api/v1/voice/test-call",
            json={
                "phone_number": "+919444012345",
                "script_purpose": "Testing AI Voice Assistant",
            },
        )
        assert resp_call.status_code == 200
        assert "status" in resp_call.json()

        # 2. Call records endpoint
        resp_records = await client.get("/api/v1/voice/records")
        assert resp_records.status_code == 200
        assert isinstance(resp_records.json(), list)
