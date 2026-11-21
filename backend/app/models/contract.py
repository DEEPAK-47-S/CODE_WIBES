"""Legal Contract and Service Level Agreement (SLA) model."""
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Float, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Contract(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Client Service Agreement & NDA."""
    __tablename__ = "contracts"

    contract_number: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    client_name: Mapped[str] = mapped_column(String(150), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    
    project_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id"), nullable=True, index=True
    )
    
    terms_text: Mapped[str] = mapped_column(Text, nullable=False)
    total_value_inr: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    
    # Status: draft, founder_approved, client_signed, active, terminated
    status: Mapped[str] = mapped_column(String(30), default="draft", index=True, nullable=False)
    
    founder_signed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    client_signed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    project = relationship("Project", backref="contracts")
