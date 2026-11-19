"""API v1 Lead / Client CRM routes with Google Maps Harvester."""
from typing import List, Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.schemas import LeadCreate, LeadRead
from app.services.company_service import CompanyService
from app.services.google_maps_lead_harvester import GoogleMapsLeadHarvester

router = APIRouter(prefix="/leads", tags=["leads"])


class GoogleMapsHarvestRequest(BaseModel):
    query: str = "Software Companies"
    location: str = "Chennai"
    count: int = 5


@router.get("", response_model=List[LeadRead])
async def list_leads(db: AsyncSession = Depends(get_db)):
    """List all leads captured by Hunter Agent and Google Maps."""
    service = CompanyService(db)
    return await service.get_leads()


@router.post("", response_model=LeadRead, status_code=status.HTTP_201_CREATED)
async def create_lead(data: LeadCreate, db: AsyncSession = Depends(get_db)):
    """Add a new client lead to the CRM."""
    service = CompanyService(db)
    return await service.create_lead(data)


@router.post("/google-maps-harvest")
async def harvest_google_maps_leads(
    req: GoogleMapsHarvestRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Direct Hunter Agent to harvest targeted business leads from Google Maps
    by searching specific industry & location. All results are saved to PostgreSQL CRM.
    """
    harvester = GoogleMapsLeadHarvester(db)
    harvested = await harvester.harvest_leads(
        query=req.query,
        location=req.location,
        target_count=req.count,
    )
    return {
        "status": "SUCCESS",
        "message": f"Successfully harvested {len(harvested)} leads from Google Maps for '{req.query}' in '{req.location}'",
        "query": req.query,
        "location": req.location,
        "leads_added": harvested,
    }
