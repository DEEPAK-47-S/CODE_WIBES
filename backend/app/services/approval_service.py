"""Approval Service managing the Founder approval inbox, decisions, and task dependencies."""
from datetime import datetime, timezone
import uuid
from typing import Any, Dict, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.approval import ApprovalRequest, TaskDependency
from app.models.task import Task
from app.services.audit_service import AuditService


class ApprovalService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.audit = AuditService(db)

    async def create_request(
        self,
        action_type: str,
        title: str,
        agent_id: Optional[uuid.UUID] = None,
        task_id: Optional[uuid.UUID] = None,
        description: Optional[str] = None,
        preview_payload: Optional[Dict[str, Any]] = None,
        risk_level: str = "HIGH",
    ) -> ApprovalRequest:
        """Create an explicit approval request for Founder review."""
        req = ApprovalRequest(
            action_type=action_type,
            title=title,
            agent_id=agent_id,
            task_id=task_id,
            description=description,
            preview_payload=preview_payload or {},
            risk_level=risk_level,
            status="pending",
        )
        self.db.add(req)

        # Update task status to awaiting_approval if task_id provided
        if task_id:
            res = await self.db.execute(select(Task).where(Task.id == task_id))
            task = res.scalar_one_or_none()
            if task:
                task.status = "awaiting_approval"

        await self.db.commit()
        await self.db.refresh(req)

        await self.audit.log_event(
            actor_type="agent",
            actor_id=agent_id,
            action=f"approval_requested:{action_type}",
            resource_type="approval_request",
            resource_id=req.id,
            details={"title": title, "risk_level": risk_level},
            input_payload=preview_payload,
            policy_decision="APPROVAL_REQUIRED",
            risk_level=risk_level,
        )
        return req

    async def decide_request(
        self,
        request_id: uuid.UUID,
        approved: bool,
        founder_feedback: Optional[str] = None,
    ) -> ApprovalRequest:
        """Process Founder decision on an approval request."""
        res = await self.db.execute(
            select(ApprovalRequest).where(ApprovalRequest.id == request_id)
        )
        req = res.scalar_one_or_none()
        if not req:
            raise ValueError(f"Approval request {request_id} not found.")

        req.status = "approved" if approved else "rejected"
        req.founder_feedback = founder_feedback
        req.decided_at = datetime.now(timezone.utc)

        # Update task status accordingly
        if req.task_id:
            res_task = await self.db.execute(select(Task).where(Task.id == req.task_id))
            task = res_task.scalar_one_or_none()
            if task:
                task.status = "approved" if approved else "rejected"

        await self.db.commit()
        await self.db.refresh(req)

        await self.audit.log_event(
            actor_type="founder",
            action=f"approval_decided:{req.status}",
            resource_type="approval_request",
            resource_id=req.id,
            details={"approved": approved, "feedback": founder_feedback},
            policy_decision="APPROVED" if approved else "REJECTED",
            risk_level="CRITICAL" if req.risk_level == "CRITICAL" else "HIGH",
        )
        return req

    async def list_pending_requests(self) -> List[ApprovalRequest]:
        """Fetch all requests currently pending Founder decision."""
        res = await self.db.execute(
            select(ApprovalRequest)
            .where(ApprovalRequest.status == "pending")
            .order_by(ApprovalRequest.created_at.desc())
        )
        return list(res.scalars().all())

    async def can_task_run(self, task_id: uuid.UUID) -> tuple[bool, str]:
        """Verify whether all prerequisite task dependencies have reached 'completed' status."""
        res = await self.db.execute(
            select(TaskDependency).where(TaskDependency.task_id == task_id)
        )
        deps = res.scalars().all()
        if not deps:
            return True, "No dependencies"

        for dep in deps:
            res_parent = await self.db.execute(
                select(Task).where(Task.id == dep.depends_on_task_id)
            )
            parent = res_parent.scalar_one_or_none()
            if not parent or parent.status != "completed":
                parent_title = parent.title if parent else str(dep.depends_on_task_id)
                return False, f"Blocked by dependency task: '{parent_title}' (status: {parent.status if parent else 'missing'})"

        return True, "All dependencies completed"
