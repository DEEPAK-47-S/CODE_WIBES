"""Lead / Client CRM model for Lead Gen Agent."""
import uuid
from typing import Optional
from sqlalchemy import String, Text, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Lead(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Client lead discovered or managed by Lead Generation AI Agent."""

    __tablename__ = "leads"

    company_name: Mapped[str] = mapped_column(String(200), nullable=False)
    contact_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    contact_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    industry: Mapped[str] = mapped_column(String(100), default="Technology", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="new", nullable=False)  # new, contacted, proposal_sent, closed_won, closed_lost
    estimated_value: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    source: Mapped[str] = mapped_column(String(100), default="AI Lead Scraping", nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<Lead {self.company_name} ({self.status})>"
