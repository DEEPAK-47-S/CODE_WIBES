"""API routes for customer review portal feedback and change request management."""
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.change_request import ChangeRequest
from app.services.approval_service import ApprovalService
from app.services.audit_service import AuditService

router = APIRouter(prefix="/change-requests", tags=["Customer Revisions & Change Requests"])


class ChangeRequestCreateSchema(BaseModel):
    project_id: uuid.UUID
    title: str
    description: str
    is_in_scope: bool = True
    estimated_hours: int = 4
    priority: str = "medium"


class ChangeRequestUpdateSchema(BaseModel):
    status: str
    resolution_notes: Optional[str] = None


@router.post("")
async def submit_change_request(data: ChangeRequestCreateSchema, db: AsyncSession = Depends(get_db)):
    """Submit a client change request from the review portal."""
    audit = AuditService(db)
    req = ChangeRequest(
        project_id=data.project_id,
        title=data.title,
        description=data.description,
        is_in_scope=data.is_in_scope,
        estimated_hours=data.estimated_hours,
        priority=data.priority,
        status="submitted",
    )
    db.add(req)
    await db.flush()

    # If out of scope, automatically submit approval request for Founder before charging client
    if not data.is_in_scope:
        approval = ApprovalService(db)
        await approval.create_request(
            action_type="out_of_scope_change_order",
            title=f"Out-of-Scope Change Request: {data.title}",
            description=f"Client submitted additional feature: {data.description} (Estimated {data.estimated_hours}h).",
            preview_payload={
                "change_request_id": str(req.id),
                "estimated_hours": data.estimated_hours,
                "project_id": str(data.project_id),
            },
            risk_level="MEDIUM",
        )

    await db.commit()
    await db.refresh(req)

    await audit.log_event(
        actor_type="customer",
        action="change_request_submitted",
        resource_type="change_request",
        resource_id=req.id,
        details={"title": data.title, "in_scope": data.is_in_scope},
        risk_level="LOW" if data.is_in_scope else "MEDIUM",
    )

    return {
        "status": "submitted",
        "change_request_id": str(req.id),
        "is_in_scope": req.is_in_scope,
    }


@router.get("/project/{project_id}")
async def list_project_change_requests(project_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """List all change requests submitted for a project."""
    res = await db.execute(
        select(ChangeRequest)
        .where(ChangeRequest.project_id == project_id)
        .order_by(ChangeRequest.created_at.desc())
    )
    items = res.scalars().all()
    return [
        {
            "id": str(r.id),
            "project_id": str(r.project_id),
            "title": r.title,
            "description": r.description,
            "is_in_scope": r.is_in_scope,
            "estimated_hours": r.estimated_hours,
            "priority": r.priority,
            "status": r.status,
            "resolution_notes": r.resolution_notes,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in items
    ]


@router.patch("/{request_id}/status")
async def update_change_request_status(
    request_id: uuid.UUID, data: ChangeRequestUpdateSchema, db: AsyncSession = Depends(get_db)
):
    """Update progress and resolution notes of a change request."""
    res = await db.execute(select(ChangeRequest).where(ChangeRequest.id == request_id))
    req = res.scalar_one_or_none()
    if not req:
        raise HTTPException(status_code=404, detail="Change request not found.")

    req.status = data.status
    if data.resolution_notes:
        req.resolution_notes = data.resolution_notes

    await db.commit()
    return {"status": "updated", "change_request_id": str(req.id), "current_status": req.status}
