"""API routes for Model Registry, dynamic capability discovery, and benchmarks."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.services.model_registry_service import ModelRegistryService

router = APIRouter(prefix="/models", tags=["Model Registry"])


class ModelResponseSchema(BaseModel):
    name: str
    parameter_size: Optional[str] = None
    quantization: Optional[str] = None
    advertised_context: int
    runtime_context: int
    supports_tools: bool
    supports_vision: bool
    supports_thinking: bool
    supports_json: bool
    task_categories: Optional[List[str]] = None
    latency_ms: Optional[float] = None
    tokens_per_sec: Optional[float] = None
    benchmark_score: Optional[float] = None
    status: str
    is_enabled: bool


@router.get("", response_model=List[ModelResponseSchema])
async def list_registered_models(db: AsyncSession = Depends(get_db)):
    """List all local Ollama models registered with verified capabilities and runtime contexts."""
    service = ModelRegistryService(db)
    models = await service.list_models()
    return [
        ModelResponseSchema(
            name=m.name,
            parameter_size=m.parameter_size,
            quantization=m.quantization,
            advertised_context=m.advertised_context,
            runtime_context=m.runtime_context,
            supports_tools=m.supports_tools,
            supports_vision=m.supports_vision,
            supports_thinking=m.supports_thinking,
            supports_json=m.supports_json,
            task_categories=m.task_categories or [],
            latency_ms=m.latency_ms,
            tokens_per_sec=m.tokens_per_sec,
            benchmark_score=m.benchmark_score,
            status=m.status,
            is_enabled=m.is_enabled,
        )
        for m in models
    ]


@router.post("/probe")
async def probe_ollama_models(db: AsyncSession = Depends(get_db)):
    """Trigger live probing of local Ollama /api/tags and /api/show to update capabilities."""
    service = ModelRegistryService(db)
    synced = await service.probe_and_sync_ollama_models()
    return {
        "status": "probed",
        "models_discovered": len(synced),
        "models": [m.name for m in synced],
    }


@router.post("/{model_name}/benchmark")
async def benchmark_single_model(model_name: str, db: AsyncSession = Depends(get_db)):
    """Run a real inference latency and throughput benchmark on a specific model."""
    service = ModelRegistryService(db)
    try:
        result = await service.benchmark_model(model_name)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
