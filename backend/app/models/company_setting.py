"""Company settings model for autonomy policies, kill switches, and budgets."""
import uuid

from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class CompanySetting(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """System-wide operational parameters and safety kill switches controlled by Founder."""

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
    founder_verified_phone: Mapped[str | None] = mapped_column(
        String(20), nullable=True
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

    def __repr__(self) -> str:
        return (
            f"<CompanySetting pause={self.emergency_pause_all_agents} "
            f"disable_ext={self.disable_external_actions}>"
        )
