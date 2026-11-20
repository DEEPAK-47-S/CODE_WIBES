"""API v1 master router."""
from fastapi import APIRouter

from app.api.departments import router as departments_router
from app.api.agents import router as agents_router
from app.api.projects import router as projects_router
from app.api.tasks import router as tasks_router
from app.api.analytics import router as analytics_router
from app.api.leads import router as leads_router
from app.api.owner import router as owner_router
from app.api.settings import router as settings_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(departments_router)
api_v1_router.include_router(agents_router)
api_v1_router.include_router(projects_router)
api_v1_router.include_router(tasks_router)
api_v1_router.include_router(analytics_router)
api_v1_router.include_router(leads_router)
api_v1_router.include_router(owner_router)
api_v1_router.include_router(settings_router)
