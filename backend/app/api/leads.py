"""API v1 Lead / Client CRM routes with Google Maps Crawler & Exporter."""
from typing import List, Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, status, Response
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
    min_rating: float = 0.0
    only_missing_website: bool = False
    multi_queries: Optional[List[str]] = None


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
    Direct Hunter Agent to harvest targeted business leads from Google Maps.
    Supports single query or multi-search batch lists, rating filtering,
    and missing-website discovery for client prospecting.
    """
    harvester = GoogleMapsLeadHarvester(db)

    if req.multi_queries and len(req.multi_queries) > 0:
        harvested = await harvester.bulk_harvest_leads(
            queries=req.multi_queries,
            count_per_query=req.count,
            min_rating=req.min_rating,
            only_missing_website=req.only_missing_website,
        )
        return {
            "status": "SUCCESS",
            "message": f"Multi-search complete: Harvested {len(harvested)} leads across {len(req.multi_queries)} search terms",
            "query": f"Multi-search ({len(req.multi_queries)} terms)",
            "location": "Multiple",
            "leads_added": harvested,
        }

    harvested = await harvester.harvest_leads(
        query=req.query,
        location=req.location,
        target_count=req.count,
        min_rating=req.min_rating,
        only_missing_website=req.only_missing_website,
    )
    return {
        "status": "SUCCESS",
        "message": f"Successfully crawled {len(harvested)} leads from Google Maps for '{req.query}' in '{req.location}'",
        "query": req.query,
        "location": req.location,
        "leads_added": harvested,
    }


@router.get("/export/csv")
async def export_leads_csv(db: AsyncSession = Depends(get_db)):
    """
    Export all crawled Google Maps leads to Excel-ready CSV format
    with headers matching the Botsol schema specification.
    """
    harvester = GoogleMapsLeadHarvester(db)
    csv_content = await harvester.export_leads_csv()
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=code_wibes_google_maps_leads.csv"
        },
    )


@router.get("/export/json")
async def export_leads_json(db: AsyncSession = Depends(get_db)):
    """
    Export all crawled Google Maps leads as a structured JSON array
    matching the Botsol crawler schema.
    """
    harvester = GoogleMapsLeadHarvester(db)
    return await harvester.export_leads_json()

