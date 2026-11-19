"""API v1 Department routes."""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.schemas import DepartmentRead
from app.services.company_service import CompanyService

router = APIRouter(prefix="/departments", tags=["departments"])


@router.get("", response_model=List[DepartmentRead])
async def list_departments(db: AsyncSession = Depends(get_db)):
    """List all company departments."""
    service = CompanyService(db)
    return await service.get_departments()
