"""Persistent 7-tier memory management and context checkpoint/resume service."""
import uuid
from typing import Any, Dict, List, Optional
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.memory import CompanyMemory, TaskCheckpoint

VALID_TIERS = {
    "constitution",
    "founder_preference",
    "department",
    "agent",
    "project",
    "task",
    "customer",
}


class MemoryService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def store_memory(
        self,
        tier: str,
        namespace: str,
        key: str,
        content: str,
        metadata_json: Optional[Dict[str, Any]] = None,
        provenance: Optional[str] = None,
        retention_policy: str = "permanent",
    ) -> CompanyMemory:
        """Store or update a memory record within one of the 7 memory tiers."""
        if tier not in VALID_TIERS:
            raise ValueError(f"Invalid memory tier '{tier}'. Must be one of: {VALID_TIERS}")

        # Check existing record
        res = await self.db.execute(
            select(CompanyMemory).where(
                CompanyMemory.tier == tier,
                CompanyMemory.namespace == namespace,
                CompanyMemory.key == key,
            )
        )
        existing = res.scalar_one_or_none()
        if existing:
            existing.content = content
            existing.metadata_json = metadata_json
            existing.provenance = provenance
            existing.retention_policy = retention_policy
            await self.db.commit()
            await self.db.refresh(existing)
            return existing

        new_mem = CompanyMemory(
            tier=tier,
            namespace=namespace,
            key=key,
            content=content,
            metadata_json=metadata_json,
            provenance=provenance,
            retention_policy=retention_policy,
        )
        self.db.add(new_mem)
        await self.db.commit()
        await self.db.refresh(new_mem)
        return new_mem

    async def search_memory(
        self,
        tier: Optional[str] = None,
        namespace: Optional[str] = None,
        search_query: Optional[str] = None,
        limit: int = 20,
    ) -> List[CompanyMemory]:
        """Search persistent memories filtered by tier, namespace, or content."""
        query = select(CompanyMemory)
        if tier:
            query = query.where(CompanyMemory.tier == tier)
        if namespace:
            query = query.where(CompanyMemory.namespace == namespace)
        if search_query:
            query = query.where(CompanyMemory.content.ilike(f"%{search_query}%"))

        query = query.order_by(CompanyMemory.created_at.desc()).limit(limit)
        res = await self.db.execute(query)
        return list(res.scalars().all())

    async def create_task_checkpoint(
        self,
        task_id: uuid.UUID,
        goal: str,
        completed_work: str,
        token_count_estimate: int,
        key_decisions: Optional[List[str]] = None,
        verified_facts: Optional[List[str]] = None,
        open_questions: Optional[List[str]] = None,
        next_exact_actions: Optional[List[str]] = None,
        file_paths: Optional[List[str]] = None,
        state_payload: Optional[Dict[str, Any]] = None,
        trigger_reason: str = "context_threshold_70%",
    ) -> TaskCheckpoint:
        """
        Create a durable checkpoint when context reaches 65-75% threshold.
        Saves goal, completed work, decisions, and exact next steps in PostgreSQL.
        """
        # Determine run number
        res = await self.db.execute(
            select(TaskCheckpoint)
            .where(TaskCheckpoint.task_id == task_id)
            .order_by(desc(TaskCheckpoint.run_number))
            .limit(1)
        )
        latest = res.scalar_one_or_none()
        next_run = (latest.run_number + 1) if latest else 1

        checkpoint = TaskCheckpoint(
            task_id=task_id,
            run_number=next_run,
            token_count_estimate=token_count_estimate,
            trigger_reason=trigger_reason,
            goal=goal,
            completed_work=completed_work,
            key_decisions=key_decisions or [],
            verified_facts=verified_facts or [],
            open_questions=open_questions or [],
            next_exact_actions=next_exact_actions or [],
            file_paths=file_paths or [],
            state_payload=state_payload or {},
        )
        self.db.add(checkpoint)
        await self.db.commit()
        await self.db.refresh(checkpoint)
        return checkpoint

    async def get_latest_checkpoint(self, task_id: uuid.UUID) -> Optional[TaskCheckpoint]:
        """Fetch the most recent checkpoint for a task to resume execution."""
        res = await self.db.execute(
            select(TaskCheckpoint)
            .where(TaskCheckpoint.task_id == task_id)
            .order_by(desc(TaskCheckpoint.run_number))
            .limit(1)
        )
        return res.scalar_one_or_none()

    @staticmethod
    def should_trigger_checkpoint(token_count: int, context_budget: int = 8192, threshold_pct: float = 0.70) -> bool:
        """Determine if context usage has hit the 65-75% checkpoint threshold."""
        return token_count >= (context_budget * threshold_pct)
