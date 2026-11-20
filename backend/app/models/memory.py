"""Persistent 7-tier memory and task checkpoint models."""
import uuid
from sqlalchemy import BigInteger, Boolean, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class CompanyMemory(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """
    Persistent 7-tier memory stored in PostgreSQL outside model context.
    Tiers:
    1. constitution - Hard company rules and branding
    2. founder_preference - Founder directives and decisions
    3. department - Department standard operating procedures (SOPs)
    4. agent - Agent-specific memory and successful patterns
    5. project - Client project scope, decisions, milestones
    6. task - Task input, execution traces, artifacts
    7. customer - Tenant-scoped privacy-compliant client memory
    """

    __tablename__ = "company_memories"

    tier: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    namespace: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    key: Mapped[str] = mapped_column(String(150), index=True, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    metadata_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    provenance: Mapped[str | None] = mapped_column(String(255), nullable=True)
    retention_policy: Mapped[str] = mapped_column(String(50), default="permanent", nullable=False)

    def __repr__(self) -> str:
        return f"<CompanyMemory tier={self.tier} namespace={self.namespace} key={self.key}>"


class TaskCheckpoint(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """
    Checkpoint created when task context reaches 65-75% budget threshold.
    Enables starting a clean model context without losing work or resetting models.
    """

    __tablename__ = "task_checkpoints"

    task_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tasks.id"), index=True, nullable=False
    )
    run_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    token_count_estimate: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    trigger_reason: Mapped[str] = mapped_column(
        String(100), default="context_threshold_70%", nullable=False
    )
    
    # Structured checkpoint summary
    goal: Mapped[str] = mapped_column(Text, nullable=False)
    completed_work: Mapped[str] = mapped_column(Text, nullable=False)
    key_decisions: Mapped[list | None] = mapped_column(JSON, default=list, nullable=True)
    verified_facts: Mapped[list | None] = mapped_column(JSON, default=list, nullable=True)
    open_questions: Mapped[list | None] = mapped_column(JSON, default=list, nullable=True)
    next_exact_actions: Mapped[list | None] = mapped_column(JSON, default=list, nullable=True)
    file_paths: Mapped[list | None] = mapped_column(JSON, default=list, nullable=True)
    state_payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    def __repr__(self) -> str:
        return f"<TaskCheckpoint task={self.task_id} run={self.run_number} reason={self.trigger_reason}>"
