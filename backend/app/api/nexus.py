"""API v1 NEXUS Central AI Manager routes for orchestrated company sprints."""
from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.services.nexus_manager import NexusManagerService

router = APIRouter(prefix="/nexus", tags=["nexus"])


class SprintRequest(BaseModel):
    """Founder directive to trigger a full company sprint."""
    objective: str
    max_retries: int = 2


class TaskExecuteRequest(BaseModel):
    """Execute a single task through NEXUS verification pipeline."""
    task_id: str
    max_retries: int = 2


@router.post("/sprint/plan")
async def plan_sprint(req: SprintRequest, db: AsyncSession = Depends(get_db)):
    """
    NEXUS decomposes a Founder objective into a Project with departmental tasks.
    Returns the strategic plan and task assignments without executing them.
    """
    nexus = NexusManagerService(db)
    try:
        return await nexus.plan_company_sprint(req.objective)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.post("/sprint/execute")
async def execute_sprint(req: SprintRequest, db: AsyncSession = Depends(get_db)):
    """
    Full end-to-end sprint: NEXUS plans, delegates, executes tasks sequentially,
    verifies each deliverable, and reports back to Founder.
    """
    nexus = NexusManagerService(db)
    try:
        return await nexus.run_end_to_end_sprint(req.objective)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.post("/task/execute")
async def execute_single_task(req: TaskExecuteRequest, db: AsyncSession = Depends(get_db)):
    """
    Execute a single task through the NEXUS verification pipeline:
    Agent inference → NEXUS quality check → optional retry → completion.
    """
    import uuid
    nexus = NexusManagerService(db)
    try:
        task_uuid = uuid.UUID(req.task_id)
        return await nexus.execute_task_with_verifier(task_uuid, max_retries=req.max_retries)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
