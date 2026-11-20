"""Customer change request and feedback revision model."""
import uuid
from typing import Optional
from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class ChangeRequest(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Customer revision or change request submitted during staging review or post-delivery."""

    __tablename__ = "change_requests"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id"), index=True, nullable=False
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Scope determination: in-scope goes to revisions workflow; out-of-scope triggers Founder quote approval
    is_in_scope: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    estimated_hours: Mapped[int] = mapped_column(Integer, default=4, nullable=False)
    priority: Mapped[str] = mapped_column(String(20), default="medium", nullable=False)
    
    # Status: submitted, triaged, in_progress, verified_qa, closed
    status: Mapped[str] = mapped_column(String(30), default="submitted", index=True, nullable=False)
    resolution_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<ChangeRequest {self.title} in_scope={self.is_in_scope} status={self.status}>"
