"""Invoice model for billing, GST calculations, and payment tracking."""
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Invoice(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Client Invoice with GST and payment tracking."""
    __tablename__ = "invoices"

    invoice_number: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    client_name: Mapped[str] = mapped_column(String(150), nullable=False)
    client_email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    client_phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    project_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id"), nullable=True, index=True
    )
    proposal_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("proposal_drafts.id"), nullable=True, index=True
    )
    
    currency: Mapped[str] = mapped_column(String(10), default="INR", nullable=False)
    subtotal: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    gst_rate_pct: Mapped[float] = mapped_column(Float, default=18.0, nullable=False)
    gst_amount: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_amount: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    
    # Status: draft, sent, paid, overdue, cancelled
    status: Mapped[str] = mapped_column(String(30), default="draft", index=True, nullable=False)
    line_items: Mapped[List[Dict[str, Any]]] = mapped_column(JSONB, default=list, nullable=False)
    
    payment_link: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    payment_reference_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    paid_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    project = relationship("Project", backref="invoices")
    proposal = relationship("ProposalDraft", backref="invoices")
