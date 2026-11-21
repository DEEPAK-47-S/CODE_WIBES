"""API v1 routes for Prospecting, Live Website Audits, and Outreach Pitches."""
import uuid
from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.services.lead_audit_service import LeadAuditService

router = APIRouter(prefix="/prospecting", tags=["prospecting"])


class AuditRequest(BaseModel):
    target_url: str
    business_name: str
    lead_id: Optional[str] = None


class OutreachDraftRequest(BaseModel):
    audit_id: str


@router.post("/audit")
async def audit_prospect_website(req: AuditRequest, db: AsyncSession = Depends(get_db)):
    """Runs deep technical audit on a prospect URL, returning score and HTML report."""
    service = LeadAuditService(db)
    lead_uuid = uuid.UUID(req.lead_id) if req.lead_id else None
    audit = await service.audit_website(
        target_url=req.target_url,
        business_name=req.business_name,
        lead_id=lead_uuid,
    )
    return {
        "id": str(audit.id),
        "target_url": audit.target_url,
        "business_name": audit.business_name,
        "overall_score": audit.overall_score,
        "performance_score": audit.performance_score,
        "seo_score": audit.seo_score,
        "mobile_friendly": audit.mobile_friendly,
        "ssl_active": audit.ssl_active,
        "issues_found": audit.issues_found,
        "proposed_solutions": audit.proposed_solutions,
        "report_html": audit.audit_report_html,
    }


@router.post("/outreach/draft")
async def draft_outreach_pitch(req: OutreachDraftRequest, db: AsyncSession = Depends(get_db)):
    """Drafts personalized outreach pitch and intercepts behind Founder Approval."""
    service = LeadAuditService(db)
    try:
        audit_uuid = uuid.UUID(req.audit_id)
        return await service.generate_outreach_pitch(audit_uuid)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
