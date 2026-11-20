"""API routes for Founder Approval Inbox and Decision Processing."""
import uuid
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.services.approval_service import ApprovalService

router = APIRouter(prefix="/approvals", tags=["Founder Approvals"])


class ApprovalCreateSchema(BaseModel):
    action_type: str
    title: str
    agent_id: Optional[uuid.UUID] = None
    task_id: Optional[uuid.UUID] = None
    description: Optional[str] = None
    preview_payload: Optional[Dict[str, Any]] = None
    risk_level: str = "HIGH"


class ApprovalDecisionSchema(BaseModel):
    approved: bool
    founder_feedback: Optional[str] = None


@router.get("/pending")
async def get_pending_approvals(db: AsyncSession = Depends(get_db)):
    """Fetch all pending approval requests in the Founder Inbox."""
    service = ApprovalService(db)
    items = await service.list_pending_requests()
    return [
        {
            "id": str(r.id),
            "task_id": str(r.task_id) if r.task_id else None,
            "agent_id": str(r.agent_id) if r.agent_id else None,
            "action_type": r.action_type,
            "title": r.title,
            "description": r.description,
            "preview_payload": r.preview_payload,
            "risk_level": r.risk_level,
            "status": r.status,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in items
    ]


@router.post("")
async def submit_approval_request(
    data: ApprovalCreateSchema, db: AsyncSession = Depends(get_db)
):
    """Submit a new action request to the Founder Approval queue."""
    service = ApprovalService(db)
    req = await service.create_request(
        action_type=data.action_type,
        title=data.title,
        agent_id=data.agent_id,
        task_id=data.task_id,
        description=data.description,
        preview_payload=data.preview_payload,
        risk_level=data.risk_level,
    )
    return {
        "status": "submitted",
        "request_id": str(req.id),
        "approval_status": req.status,
    }


@router.post("/{request_id}/decide")
async def decide_approval_request(
    request_id: uuid.UUID,
    data: ApprovalDecisionSchema,
    db: AsyncSession = Depends(get_db),
):
    """Approve or reject a pending request as the Founder."""
    service = ApprovalService(db)
    try:
        req = await service.decide_request(
            request_id=request_id,
            approved=data.approved,
            founder_feedback=data.founder_feedback,
        )
        return {
            "status": req.status,
            "request_id": str(req.id),
            "decided_at": req.decided_at.isoformat() if req.decided_at else None,
            "feedback": req.founder_feedback,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
