"""Social Media & Content Marketing Post model."""
from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Text, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class MarketingPost(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Generated marketing campaign, blog, or social post."""
    __tablename__ = "marketing_posts"

    # Platform: linkedin, x_twitter, tech_blog, newsletter
    platform: Mapped[str] = mapped_column(String(30), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    content_text: Mapped[str] = mapped_column(Text, nullable=False)
    hashtags: Mapped[List[str]] = mapped_column(JSONB, default=list, nullable=False)
    
    # Status: draft, founder_approved, published, rejected
    status: Mapped[str] = mapped_column(String(30), default="draft", index=True, nullable=False)
    scheduled_for: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # Agent author: StoryArc, ViralVox, Showcase
    created_by_agent: Mapped[str] = mapped_column(String(50), default="StoryArc", nullable=False)
