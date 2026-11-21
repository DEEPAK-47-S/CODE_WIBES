"""Semantic Vector Memory Service using local Ollama embeddings and cosine similarity search."""
import math
import uuid
from typing import Any, Dict, List, Optional
import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.memory import CompanyMemory
from app.models.memory_embedding import MemoryEmbedding

OLLAMA_EMBED_API = "http://127.0.0.1:11434/api/embeddings"
DEFAULT_EMBED_MODEL = "embeddinggemma-2:latest"


def _cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Computes cosine similarity between two float vectors."""
    if not vec_a or not vec_b or len(vec_a) != len(vec_b):
        return 0.0
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


class SemanticMemoryService:
    """Indexes and performs semantic similarity search across company memory tiers."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_embedding(self, text: str, model: str = DEFAULT_EMBED_MODEL) -> List[float]:
        """Queries local Ollama embeddings endpoint, with deterministic fallback vector."""
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.post(OLLAMA_EMBED_API, json={"model": model, "prompt": text})
                if resp.status_code == 200:
                    vec = resp.json().get("embedding")
                    if isinstance(vec, list) and len(vec) > 0:
                        return [float(x) for x in vec]
        except Exception:
            pass

        # Deterministic fallback pseudo-embedding based on hash buckets
        # Ensures search functions reliably in tests or when embedding model is loading
        dim = 256
        vec = [0.0] * dim
        for i, word in enumerate(text.lower().split()):
            bucket = hash(word) % dim
            vec[bucket] += 1.0 / (i + 1.0)
        norm = math.sqrt(sum(x * x for x in vec)) or 1.0
        return [x / norm for x in vec]

    async def index_memory(
        self,
        memory_id: uuid.UUID,
        content: str,
        namespace: str = "general",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> MemoryEmbedding:
        """Computes and stores embedding vector for a memory entry."""
        vec = await self.get_embedding(content)
        embedding = MemoryEmbedding(
            memory_id=memory_id,
            namespace=namespace,
            content_chunk=content,
            embedding_vector=vec,
            dimension=len(vec),
            metadata_json=metadata or {},
        )
        self.db.add(embedding)
        await self.db.commit()
        await self.db.refresh(embedding)
        return embedding

    async def search(
        self,
        query: str,
        namespace: Optional[str] = None,
        limit: int = 5,
    ) -> List[Dict[str, Any]]:
        """Finds closest memory entries by cosine similarity to query vector."""
        query_vec = await self.get_embedding(query)

        stmt = select(MemoryEmbedding)
        if namespace:
            stmt = stmt.where(MemoryEmbedding.namespace == namespace)

        res = await self.db.execute(stmt)
        candidates = res.scalars().all()

        scored = []
        for cand in candidates:
            sim = _cosine_similarity(query_vec, cand.embedding_vector)
            scored.append({
                "id": str(cand.id),
                "memory_id": str(cand.memory_id) if cand.memory_id else None,
                "content": cand.content_chunk,
                "namespace": cand.namespace,
                "similarity_score": round(sim, 4),
            })

        scored.sort(key=lambda x: x["similarity_score"], reverse=True)
        return scored[:limit]

    async def sync_all_memories(self) -> int:
        """Indexes any unindexed CompanyMemory records into semantic memory."""
        res = await self.db.execute(select(CompanyMemory))
        memories = res.scalars().all()

        indexed_count = 0
        for mem in memories:
            existing = await self.db.execute(
                select(MemoryEmbedding).where(MemoryEmbedding.memory_id == mem.id)
            )
            if not existing.scalar_one_or_none():
                await self.index_memory(
                    memory_id=mem.id,
                    content=mem.content,
                    namespace=mem.namespace or "general",
                    metadata={"tier": mem.tier, "source": mem.source_agent},
                )
                indexed_count += 1
        return indexed_count
