"""Vector and semantic memory embedding model."""
import uuid
from typing import Any, Dict, List, Optional
from sqlalchemy import String, Integer, Text, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class MemoryEmbedding(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Vector representation of company memories and code knowledge chunks."""
    __tablename__ = "memory_embeddings"

    memory_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("company_memories.id"), nullable=True, index=True
    )
    namespace: Mapped[str] = mapped_column(String(50), default="general", index=True, nullable=False)
    content_chunk: Mapped[str] = mapped_column(Text, nullable=False)
    embedding_vector: Mapped[List[float]] = mapped_column(JSONB, default=list, nullable=False)
    dimension: Mapped[int] = mapped_column(Integer, default=768, nullable=False)
    metadata_json: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)

    memory = relationship("CompanyMemory", backref="embeddings")
