"""Company settings & kill switches API router."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database.session import get_db
from app.services.audit_service import AuditService

router = APIRouter(prefix="/settings", tags=["Settings & Governance"])


class SettingsUpdateSchema(BaseModel):
    emergency_pause_all_agents: Optional[bool] = None
    disable_external_actions: Optional[bool] = None
    allow_calling_test_mode: Optional[bool] = None
    allow_production_calling: Optional[bool] = None
    founder_verified_phone: Optional[str] = None
    max_concurrent_models: Optional[int] = None
    daily_call_limit: Optional[int] = None
    monthly_budget_cap_usd: Optional[float] = None
    
    # Integration API Keys
    google_maps_api_key: Optional[str] = None
    elevenlabs_api_key: Optional[str] = None
    elevenlabs_voice_id: Optional[str] = None
    twilio_account_sid: Optional[str] = None
    twilio_auth_token: Optional[str] = None
    twilio_phone_number: Optional[str] = None
    whatsapp_api_token: Optional[str] = None
    whatsapp_phone_number_id: Optional[str] = None
    razorpay_key_id: Optional[str] = None
    razorpay_key_secret: Optional[str] = None
    stripe_api_key: Optional[str] = None
    cloud_llm_api_key: Optional[str] = None


@router.get("")
async def get_settings(db: AsyncSession = Depends(get_db)):
    """Fetch current global company operational settings, kill switch states, and API credentials."""
    service = AuditService(db)
    settings = await service.get_or_create_settings()
    return {
        "id": str(settings.id),
        "emergency_pause_all_agents": settings.emergency_pause_all_agents,
        "disable_external_actions": settings.disable_external_actions,
        "allow_calling_test_mode": settings.allow_calling_test_mode,
        "allow_production_calling": settings.allow_production_calling,
        "founder_verified_phone": settings.founder_verified_phone,
        "max_concurrent_models": settings.max_concurrent_models,
        "daily_call_limit": settings.daily_call_limit,
        "monthly_budget_cap_usd": settings.monthly_budget_cap_usd,
        "google_maps_api_key": settings.google_maps_api_key or "",
        "elevenlabs_api_key": settings.elevenlabs_api_key or "",
        "elevenlabs_voice_id": settings.elevenlabs_voice_id or "",
        "twilio_account_sid": settings.twilio_account_sid or "",
        "twilio_auth_token": settings.twilio_auth_token or "",
        "twilio_phone_number": settings.twilio_phone_number or "",
        "whatsapp_api_token": settings.whatsapp_api_token or "",
        "whatsapp_phone_number_id": settings.whatsapp_phone_number_id or "",
        "razorpay_key_id": settings.razorpay_key_id or "",
        "razorpay_key_secret": settings.razorpay_key_secret or "",
        "stripe_api_key": settings.stripe_api_key or "",
        "cloud_llm_api_key": settings.cloud_llm_api_key or "",
        "updated_at": settings.updated_at.isoformat() if settings.updated_at else None,
    }



@router.patch("")
async def update_settings(
    update_data: SettingsUpdateSchema,
    db: AsyncSession = Depends(get_db),
):
    """Update global company operational parameters and safety kill switches."""
    service = AuditService(db)
    settings = await service.get_or_create_settings()

    changes = {}
    for field, val in update_data.model_dump(exclude_unset=True).items():
        old_val = getattr(settings, field)
        if old_val != val:
            setattr(settings, field, val)
            changes[field] = {"from": old_val, "to": val}

    if changes:
        await db.commit()
        await db.refresh(settings)
        await service.log_event(
            actor_type="founder",
            action="update_company_settings",
            details={"changes": changes},
            risk_level="HIGH" if "emergency_pause_all_agents" in changes or "disable_external_actions" in changes else "MEDIUM",
        )

    return {
        "status": "updated",
        "applied_changes": changes,
        "settings": {
            "emergency_pause_all_agents": settings.emergency_pause_all_agents,
            "disable_external_actions": settings.disable_external_actions,
            "allow_calling_test_mode": settings.allow_calling_test_mode,
            "allow_production_calling": settings.allow_production_calling,
            "founder_verified_phone": settings.founder_verified_phone,
            "max_concurrent_models": settings.max_concurrent_models,
            "daily_call_limit": settings.daily_call_limit,
            "monthly_budget_cap_usd": settings.monthly_budget_cap_usd,
        },
    }


@router.post("/emergency-pause")
async def trigger_emergency_pause(db: AsyncSession = Depends(get_db)):
    """One-click emergency kill switch: immediately pause all company agents."""
    service = AuditService(db)
    settings = await service.get_or_create_settings()
    settings.emergency_pause_all_agents = True
    await db.commit()
    await service.log_event(
        actor_type="founder",
        action="emergency_pause_triggered",
        details={"reason": "Manual Founder Emergency Stop"},
        risk_level="CRITICAL",
    )
    return {"status": "paused", "emergency_pause_all_agents": True}


@router.post("/resume")
async def resume_operations(db: AsyncSession = Depends(get_db)):
    """Resume company agent operations after an emergency pause."""
    service = AuditService(db)
    settings = await service.get_or_create_settings()
    settings.emergency_pause_all_agents = False
    await db.commit()
    await service.log_event(
        actor_type="founder",
        action="operations_resumed",
        details={"reason": "Manual Founder Resume Action"},
        risk_level="HIGH",
    )
    return {"status": "resumed", "emergency_pause_all_agents": False}
