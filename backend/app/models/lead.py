"""Lead / Client CRM model with Google Places deduplication and compliance provenance."""
import uuid
from typing import Optional
from sqlalchemy import Boolean, Float, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Lead(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Client lead discovered through Google Places API (New) or first-party research."""

    __tablename__ = "leads"

    company_name: Mapped[str] = mapped_column(String(200), nullable=False)
    contact_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    contact_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    has_website: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Geographic discovery
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    district: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, default="Coimbatore")
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, default="Tamil Nadu")

    industry: Mapped[str] = mapped_column(String(100), default="Technology", nullable=False)
    status: Mapped[str] = mapped_column(
        String(50), default="new", nullable=False
    )  # new, researching, qualified, not_qualified, needs_consent, consent_verified, call_ready, contacted, interested, follow_up, proposal_draft, converted, do_not_contact

    # Google Places compliance & deduplication
    place_id: Mapped[Optional[str]] = mapped_column(String(150), unique=True, index=True, nullable=True)
    rating: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    review_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    google_attribution_required: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Consent & Telecom Compliance
    consent_status: Mapped[str] = mapped_column(
        String(50), default="needs_consent", nullable=False
    )  # needs_consent, consent_verified, opt_out, suppressed
    qualification_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    estimated_value: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    source: Mapped[str] = mapped_column(String(100), default="Google Places API (New)", nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    provenance_metadata: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    @property
    def business_name(self) -> str:
        return self.company_name

    @business_name.setter
    def business_name(self, value: str) -> None:
        self.company_name = value

    def __repr__(self) -> str:
        return f"<Lead {self.company_name} ({self.status}) place_id={self.place_id}>"
