"""Voice Call and Telephony Compliance model."""
import uuid
from typing import Optional
from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class VoiceCallRecord(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Voice call record managed by ElevenLabs voice agent adapter."""

    __tablename__ = "voice_call_records"

    lead_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("leads.id"), nullable=True, index=True
    )
    phone_number_masked: Mapped[str] = mapped_column(String(50), nullable=False)
    is_test_call: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Telephony Provider & ElevenLabs references
    provider: Mapped[str] = mapped_column(String(50), default="ElevenLabs", nullable=False)
    conversation_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    call_duration_seconds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Compliance & Consent
    dlt_template_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    consent_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    opt_out_detected: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    status: Mapped[str] = mapped_column(
        String(50), default="initiated", nullable=False
    )  # initiated, ringing, answered, completed, failed, blocked_compliance
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    transcript_redacted: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    call_metadata: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    def __repr__(self) -> str:
        return f"<VoiceCallRecord {self.phone_number_masked} status={self.status} test={self.is_test_call}>"
