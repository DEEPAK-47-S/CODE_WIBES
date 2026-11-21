"""API routes for persistent 7-tier memory and task checkpoints."""
import uuid
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.services.memory_service import MemoryService

router = APIRouter(prefix="/memory", tags=["Persistent Memory"])


class MemoryCreateSchema(BaseModel):
    tier: str
    namespace: str
    key: str
    content: str
    metadata_json: Optional[Dict[str, Any]] = None
    provenance: Optional[str] = None
    retention_policy: str = "permanent"


class CheckpointCreateSchema(BaseModel):
    task_id: uuid.UUID
    goal: str
    completed_work: str
    token_count_estimate: int
    key_decisions: Optional[List[str]] = None
    verified_facts: Optional[List[str]] = None
    open_questions: Optional[List[str]] = None
    next_exact_actions: Optional[List[str]] = None
    file_paths: Optional[List[str]] = None
    state_payload: Optional[Dict[str, Any]] = None
    trigger_reason: str = "context_threshold_70%"


@router.get("")
async def search_memories(
    tier: Optional[str] = None,
    namespace: Optional[str] = None,
    q: Optional[str] = None,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
):
    """Query persistent memories across the 7 tiers."""
    service = MemoryService(db)
    items = await service.search_memory(tier=tier, namespace=namespace, search_query=q, limit=limit)
    return [
        {
            "id": str(m.id),
            "tier": m.tier,
            "namespace": m.namespace,
            "key": m.key,
            "content": m.content,
            "metadata": m.metadata_json,
            "provenance": m.provenance,
            "created_at": m.created_at.isoformat() if m.created_at else None,
        }
        for m in items
    ]


@router.post("")
async def create_memory(data: MemoryCreateSchema, db: AsyncSession = Depends(get_db)):
    """Store or update a memory record in a specified tier."""
    service = MemoryService(db)
    try:
        mem = await service.store_memory(
            tier=data.tier,
            namespace=data.namespace,
            key=data.key,
            content=data.content,
            metadata_json=data.metadata_json,
            provenance=data.provenance,
            retention_policy=data.retention_policy,
        )
        return {
            "status": "stored",
            "id": str(mem.id),
            "tier": mem.tier,
            "namespace": mem.namespace,
            "key": mem.key,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/checkpoints")
async def create_task_checkpoint(data: CheckpointCreateSchema, db: AsyncSession = Depends(get_db)):
    """Save a task checkpoint when context reaches 65-75% budget threshold."""
    service = MemoryService(db)
    chk = await service.create_task_checkpoint(
        task_id=data.task_id,
        goal=data.goal,
        completed_work=data.completed_work,
        token_count_estimate=data.token_count_estimate,
        key_decisions=data.key_decisions,
        verified_facts=data.verified_facts,
        open_questions=data.open_questions,
        next_exact_actions=data.next_exact_actions,
        file_paths=data.file_paths,
        state_payload=data.state_payload,
        trigger_reason=data.trigger_reason,
    )
    return {
        "status": "checkpoint_created",
        "checkpoint_id": str(chk.id),
        "task_id": str(chk.task_id),
        "run_number": chk.run_number,
        "trigger_reason": chk.trigger_reason,
    }


@router.get("/checkpoints/{task_id}/latest")
async def get_latest_task_checkpoint(task_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Retrieve the latest checkpoint for a task to resume execution."""
    service = MemoryService(db)
    chk = await service.get_latest_checkpoint(task_id)
    if not chk:
        raise HTTPException(status_code=404, detail="No checkpoint found for task.")
    return {
        "checkpoint_id": str(chk.id),
        "task_id": str(chk.task_id),
        "run_number": chk.run_number,
        "goal": chk.goal,
        "completed_work": chk.completed_work,
        "key_decisions": chk.key_decisions,
        "verified_facts": chk.verified_facts,
        "open_questions": chk.open_questions,
        "next_exact_actions": chk.next_exact_actions,
        "file_paths": chk.file_paths,
        "trigger_reason": chk.trigger_reason,
        "created_at": chk.created_at.isoformat() if chk.created_at else None,
    }


@router.get("/semantic-search")
async def semantic_search_memories(
    q: str,
    namespace: Optional[str] = None,
    limit: int = 5,
    db: AsyncSession = Depends(get_db),
):
    """Vector cosine similarity search over persistent company memories."""
    from app.services.semantic_memory_service import SemanticMemoryService
    service = SemanticMemoryService(db)
    return await service.search(query=q, namespace=namespace, limit=limit)


@router.post("/sync-embeddings")
async def sync_memory_embeddings(db: AsyncSession = Depends(get_db)):
    """Indexes all unindexed company memories into vector embeddings."""
    from app.services.semantic_memory_service import SemanticMemoryService
    service = SemanticMemoryService(db)
    indexed = await service.sync_all_memories()
    return {"status": "synced", "indexed_memories_count": indexed}

