"""API v1 routes for Website Factory 2.0 multi-file generation and staging previews."""
import uuid
from typing import List, Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.services.website_factory_service import WebsiteFactoryService
from app.services.quality_security_service import QualitySecurityService

router = APIRouter(prefix="/factory", tags=["factory"])


class CodebaseGenerateRequest(BaseModel):
    project_id: str
    project_name: str
    tech_stack: str = "React + Tailwind + FastAPI"
    pages: Optional[List[str]] = None
    features: Optional[List[str]] = None


@router.post("/generate")
async def generate_codebase(req: CodebaseGenerateRequest, db: AsyncSession = Depends(get_db)):
    """Generates complete multi-file React codebase and standalone staging preview."""
    service = WebsiteFactoryService(db)
    try:
        p_uuid = uuid.UUID(req.project_id)
        return await service.create_isolated_project_workspace(
            project_id=p_uuid,
            project_name=req.project_name,
            tech_stack=req.tech_stack,
            pages=req.pages,
            features=req.features,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/preview/{project_id}", response_class=HTMLResponse)
async def preview_staging_site(project_id: str, db: AsyncSession = Depends(get_db)):
    """Renders the generated staging website in HTML format for browser/iframe embedding."""
    service = WebsiteFactoryService(db)
    try:
        p_uuid = uuid.UUID(project_id)
        html_content = await service.get_staging_html(p_uuid)
        return HTMLResponse(content=html_content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/export/{project_id}")
async def export_workspace_zip(project_id: str, db: AsyncSession = Depends(get_db)):
    """Downloads packaged zip file of the generated project codebase."""
    service = WebsiteFactoryService(db)
    try:
        p_uuid = uuid.UUID(project_id)
        zip_path = await service.export_project_zip(p_uuid)
        return FileResponse(
            path=str(zip_path),
            filename=zip_path.name,
            media_type="application/zip",
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/audit/{project_id}")
async def get_project_qa_audit(project_id: str, db: AsyncSession = Depends(get_db)):
    """Retrieves or executes QA & Security certification audit (D04 QA & D10 CyberSecurity)."""
    service = QualitySecurityService(db)
    try:
        p_uuid = uuid.UUID(project_id)
        return await service.get_audit_report(p_uuid)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/audit/{project_id}")
async def run_project_qa_audit(project_id: str, db: AsyncSession = Depends(get_db)):
    """Forces a fresh QA & Security audit across all workspace files."""
    service = QualitySecurityService(db)
    try:
        p_uuid = uuid.UUID(project_id)
        return await service.audit_project_workspace(p_uuid)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
