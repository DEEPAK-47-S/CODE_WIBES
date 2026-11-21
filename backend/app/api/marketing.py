"""API v1 routes for Social Media, Thought Leadership, and Marketing Posts."""
import uuid
from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.services.marketing_service import MarketingService

router = APIRouter(prefix="/marketing", tags=["marketing"])


class PostGenerateRequest(BaseModel):
    platform: str
    topic: str
    key_insight: Optional[str] = None
    author_agent: str = "StoryArc"


@router.get("/posts")
async def get_posts(platform: Optional[str] = None, status: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    """List marketing and social media posts."""
    service = MarketingService(db)
    posts = await service.list_posts(platform, status)
    return [
        {
            "id": str(p.id),
            "platform": p.platform,
            "title": p.title,
            "content_text": p.content_text,
            "hashtags": p.hashtags,
            "status": p.status,
            "created_by_agent": p.created_by_agent,
            "published_at": p.published_at.isoformat() if p.published_at else None,
            "created_at": p.created_at.isoformat(),
        }
        for p in posts
    ]


@router.post("/posts/generate")
async def generate_post(req: PostGenerateRequest, db: AsyncSession = Depends(get_db)):
    """Generates thought leadership post and intercepts behind Founder Approval."""
    service = MarketingService(db)
    post = await service.generate_thought_leadership_post(
        platform=req.platform,
        topic=req.topic,
        key_insight=req.key_insight,
        author_agent=req.author_agent,
    )
    return {
        "id": str(post.id),
        "platform": post.platform,
        "title": post.title,
        "content": post.content_text,
        "status": post.status,
        "hashtags": post.hashtags,
    }


@router.post("/posts/{post_id}/publish")
async def publish_post(post_id: str, db: AsyncSession = Depends(get_db)):
    """Marks post as published upon Founder approval."""
    service = MarketingService(db)
    try:
        p_uuid = uuid.UUID(post_id)
        return await service.approve_and_publish(p_uuid)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
