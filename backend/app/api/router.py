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
from app.api.models_registry import router as models_router
from app.api.memory import router as memory_router
from app.api.approvals import router as approvals_router
from app.api.voice import router as voice_router
from app.api.proposals import router as proposals_router
from app.api.change_requests import router as change_requests_router
from app.api.nexus import router as nexus_router
from app.api.prospecting import router as prospecting_router
from app.api.billing import router as billing_router
from app.api.marketing import router as marketing_router
from app.api.website_factory import router as website_factory_router
from app.api.client_portal import router as client_portal_router
from app.api.reviews import router as reviews_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(departments_router)
api_v1_router.include_router(agents_router)
api_v1_router.include_router(projects_router)
api_v1_router.include_router(tasks_router)
api_v1_router.include_router(analytics_router)
api_v1_router.include_router(leads_router)
api_v1_router.include_router(owner_router)
api_v1_router.include_router(settings_router)
api_v1_router.include_router(models_router)
api_v1_router.include_router(memory_router)
api_v1_router.include_router(approvals_router)
api_v1_router.include_router(voice_router)
api_v1_router.include_router(proposals_router)
api_v1_router.include_router(change_requests_router)
api_v1_router.include_router(nexus_router)
api_v1_router.include_router(prospecting_router)
api_v1_router.include_router(billing_router)
api_v1_router.include_router(marketing_router)
api_v1_router.include_router(website_factory_router)
api_v1_router.include_router(client_portal_router)
api_v1_router.include_router(reviews_router)

