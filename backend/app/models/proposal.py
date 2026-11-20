"""Customer Requirement Brief and Proposal models."""
import uuid
from typing import Optional
from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class CustomerRequirementBrief(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Structured client requirement brief captured by Discovery & Solutions agents."""

    __tablename__ = "customer_requirement_briefs"

    lead_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("leads.id"), nullable=True, index=True
    )
    client_name: Mapped[str] = mapped_column(String(200), nullable=False)
    business_goals: Mapped[str] = mapped_column(Text, nullable=False)
    target_audience: Mapped[str] = mapped_column(String(200), default="B2B / Consumers", nullable=False)
    
    required_pages: Mapped[list | None] = mapped_column(JSON, default=list, nullable=True)
    required_features: Mapped[list | None] = mapped_column(JSON, default=list, nullable=True)
    tech_stack_preference: Mapped[str] = mapped_column(String(100), default="React + FastAPI + PostgreSQL", nullable=False)
    
    brand_guidelines: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    client_budget_range: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    target_timeline_weeks: Mapped[int] = mapped_column(Integer, default=2, nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    def __repr__(self) -> str:
        return f"<CustomerRequirementBrief {self.client_name} v{self.version}>"


class ProposalDraft(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Formal business proposal and quotation requiring human Founder approval before dispatch."""

    __tablename__ = "proposal_drafts"

    brief_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("customer_requirement_briefs.id"), index=True, nullable=False
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    scope_summary: Mapped[str] = mapped_column(Text, nullable=False)
    milestones: Mapped[list | None] = mapped_column(JSON, default=list, nullable=True)
    acceptance_criteria: Mapped[list | None] = mapped_column(JSON, default=list, nullable=True)
    
    estimated_hours: Mapped[int] = mapped_column(Integer, default=40, nullable=False)
    total_cost_inr: Mapped[float] = mapped_column(Float, default=50000.0, nullable=False)
    pricing_breakdown: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    
    status: Mapped[str] = mapped_column(
        String(50), default="draft", nullable=False
    )  # draft, awaiting_approval, approved, sent_to_client, rejected
    approval_request_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("approval_requests.id"), nullable=True
    )

    def __repr__(self) -> str:
        return f"<ProposalDraft {self.title} total=₹{self.total_cost_inr} status={self.status}>"
