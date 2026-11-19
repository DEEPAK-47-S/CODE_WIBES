"""API v1 Analytics & Overview stats routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.schemas import OverviewStats
from app.services.company_service import CompanyService

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/overview", response_model=OverviewStats)
async def get_overview_stats(db: AsyncSession = Depends(get_db)):
    """Retrieve top-level company statistics for the executive dashboard."""
    service = CompanyService(db)
    return await service.get_overview_stats()
