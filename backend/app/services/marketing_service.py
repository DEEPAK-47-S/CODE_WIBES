"""Marketing & Content Strategy Service for thought leadership, social posts, and case studies."""
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.marketing_post import MarketingPost
from app.services.approval_service import ApprovalService
from app.services.audit_service import AuditService


class MarketingService:
    """Manages AI-authored marketing campaigns, thought leadership posts, and approval queues."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.approval = ApprovalService(db)
        self.audit = AuditService(db)

    async def generate_thought_leadership_post(
        self,
        platform: str,
        topic: str,
        key_insight: Optional[str] = None,
        author_agent: str = "StoryArc",
    ) -> MarketingPost:
        """Drafts a platform-native social or blog post and queues for Founder Approval."""
        platform = platform.lower()
        key_insight = key_insight or "Autonomous software engineering accelerates delivery while ensuring strict verification."

        if platform == "linkedin":
            title = f"The Future of Software Engineering: {topic}"
            content = (
                f"🚀 How we approach {topic} at CODE WIBES TECHNOLOGIES:\n\n"
                f"Traditional software cycles often struggle with requirement drift and manual QA bottlenecks. "
                f"By organizing specialist AI agents across architecture, security, and testing, "
                f"we eliminate repetitive delays while keeping the Founder firmly in control.\n\n"
                f"💡 Key Takeaway: {key_insight}\n\n"
                f"What is your team's biggest challenge in modern web delivery? Let's discuss in the comments below."
            )
            hashtags = ["#AI", "#SoftwareEngineering", "#Startups", "#TechLeadership", "#CODEWIBES"]

        elif platform == "x_twitter":
            title = f"Thread on {topic}"
            content = (
                f"1/4 How autonomous AI agents transform {topic} at @CodeWibes:\n\n"
                f"Instead of a monolithic bot, we deploy 10 specialized departments with strict verifier loops.\n\n"
                f"2/4 Key insight: {key_insight}\n\n"
                f"3/4 Zero fake data. Zero unverified code. Every consequential action requires human founder sign-off.\n\n"
                f"4/4 Built for the modern enterprise. 🧵👇"
            )
            hashtags = ["#BuildInPublic", "#AIStartups", "#TechTrends"]

        else:  # tech_blog
            title = f"Architecting High-Speed Solutions for {topic}"
            content = (
                f"# Architecting High-Speed Solutions for {topic}\n\n"
                f"### By {author_agent} & DEEPAKUMAR.S (Founder)\n\n"
                f"In this technical breakdown, we examine how autonomous software pipelines "
                f"deliver robust web applications with zero compromise on code quality.\n\n"
                f"#### Core Principles:\n"
                f"- **Strict Data Provenance**: No synthetic leads or mock revenue.\n"
                f"- **Hardware Safety**: Sequential local inference on RTX GPUs.\n"
                f"- **{key_insight}**\n\n"
                f"Explore our live client builds at https://codewibes.com"
            )
            hashtags = ["#WebDev", "#Architecture", "#FastAPI", "#React"]

        post = MarketingPost(
            platform=platform,
            title=title,
            content_text=content,
            hashtags=hashtags,
            status="draft",
            created_by_agent=author_agent,
        )
        self.db.add(post)
        await self.db.flush()

        # Intercept behind Founder Approval
        await self.approval.create_request(
            action_type="PUBLISH_MARKETING_POST",
            title=f"Publish {platform.capitalize()} Post: {title[:40]}...",
            description=f"Drafted by {author_agent}. Review content before broadcast.",
            preview_payload={
                "post_id": str(post.id),
                "platform": platform,
                "title": title,
                "content": content,
            },
            risk_level="LOW",
        )
        await self.db.commit()
        await self.db.refresh(post)
        return post

    async def approve_and_publish(self, post_id: uuid.UUID) -> Dict[str, Any]:
        """Marks post as published upon Founder approval."""
        res = await self.db.execute(select(MarketingPost).where(MarketingPost.id == post_id))
        post = res.scalar_one_or_none()
        if not post:
            raise ValueError(f"Post {post_id} not found.")

        post.status = "published"
        post.published_at = datetime.now(timezone.utc)
        await self.db.commit()

        return {
            "status": "published",
            "post_id": str(post.id),
            "platform": post.platform,
            "published_at": post.published_at.isoformat(),
        }

    async def list_posts(self, platform: Optional[str] = None, status: Optional[str] = None) -> List[MarketingPost]:
        """Lists marketing posts with optional filters."""
        stmt = select(MarketingPost).order_by(MarketingPost.created_at.desc())
        if platform:
            stmt = stmt.where(MarketingPost.platform == platform.lower())
        if status:
            stmt = stmt.where(MarketingPost.status == status.lower())
        res = await self.db.execute(stmt)
        return res.scalars().all()
