"""CODE WIBES — FastAPI application entry point."""
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.config import settings
from app.database.session import engine, AsyncSessionLocal
from app.api.router import api_v1_router
from app.services.company_service import CompanyService

# Import models so SQLAlchemy registers them with Base.metadata
import app.models  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle."""
    # Seed initial company structure if DB is clean
    async with AsyncSessionLocal() as session:
        try:
            service = CompanyService(session)
            await service.seed_initial_company()
            await service.sync_full_organization()
        except Exception as e:
            print(f"Warning during seed: {e}")

    yield
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered Software Company Operating System",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS — allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API v1
app.include_router(api_v1_router)


@app.get("/")
async def root():
    """Root endpoint — basic platform info."""
    return {
        "company": settings.APP_NAME,
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health")
async def health():
    """Application health check."""
    return {"status": "healthy"}


@app.get("/health/database")
async def database_health():
    """Database connectivity health check."""
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        return {
            "database": "connected",
            "status": "healthy",
        }
    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed. Check server logs.",
        ) from error
