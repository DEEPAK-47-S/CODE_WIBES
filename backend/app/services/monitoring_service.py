"""System Monitoring & Observability Service."""
import time
import httpx
from typing import Any, Dict
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.audit_service import AuditService

OLLAMA_BASE_URL = "http://127.0.0.1:11434"


class MonitoringService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.audit = AuditService(db)

    async def get_system_health(self) -> Dict[str, Any]:
        """Perform comprehensive system diagnostics across DB, Ollama, and Governance."""
        # 1. Database Health & Latency
        t0 = time.time()
        try:
            res = await self.db.execute(text("SELECT 1"))
            db_ok = res.scalar() == 1
            db_latency_ms = round((time.time() - t0) * 1000, 2)
        except Exception as e:
            db_ok = False
            db_latency_ms = -1.0

        # 2. Ollama Health & Loaded Models
        ollama_ok = False
        loaded_models = []
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                res = await client.get(f"{OLLAMA_BASE_URL}/api/ps")
                if res.status_code == 200:
                    ollama_ok = True
                    loaded_models = [m.get("name") for m in res.json().get("models", [])]
        except Exception:
            ollama_ok = False

        # 3. Governance & Kill Switches
        settings = await self.audit.get_or_create_settings()

        return {
            "status": "healthy" if db_ok and ollama_ok else "degraded",
            "timestamp": time.time(),
            "database": {
                "connected": db_ok,
                "latency_ms": db_latency_ms,
                "engine": "PostgreSQL 19 AsyncPG",
            },
            "inference_engine": {
                "ollama_running": ollama_ok,
                "loaded_models": loaded_models,
                "max_concurrency_cap": settings.max_concurrent_models,
            },
            "governance_kill_switches": {
                "emergency_pause_active": settings.emergency_pause_all_agents,
                "external_actions_disabled": settings.disable_external_actions,
                "production_calling_locked": not settings.allow_production_calling,
            },
        }
