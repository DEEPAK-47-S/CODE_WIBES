"""API v1 NEXUS Central AI Manager routes for orchestrated company sprints and autopilot."""
import uuid
from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.services.nexus_manager import NexusManagerService
from app.services.autopilot_service import AutopilotService
from app.services.executive_briefing_service import ExecutiveBriefingService
from app.services.autonomous_scheduler import AutonomousSchedulerService

router = APIRouter(prefix="/nexus", tags=["nexus"])


class SprintRequest(BaseModel):
    """Founder directive to trigger a full company sprint."""
    objective: str
    max_retries: int = 2


class TaskExecuteRequest(BaseModel):
    """Execute a single task through NEXUS verification pipeline."""
    task_id: str
    max_retries: int = 2


class AutopilotRequest(BaseModel):
    """Trigger full end-to-end 10-department autonomous client acquisition and delivery."""
    business_name: str
    website_url: str
    phone: Optional[str] = "+91 98400 12345"
    location: Optional[str] = "Coimbatore, Tamil Nadu"
    category: Optional[str] = "Enterprise Manufacturing & Retail"


@router.post("/sprint/plan")
async def plan_sprint(req: SprintRequest, db: AsyncSession = Depends(get_db)):
    """NEXUS decomposes a Founder objective into a Project with departmental tasks."""
    nexus = NexusManagerService(db)
    try:
        return await nexus.plan_company_sprint(req.objective)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.post("/sprint/execute")
async def execute_sprint(req: SprintRequest, db: AsyncSession = Depends(get_db)):
    """Full end-to-end sprint: NEXUS plans, delegates, executes tasks sequentially, and verifies deliverables."""
    nexus = NexusManagerService(db)
    try:
        return await nexus.run_end_to_end_sprint(req.objective)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.post("/task/execute")
async def execute_single_task(req: TaskExecuteRequest, db: AsyncSession = Depends(get_db)):
    """Execute a single task through the NEXUS verification pipeline."""
    nexus = NexusManagerService(db)
    try:
        task_uuid = uuid.UUID(req.task_id)
        return await nexus.execute_task_with_verifier(task_uuid, max_retries=req.max_retries)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.post("/autopilot/run")
async def run_full_company_autopilot(req: AutopilotRequest, db: AsyncSession = Depends(get_db)):
    """
    Executes the entire 10-department autonomous company pipeline:
    Lead Discovery -> Web Audit -> Multi-Channel Contact & WhatsApp -> Proposal -> Codebase Factory -> Invoicing -> MSA.
    """
    autopilot = AutopilotService(db)
    try:
        return await autopilot.run_full_company_pipeline(
            business_name=req.business_name,
            website_url=req.website_url,
            phone=req.phone or "+91 98400 12345",
            location=req.location or "Coimbatore, Tamil Nadu",
            category=req.category or "Enterprise Manufacturing & Retail",
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/briefing")
async def get_executive_daily_briefing(db: AsyncSession = Depends(get_db)):
    """NEXUS COO daily intelligence briefing: pipeline, revenue, tasks, and strategic priorities."""
    briefing_service = ExecutiveBriefingService(db)
    try:
        return await briefing_service.generate_daily_briefing()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pulse")
async def trigger_company_pulse(db: AsyncSession = Depends(get_db)):
    """Executes a proactive autonomous operations pulse across leads, receivables, and QA."""
    scheduler = AutonomousSchedulerService(db)
    try:
        return await scheduler.execute_company_pulse()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
