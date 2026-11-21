"""API routes for Voice Calling, Opt-Out Enforcement, and Founder Alert Channel."""
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.voice_call import VoiceCallRecord
from app.services.voice_service import VoiceService

router = APIRouter(prefix="/voice", tags=["Voice & Telephony"])


class TestCallRequestSchema(BaseModel):
    phone_number: str
    lead_id: Optional[uuid.UUID] = None
    script_purpose: str = "Client qualification and web service discovery"


class FounderAlertSchema(BaseModel):
    alert_message: str


@router.get("/records")
async def list_voice_call_records(db: AsyncSession = Depends(get_db)):
    """List historical voice call records and compliance verification states."""
    res = await db.execute(
        select(VoiceCallRecord).order_by(VoiceCallRecord.created_at.desc()).limit(50)
    )
    records = res.scalars().all()
    return [
        {
            "id": str(r.id),
            "lead_id": str(r.lead_id) if r.lead_id else None,
            "phone_masked": r.phone_number_masked,
            "is_test_call": r.is_test_call,
            "duration": r.call_duration_seconds,
            "status": r.status,
            "summary": r.summary,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in records
    ]


@router.post("/test-call")
async def execute_test_voice_call(
    data: TestCallRequestSchema, db: AsyncSession = Depends(get_db)
):
    """Execute an ElevenLabs voice call under strict India telecom compliance test rules."""
    service = VoiceService(db)
    result = await service.initiate_voice_call(
        phone_number=data.phone_number,
        lead_id=data.lead_id,
        script_purpose=data.script_purpose,
        is_test_call=True,
    )
    return result


@router.post("/opt-out/{lead_id}")
async def enforce_lead_opt_out(
    lead_id: uuid.UUID,
    reason: str = "Customer requested opt-out",
    db: AsyncSession = Depends(get_db),
):
    """Add a lead to the permanent Do-Not-Contact suppression list."""
    service = VoiceService(db)
    try:
        return await service.record_opt_out(lead_id=lead_id, reason=reason)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/founder-alert")
async def dispatch_founder_alert(
    data: FounderAlertSchema, db: AsyncSession = Depends(get_db)
):
    """Trigger the Founder Voice Alert Channel for high-severity incidents."""
    service = VoiceService(db)
    result = await service.trigger_founder_emergency_alert_call(data.alert_message)
    return result


@router.post("/calls/{call_id}/extract-scope")
async def extract_scope_from_call(call_id: str, db: AsyncSession = Depends(get_db)):
    """Analyzes voice call transcript and extracts customer requirement brief and proposal draft."""
    service = VoiceService(db)
    try:
        c_uuid = uuid.UUID(call_id)
        return await service.extract_requirements_from_call(c_uuid)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/webhook")
async def handle_telephony_webhook(payload: dict, db: AsyncSession = Depends(get_db)):
    """Receives live call completion events from ElevenLabs or Twilio gateways."""
    service = VoiceService(db)
    return await service.ingest_telephony_webhook(payload)


@router.post("/twiml-inbound")
async def handle_inbound_voice_twiml():
    """Returns compliant TwiML for incoming telephone inquiries with AriaVoice introduction in Tamil & English."""
    twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say language="en-IN">Welcome to CODE WIBES TECHNOLOGIES. Connecting you with our AI Software Advisory team.</Say>
    <Pause length="1"/>
    <Say language="ta-IN">வணக்கம்! CODE WIBES TECHNOLOGIES நிறுவனத்திற்கு உங்களை வரவேற்கிறோம். எங்கள் மென்பொருள் திட்ட ஒருங்கிணைப்பாளர் உங்களுடன் இணைகிறார்.</Say>
    <Record maxLength="60" action="/api/v1/voice/webhook" playBeep="true"/>
</Response>"""
    return Response(content=twiml, media_type="application/xml")

