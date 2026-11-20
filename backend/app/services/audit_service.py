"""Audit & Governance Service for recording immutable audit logs and evaluating safety policies."""
import hashlib
import json
import uuid
from typing import Any, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.activity_log import ActivityLog
from app.models.company_setting import CompanySetting


class AuditService:
    def __init__(self, db: AsyncSession):
        self.db = db

    @staticmethod
    def compute_hash(payload: Any) -> str:
        """Compute SHA-256 hash of a payload for tamper-evident provenance."""
        try:
            serialized = json.dumps(payload, sort_keys=True, default=str)
        except Exception:
            serialized = str(payload)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    async def get_or_create_settings(self) -> CompanySetting:
        """Fetch the singular company settings record or initialize safe defaults."""
        result = await self.db.execute(select(CompanySetting).limit(1))
        setting = result.scalar_one_or_none()
        if not setting:
            setting = CompanySetting(
                emergency_pause_all_agents=False,
                disable_external_actions=True,  # Safe default
                allow_calling_test_mode=True,
                allow_production_calling=False,  # Strict compliance lock
                max_concurrent_models=1,
                daily_call_limit=10,
                monthly_budget_cap_usd=1000.0,
            )
            self.db.add(setting)
            await self.db.commit()
            await self.db.refresh(setting)
        return setting

    async def log_event(
        self,
        actor_type: str,
        action: str,
        actor_id: Optional[uuid.UUID] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[uuid.UUID] = None,
        details: Optional[Dict[str, Any]] = None,
        input_payload: Optional[Any] = None,
        output_payload: Optional[Any] = None,
        policy_decision: str = "PERMITTED",
        risk_level: str = "LOW",
    ) -> ActivityLog:
        """Create an immutable structured audit log entry."""
        audit_details = details or {}
        if input_payload is not None:
            audit_details["input_hash"] = self.compute_hash(input_payload)
        if output_payload is not None:
            audit_details["output_hash"] = self.compute_hash(output_payload)
        audit_details["policy_decision"] = policy_decision
        audit_details["risk_level"] = risk_level

        log = ActivityLog(
            actor_type=actor_type,
            actor_id=actor_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=audit_details,
        )
        self.db.add(log)
        await self.db.commit()
        await self.db.refresh(log)
        return log

    async def verify_execution_policy(self, action_category: str) -> tuple[bool, str]:
        """
        Verify whether an action is allowed to proceed based on global kill switches.
        Returns: (allowed: bool, reason: str)
        """
        settings = await self.get_or_create_settings()
        if settings.emergency_pause_all_agents:
            return False, "BLOCKED: Emergency Pause is active across all company agents."

        if action_category in ["outbound_call", "external_email", "production_deploy", "publish_post"]:
            if settings.disable_external_actions:
                return False, f"BLOCKED: External actions are globally disabled by Founder policy for '{action_category}'."

        if action_category == "production_calling" and not settings.allow_production_calling:
            return False, "BLOCKED: Production calling is disabled pending telecom/TRAI registration."

        return True, "PERMITTED"
