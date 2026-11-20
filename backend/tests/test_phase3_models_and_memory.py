"""Unit and integration tests for Phase 3: Model Registry and Persistent 7-Tier Memory."""
import uuid
import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.database.session import AsyncSessionLocal
from app.services.model_registry_service import ModelRegistryService
from app.services.memory_service import MemoryService
from app.models.project import Project
from app.models.task import Task


@pytest.mark.asyncio
async def test_model_registry_discovery_and_routing():
    """Verify that models are discovered, categorized, and routed appropriately."""
    async with AsyncSessionLocal() as db:
        service = ModelRegistryService(db)
        models = await service.probe_and_sync_ollama_models()
        assert len(models) > 0, "Should discover installed Ollama models"

        # Check task routing
        coding_model = await service.route_task("coding")
        assert "coder" in coding_model.lower() or "qwen" in coding_model.lower()

        orchestration_model = await service.route_task("orchestration")
        assert orchestration_model is not None


@pytest.mark.asyncio
async def test_persistent_memory_7_tiers():
    """Verify persistent memory storage and retrieval across the 7 canonical tiers."""
    async with AsyncSessionLocal() as db:
        mem_service = MemoryService(db)

        # 1. Constitution
        m1 = await mem_service.store_memory(
            tier="constitution",
            namespace="global",
            key="core_mission",
            content="Turning Ideas Into Digital Solutions through autonomous AI departments.",
        )
        assert m1.tier == "constitution"

        # 2. Founder Preference
        m2 = await mem_service.store_memory(
            tier="founder_preference",
            namespace="founder:deepak",
            key="approval_gate",
            content="Strict approval required before any external calling or live deployment.",
        )
        assert m2.tier == "founder_preference"

        # 3. Invalid tier should raise ValueError
        with pytest.raises(ValueError):
            await mem_service.store_memory(
                tier="invalid_tier",
                namespace="test",
                key="key",
                content="content",
            )

        # 4. Search memory
        found = await mem_service.search_memory(tier="constitution", search_query="Digital Solutions")
        assert len(found) >= 1
        assert "Turning Ideas Into Digital Solutions" in found[0].content


@pytest.mark.asyncio
async def test_task_checkpoint_and_resume():
    """Verify task checkpoint creation at threshold and checkpoint state recovery."""
    async with AsyncSessionLocal() as db:
        # Create a dummy task
        task = Task(
            title="Design SaaS Landing Page",
            status="running",
            priority="high",
        )
        db.add(task)
        await db.commit()
        await db.refresh(task)

        mem_service = MemoryService(db)

        # Check threshold evaluation
        should_checkpoint = mem_service.should_trigger_checkpoint(token_count=6000, context_budget=8192, threshold_pct=0.70)
        assert should_checkpoint is True

        # Create checkpoint
        chk = await mem_service.create_task_checkpoint(
            task_id=task.id,
            goal="Design complete responsive UI wireframes for SaaS client",
            completed_work="Completed sitemap and color system tokens",
            token_count_estimate=6100,
            key_decisions=["Use midnight navy theme", "Use 8px grid"],
            verified_facts=["Client requested 4 pages: Home, Pricing, About, Contact"],
            next_exact_actions=["Generate Pricing table React component"],
            trigger_reason="context_threshold_70%",
        )
        assert chk.run_number == 1
        assert chk.trigger_reason == "context_threshold_70%"

        # Retrieve checkpoint for clean context continuation
        latest = await mem_service.get_latest_checkpoint(task.id)
        assert latest is not None
        assert latest.goal == "Design complete responsive UI wireframes for SaaS client"
        assert len(latest.next_exact_actions) == 1
        assert latest.next_exact_actions[0] == "Generate Pricing table React component"


@pytest.mark.asyncio
async def test_models_and_memory_api_endpoints():
    """Verify REST endpoints for models and memory."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # GET /api/v1/models
        resp_models = await client.get("/api/v1/models")
        assert resp_models.status_code == 200
        models_data = resp_models.json()
        assert len(models_data) > 0

        # POST /api/v1/memory
        resp_mem = await client.post(
            "/api/v1/memory",
            json={
                "tier": "department",
                "namespace": "D06",
                "key": "coding_standard",
                "content": "All code must be modular, typed, and have passing unit tests.",
            },
        )
        assert resp_mem.status_code == 200
        assert resp_mem.json()["status"] == "stored"

        # GET /api/v1/memory?tier=department
        resp_get_mem = await client.get("/api/v1/memory?tier=department")
        assert resp_get_mem.status_code == 200
        assert len(resp_get_mem.json()) >= 1
