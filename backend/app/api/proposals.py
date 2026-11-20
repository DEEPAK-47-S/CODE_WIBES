"""API routes for Customer Briefs, Proposals, and Website Factory Workspaces."""
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.proposal import CustomerRequirementBrief, ProposalDraft
from app.services.requirement_proposal_service import RequirementProposalService
from app.services.website_factory_service import WebsiteFactoryService

router = APIRouter(prefix="/proposals", tags=["Proposals & Website Factory"])


class BriefCreateSchema(BaseModel):
    client_name: str
    business_goals: str
    required_pages: List[str]
    required_features: List[str]
    lead_id: Optional[uuid.UUID] = None
    target_audience: str = "B2B / Direct Consumers"
    tech_stack_preference: str = "React + FastAPI + PostgreSQL"
    target_timeline_weeks: int = 2


class GenerateProposalSchema(BaseModel):
    brief_id: uuid.UUID
    estimated_hours: int = 40
    rate_per_hour_inr: float = 1250.0


class CreateWorkspaceSchema(BaseModel):
    project_id: uuid.UUID
    project_name: str
    tech_stack: str = "React + FastAPI + PostgreSQL"


@router.post("/briefs")
async def create_requirement_brief(data: BriefCreateSchema, db: AsyncSession = Depends(get_db)):
    """Create a structured customer requirement brief."""
    service = RequirementProposalService(db)
    brief = await service.create_requirement_brief(
        client_name=data.client_name,
        business_goals=data.business_goals,
        required_pages=data.required_pages,
        required_features=data.required_features,
        lead_id=data.lead_id,
        target_audience=data.target_audience,
        tech_stack_preference=data.tech_stack_preference,
        target_timeline_weeks=data.target_timeline_weeks,
    )
    return {"status": "created", "brief_id": str(brief.id), "client_name": brief.client_name}


@router.get("/briefs")
async def list_requirement_briefs(db: AsyncSession = Depends(get_db)):
    """List all captured requirement briefs."""
    res = await db.execute(
        select(CustomerRequirementBrief).order_by(CustomerRequirementBrief.created_at.desc())
    )
    briefs = res.scalars().all()
    return [
        {
            "id": str(b.id),
            "client_name": b.client_name,
            "business_goals": b.business_goals,
            "pages": b.required_pages,
            "features": b.required_features,
            "tech_stack": b.tech_stack_preference,
            "timeline_weeks": b.target_timeline_weeks,
            "created_at": b.created_at.isoformat() if b.created_at else None,
        }
        for b in briefs
    ]


@router.post("/generate")
async def generate_proposal(data: GenerateProposalSchema, db: AsyncSession = Depends(get_db)):
    """Generate a formal proposal draft and submit to Founder Approval Inbox."""
    service = RequirementProposalService(db)
    try:
        proposal = await service.generate_proposal_draft(
            brief_id=data.brief_id,
            estimated_hours=data.estimated_hours,
            rate_per_hour_inr=data.rate_per_hour_inr,
        )
        return {
            "status": "awaiting_founder_approval",
            "proposal_id": str(proposal.id),
            "title": proposal.title,
            "total_cost_inr": proposal.total_cost_inr,
            "estimated_hours": proposal.estimated_hours,
            "approval_request_id": str(proposal.approval_request_id),
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("")
async def list_proposals(db: AsyncSession = Depends(get_db)):
    """List generated proposals and approval states."""
    res = await db.execute(select(ProposalDraft).order_by(ProposalDraft.created_at.desc()))
    proposals = res.scalars().all()
    return [
        {
            "id": str(p.id),
            "brief_id": str(p.brief_id),
            "title": p.title,
            "scope_summary": p.scope_summary,
            "milestones": p.milestones,
            "total_cost_inr": p.total_cost_inr,
            "status": p.status,
            "approval_request_id": str(p.approval_request_id) if p.approval_request_id else None,
            "created_at": p.created_at.isoformat() if p.created_at else None,
        }
        for p in proposals
    ]


@router.post("/workspaces/create")
async def create_isolated_workspace(data: CreateWorkspaceSchema, db: AsyncSession = Depends(get_db)):
    """Initialize an isolated project directory in execution/workspaces for client code generation."""
    factory = WebsiteFactoryService(db)
    result = await factory.create_isolated_project_workspace(
        project_id=data.project_id,
        project_name=data.project_name,
        tech_stack=data.tech_stack,
    )
    return result
