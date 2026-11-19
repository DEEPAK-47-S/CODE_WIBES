"""Department model for company organization."""
from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Department(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Company department (e.g., Software Development, QA, Marketing)."""

    __tablename__ = "departments"

    name: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )
    slug: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )

    # Relationships
    agents = relationship("Agent", back_populates="department")

    def __repr__(self) -> str:
        return f"<Department {self.name}>"
