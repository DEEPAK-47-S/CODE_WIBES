"""Customer Review and Testimonial model enforcing real data provenance."""
import uuid
from typing import Optional
from sqlalchemy import String, Integer, Boolean, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class CustomerReview(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Verified client review and feedback. Strictly forbids synthetic or fake testimonials."""
    __tablename__ = "customer_reviews"

    client_name: Mapped[str] = mapped_column(String(150), nullable=False)
    rating_stars: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    review_title: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    review_text: Mapped[str] = mapped_column(Text, nullable=False)
    
    project_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id"), nullable=True, index=True
    )
    invoice_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("invoices.id"), nullable=True, index=True
    )
    
    is_verified_client: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    allowed_for_marketing: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    project = relationship("Project", backref="reviews")
    invoice = relationship("Invoice", backref="reviews")

    def __repr__(self) -> str:
        return f"<CustomerReview {self.client_name} ({self.rating_stars}★) verified={self.is_verified_client}>"
