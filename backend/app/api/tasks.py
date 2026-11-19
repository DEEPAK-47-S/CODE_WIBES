"""API v1 Task routes."""
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.schemas import TaskCreate, TaskRead
from app.services.company_service import CompanyService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=List[TaskRead])
async def list_tasks(
    project_id: Optional[uuid.UUID] = None,
    db: AsyncSession = Depends(get_db),
):
    """List all tasks, optionally filtered by project."""
    service = CompanyService(db)
    return await service.get_tasks(project_id=project_id)


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(data: TaskCreate, db: AsyncSession = Depends(get_db)):
    """Create a new task."""
    service = CompanyService(db)
    return await service.create_task(data)
