"""Service for capturing customer requirements and compiling Founder-gated proposals."""
import uuid
from typing import Any, Dict, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.proposal import CustomerRequirementBrief, ProposalDraft
from app.services.approval_service import ApprovalService
from app.services.audit_service import AuditService


class RequirementProposalService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.approval = ApprovalService(db)
        self.audit = AuditService(db)

    async def create_requirement_brief(
        self,
        client_name: str,
        business_goals: str,
        required_pages: List[str],
        required_features: List[str],
        lead_id: Optional[uuid.UUID] = None,
        target_audience: str = "B2B / Direct Consumers",
        tech_stack_preference: str = "React + FastAPI + PostgreSQL",
        target_timeline_weeks: int = 2,
    ) -> CustomerRequirementBrief:
        """Create and store a validated customer requirement brief."""
        brief = CustomerRequirementBrief(
            lead_id=lead_id,
            client_name=client_name,
            business_goals=business_goals,
            required_pages=required_pages,
            required_features=required_features,
            target_audience=target_audience,
            tech_stack_preference=tech_stack_preference,
            target_timeline_weeks=target_timeline_weeks,
        )
        self.db.add(brief)
        await self.db.commit()
        await self.db.refresh(brief)

        await self.audit.log_event(
            actor_type="agent",
            action="customer_brief_created",
            resource_type="customer_requirement_brief",
            resource_id=brief.id,
            details={"client_name": client_name, "pages": required_pages},
            risk_level="MEDIUM",
        )
        return brief

    async def generate_proposal_draft(
        self,
        brief_id: uuid.UUID,
        estimated_hours: int = 40,
        rate_per_hour_inr: float = 1250.0,
    ) -> ProposalDraft:
        """Generate a complete scope and milestone proposal requiring Founder approval."""
        res = await self.db.execute(
            select(CustomerRequirementBrief).where(CustomerRequirementBrief.id == brief_id)
        )
        brief = res.scalar_one_or_none()
        if not brief:
            raise ValueError(f"Requirement brief {brief_id} not found.")

        total_cost = estimated_hours * rate_per_hour_inr

        milestones = [
            {"phase": "M1", "title": "Discovery & UI/UX Wireframes", "pct": 25, "days": 3},
            {"phase": "M2", "title": "Full-Stack Software Engineering", "pct": 45, "days": 6},
            {"phase": "M3", "title": "QA, Accessibility & Security Audit", "pct": 15, "days": 2},
            {"phase": "M4", "title": "Staging Review & Production Deployment", "pct": 15, "days": 3},
        ]

        acceptance_criteria = [
            "All specified pages render responsively across mobile, tablet, and desktop breakpoints.",
            "Backend APIs pass automated contract and validation tests with zero 500 errors.",
            "Form submissions and lead data persist reliably in PostgreSQL database.",
            "Site achieves zero OWASP Top 10 vulnerabilities during Sentinel security audit.",
        ]

        pricing_breakdown = {
            "ui_ux_design": total_cost * 0.25,
            "full_stack_engineering": total_cost * 0.50,
            "qa_security_audit": total_cost * 0.15,
            "staging_deployment": total_cost * 0.10,
            "total_inr": total_cost,
        }

        proposal = ProposalDraft(
            brief_id=brief.id,
            title=f"Software Solution Proposal: {brief.client_name}",
            scope_summary=(
                f"End-to-end digital solution for {brief.client_name}. "
                f"Scope includes {len(brief.required_pages or [])} custom responsive pages "
                f"({', '.join(brief.required_pages or [])}) and {len(brief.required_features or [])} functional features "
                f"built on {brief.tech_stack_preference}."
            ),
            milestones=milestones,
            acceptance_criteria=acceptance_criteria,
            estimated_hours=estimated_hours,
            total_cost_inr=total_cost,
            pricing_breakdown=pricing_breakdown,
            status="awaiting_approval",
        )
        self.db.add(proposal)
        await self.db.flush()

        # Submit to Founder Approval Inbox
        approval_req = await self.approval.create_request(
            action_type="send_proposal",
            title=f"Proposal Approval: {brief.client_name} (₹{total_cost:,.2f})",
            description=f"Generated proposal for {brief.client_name}. Requires Founder review before sending.",
            preview_payload={
                "proposal_id": str(proposal.id),
                "client": brief.client_name,
                "total_inr": total_cost,
                "pages": brief.required_pages,
                "milestones": milestones,
            },
            risk_level="HIGH",
        )
        proposal.approval_request_id = approval_req.id
        await self.db.commit()
        await self.db.refresh(proposal)

        return proposal
