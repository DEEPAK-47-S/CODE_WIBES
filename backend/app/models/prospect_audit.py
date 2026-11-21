"""Prospect Website Audit model for automated client acquisition."""
import uuid
from typing import Any, Dict, List, Optional
from sqlalchemy import String, Integer, Boolean, Text, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class ProspectAudit(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Audit analysis and report for a discovered prospect website."""
    __tablename__ = "prospect_audits"

    lead_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("leads.id"), nullable=True, index=True
    )
    target_url: Mapped[str] = mapped_column(String(500), index=True, nullable=False)
    business_name: Mapped[str] = mapped_column(String(150), nullable=False)
    
    overall_score: Mapped[int] = mapped_column(Integer, default=50, nullable=False)
    performance_score: Mapped[int] = mapped_column(Integer, default=50, nullable=False)
    seo_score: Mapped[int] = mapped_column(Integer, default=50, nullable=False)
    mobile_friendly: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    ssl_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    issues_found: Mapped[List[Dict[str, Any]]] = mapped_column(JSONB, default=list, nullable=False)
    proposed_solutions: Mapped[List[Dict[str, Any]]] = mapped_column(JSONB, default=list, nullable=False)
    audit_report_html: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    outreach_pitch_draft: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    lead = relationship("Lead", backref="audits")
