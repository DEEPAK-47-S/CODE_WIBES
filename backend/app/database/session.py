"""Async database session management and dependency injection."""
from collections.abc import AsyncGenerator

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

database_url = URL.create(
    drivername="postgresql+asyncpg",
    username=settings.PGUSER,
    password=settings.PGPASSWORD,
    host=settings.PGHOST,
    port=settings.PGPORT,
    database=settings.PGDATABASE,
)

engine = create_async_engine(
    database_url,
    echo=False,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields an async database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
