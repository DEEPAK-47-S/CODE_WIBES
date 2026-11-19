"""API v1 Agent routes."""
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.schemas import AgentCreate, AgentRead
from app.services.company_service import CompanyService

router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("", response_model=List[AgentRead])
async def list_agents(db: AsyncSession = Depends(get_db)):
    """List all AI agents across the company."""
    service = CompanyService(db)
    return await service.get_agents()


@router.post("", response_model=AgentRead, status_code=status.HTTP_201_CREATED)
async def create_agent(data: AgentCreate, db: AsyncSession = Depends(get_db)):
    """Register a new AI agent."""
    service = CompanyService(db)
    return await service.create_agent(data)
