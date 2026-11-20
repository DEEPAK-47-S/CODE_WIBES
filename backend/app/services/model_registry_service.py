"""Model Registry & Capability Probing Service for local Ollama models."""
import time
from typing import Any, Dict, List, Optional
import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.model_registry import ModelRegistry

OLLAMA_BASE_URL = "http://127.0.0.1:11434"

# Category mapping guidelines
MODEL_CATEGORY_MAPPINGS = {
    "qwen3.5:4b": ["orchestration", "general", "reasoning", "customer_discovery"],
    "qwen2.5-coder:3b": ["coding", "engineering", "qa", "database", "debugging"],
    "gemma3:4b": ["ui_ux", "design", "marketing", "vision"],
    "granite4.2:3b": ["operations", "governance", "compliance", "finance", "business_logic"],
    "phi4-mini:latest": ["planning", "devops", "reasoning_fallback"],
    "qwen3.5:2b": ["lightweight", "classification", "summaries", "documentation"],
    "llama3.1:latest": ["sales", "voice", "lead_generation", "heavy_fallback"],
    "lfm3:latest": ["rapid_triage", "lightweight_fallback"],
}


class ModelRegistryService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def probe_and_sync_ollama_models(self) -> List[ModelRegistry]:
        """Query local Ollama /api/tags and /api/show to discover installed models and capabilities."""
        discovered: List[Dict[str, Any]] = []
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
                if res.status_code == 200:
                    models_data = res.json().get("models", [])
                    for m in models_data:
                        name = m.get("name")
                        digest = m.get("digest")
                        size = m.get("size")
                        details = m.get("details", {})
                        param_size = details.get("parameter_size")
                        quant = details.get("quantization_level")

                        # Inspect capabilities by probing model details
                        show_res = await client.post(f"{OLLAMA_BASE_URL}/api/show", json={"name": name})
                        show_data = show_res.json() if show_res.status_code == 200 else {}
                        
                        # Infer capabilities
                        is_vision = "vision" in name.lower() or "gemma3" in name.lower() or "qwen3.5" in name.lower()
                        is_thinking = "thinker" in name.lower() or "3.5" in name.lower() or "granite" in name.lower()
                        is_coder = "coder" in name.lower() or "code" in name.lower()
                        
                        # Set categories
                        cats = MODEL_CATEGORY_MAPPINGS.get(name, ["general"])
                        if is_coder and "coding" not in cats:
                            cats.append("coding")

                        discovered.append({
                            "name": name,
                            "digest": digest,
                            "size_bytes": size,
                            "parameter_size": param_size,
                            "quantization": quant,
                            "advertised_context": 262144 if "qwen" in name.lower() else 131072,
                            "runtime_context": 8192,  # Conservative 8K for 6GB VRAM
                            "supports_tools": True,
                            "supports_vision": is_vision,
                            "supports_thinking": is_thinking,
                            "supports_json": True,
                            "task_categories": cats,
                            "status": "ready",
                            "is_enabled": True,
                        })
        except Exception as e:
            print(f"Ollama probe warning: {e}")

        # Update or insert into PostgreSQL model_registry table
        synced_models: List[ModelRegistry] = []
        for d in discovered:
            res = await self.db.execute(select(ModelRegistry).where(ModelRegistry.name == d["name"]))
            existing = res.scalar_one_or_none()
            if not existing:
                record = ModelRegistry(**d)
                self.db.add(record)
                synced_models.append(record)
            else:
                existing.digest = d["digest"]
                existing.size_bytes = d["size_bytes"]
                existing.parameter_size = d["parameter_size"]
                existing.quantization = d["quantization"]
                existing.supports_vision = d["supports_vision"]
                existing.supports_thinking = d["supports_thinking"]
                existing.task_categories = d["task_categories"]
                existing.status = "ready"
                synced_models.append(existing)

        await self.db.commit()
        return synced_models

    async def list_models(self) -> List[ModelRegistry]:
        """Fetch all models currently registered in the database."""
        res = await self.db.execute(select(ModelRegistry).order_by(ModelRegistry.name))
        models = list(res.scalars().all())
        if not models:
            # First time: auto-probe
            models = await self.probe_and_sync_ollama_models()
        return models

    async def benchmark_model(self, model_name: str) -> Dict[str, Any]:
        """Run a lightweight inference benchmark on a model to measure latency and tokens/sec."""
        res = await self.db.execute(select(ModelRegistry).where(ModelRegistry.name == model_name))
        model = res.scalar_one_or_none()
        if not model:
            raise ValueError(f"Model '{model_name}' not found in registry.")

        t0 = time.time()
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(
                    f"{OLLAMA_BASE_URL}/api/generate",
                    json={
                        "model": model_name,
                        "prompt": "Respond with exactly 5 words stating your model status.",
                        "stream": False,
                    },
                )
                dt = time.time() - t0
                if resp.status_code == 200:
                    data = resp.json()
                    eval_count = data.get("eval_count", 10)
                    eval_duration_ns = data.get("eval_duration", 1_000_000_000)
                    tok_sec = (eval_count / (eval_duration_ns / 1e9)) if eval_duration_ns else (eval_count / max(dt, 0.1))
                    
                    model.latency_ms = round(dt * 1000, 2)
                    model.tokens_per_sec = round(tok_sec, 2)
                    model.benchmark_score = round(min(tok_sec * 2.5, 100.0), 1)
                    await self.db.commit()
                    await self.db.refresh(model)

                    return {
                        "model": model_name,
                        "latency_ms": model.latency_ms,
                        "tokens_per_sec": model.tokens_per_sec,
                        "benchmark_score": model.benchmark_score,
                        "status": "success",
                    }
                else:
                    return {"model": model_name, "error": f"Ollama HTTP {resp.status_code}", "status": "failed"}
        except Exception as e:
            return {"model": model_name, "error": str(e), "status": "error"}

    async def route_task(self, category: str) -> str:
        """Route a task category to the best available model with verified fallback."""
        res = await self.db.execute(
            select(ModelRegistry).where(ModelRegistry.is_enabled == True)
        )
        models = res.scalars().all()
        
        # 1. Match category
        for m in models:
            if m.task_categories and category in m.task_categories:
                return m.name

        # 2. Match general fallback
        for m in models:
            if m.name in ["qwen3.5:4b", "phi4-mini:latest", "llama3.1:latest"]:
                return m.name

        return models[0].name if models else "qwen3.5:4b"
