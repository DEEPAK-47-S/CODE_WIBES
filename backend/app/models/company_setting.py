"""Company settings model for autonomy policies, kill switches, budgets, and API credentials."""
from typing import Any, Dict, Optional
from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class CompanySetting(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """System-wide operational parameters, safety kill switches, and API credentials controlled by Founder."""

    __tablename__ = "company_settings"

    # Global Safety Kill Switches
    emergency_pause_all_agents: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    disable_external_actions: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )

    # Calling Safety Gates (TRAI / Compliance)
    allow_calling_test_mode: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    allow_production_calling: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    founder_verified_phone: Mapped[Optional[str]] = mapped_column(
        String(30), nullable=True
    )

    # Resource & Budget Limits (RTX 4050 6GB VRAM safety)
    max_concurrent_models: Mapped[int] = mapped_column(
        Integer, default=1, nullable=False
    )
    daily_call_limit: Mapped[int] = mapped_column(
        Integer, default=10, nullable=False
    )
    monthly_budget_cap_usd: Mapped[float] = mapped_column(
        Float, default=1000.0, nullable=False
    )

    # Integration Credentials & API Keys (Managed from Frontend UI)
    google_maps_api_key: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    elevenlabs_api_key: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    elevenlabs_voice_id: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True
    )
    twilio_account_sid: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True
    )
    twilio_auth_token: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True
    )
    twilio_phone_number: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True
    )
    whatsapp_api_token: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    whatsapp_phone_number_id: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True
    )
    razorpay_key_id: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True
    )
    razorpay_key_secret: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True
    )
    stripe_api_key: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    cloud_llm_api_key: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    api_keys_json: Mapped[Dict[str, Any]] = mapped_column(
        JSONB, default=dict, nullable=False
    )

    def __repr__(self) -> str:
        return (
            f"<CompanySetting pause={self.emergency_pause_all_agents} "
            f"disable_ext={self.disable_external_actions}>"
        )
