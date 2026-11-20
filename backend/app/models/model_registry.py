"""Model registry entity for discovered Ollama models, runtime context, and capabilities."""
import uuid
from sqlalchemy import BigInteger, Boolean, Float, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class ModelRegistry(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Registered AI model discovered dynamically from local Ollama or cloud provider."""

    __tablename__ = "model_registry"

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    digest: Mapped[str | None] = mapped_column(String(100), nullable=True)
    size_bytes: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    parameter_size: Mapped[str | None] = mapped_column(String(50), nullable=True)
    quantization: Mapped[str | None] = mapped_column(String(50), nullable=True)
    
    # Context settings (Conservative default 8192 for 6GB VRAM)
    advertised_context: Mapped[int] = mapped_column(Integer, default=4096, nullable=False)
    runtime_context: Mapped[int] = mapped_column(Integer, default=8192, nullable=False)

    # Verified capabilities
    supports_tools: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    supports_vision: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    supports_thinking: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    supports_json: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Routing and benchmarks
    task_categories: Mapped[list | None] = mapped_column(JSON, default=list, nullable=True)
    latency_ms: Mapped[float | None] = mapped_column(Float, nullable=True)
    tokens_per_sec: Mapped[float | None] = mapped_column(Float, nullable=True)
    benchmark_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    
    status: Mapped[str] = mapped_column(String(50), default="ready", nullable=False)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    def __repr__(self) -> str:
        return f"<ModelRegistry {self.name} status={self.status} ctx={self.runtime_context}>"
