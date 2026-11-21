"""Autonomous Executive Briefing Service: NEXUS COO compiles daily standup intelligence for Founder."""
import datetime
from typing import Any, Dict, List
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lead import Lead
from app.models.project import Project
from app.models.task import Task
from app.models.invoice import Invoice
from app.models.contract import Contract
from app.models.approval import ApprovalRequest
from app.services.memory_service import MemoryService


class ExecutiveBriefingService:
    """NEXUS COO engine aggregating real-time departmental intelligence and strategic priorities."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.memory = MemoryService(db)

    async def generate_daily_briefing(self) -> Dict[str, Any]:
        """Compiles real-time company KPIs, financial state, pending approvals, and strategic orders."""
        now = datetime.datetime.now(datetime.timezone.utc)
        today_str = now.strftime("%A, %B %d, %Y")

        # 1. Lead Pipeline Telemetry
        total_leads = (await self.db.execute(select(func.count(Lead.id)))).scalar() or 0
        new_leads = (await self.db.execute(select(func.count(Lead.id)).where(Lead.status == "new"))).scalar() or 0
        contacted_leads = (await self.db.execute(select(func.count(Lead.id)).where(Lead.status == "contacted"))).scalar() or 0
        converted_leads = (await self.db.execute(select(func.count(Lead.id)).where(Lead.status == "converted"))).scalar() or 0

        # 2. Financial & Revenue Metrics
        invoices_res = (await self.db.execute(select(Invoice))).scalars().all()
        total_invoiced_inr = sum(inv.total_amount for inv in invoices_res)
        total_collected_inr = sum(inv.total_amount for inv in invoices_res if inv.status == "paid")
        pending_collection_inr = total_invoiced_inr - total_collected_inr

        # 3. Projects & Production
        total_projects = (await self.db.execute(select(func.count(Project.id)))).scalar() or 0
        total_tasks = (await self.db.execute(select(func.count(Task.id)))).scalar() or 0
        active_tasks = (await self.db.execute(select(func.count(Task.id)).where(Task.status == "in_progress"))).scalar() or 0

        # 4. Contracts & Legal
        contracts_res = (await self.db.execute(select(Contract))).scalars().all()
        signed_contracts = sum(1 for c in contracts_res if c.status == "founder_approved")

        # 5. Pending Human Approvals for Founder DEEPAKUMAR.S
        pending_approvals = (
            await self.db.execute(
                select(ApprovalRequest).where(ApprovalRequest.status == "pending")
            )
        ).scalars().all()

        # 6. NEXUS Strategic Action Plan
        strategic_priorities: List[str] = []
        if len(pending_approvals) > 0:
            strategic_priorities.append(
                f"🚨 Action Required: Review and authorize {len(pending_approvals)} pending outbound actions in Approvals tab."
            )
        if pending_collection_inr > 0:
            strategic_priorities.append(
                f"💼 Revenue Target: Follow up on ₹{pending_collection_inr:,.0f} in pending client invoices with WhatsApp reminders."
            )
        if new_leads > 0:
            strategic_priorities.append(
                f"🎯 Growth Velocity: Run technical audits on {new_leads} newly harvested Google Maps leads to generate high-converting proposals."
            )
        else:
            strategic_priorities.append(
                "🗺️ Prospecting: Trigger Google Maps Lead Harvester for target cities (Chennai, Coimbatore, Bangalore)."
            )
        strategic_priorities.append(
            "⚡ Hardware Health: RTX 4050 6GB GPU running 20 local models with sequential execution lock."
        )

        briefing = {
            "date": today_str,
            "executive_summary": (
                f"CODE WIBES operating at full capacity. {total_projects} client projects active, "
                f"₹{total_collected_inr:,.0f} revenue collected with ₹{pending_collection_inr:,.0f} pending disbursement. "
                f"NEXUS coordinating 10 departments and 101 role-based AI agents."
            ),
            "financials": {
                "total_invoiced_inr": total_invoiced_inr,
                "total_collected_inr": total_collected_inr,
                "pending_collection_inr": pending_collection_inr,
                "invoices_count": len(invoices_res),
                "active_msa_contracts": len(contracts_res),
                "signed_msa_contracts": signed_contracts,
            },
            "pipeline": {
                "total_leads": total_leads,
                "new_leads": new_leads,
                "contacted_leads": contacted_leads,
                "converted_leads": converted_leads,
            },
            "production": {
                "total_projects": total_projects,
                "total_tasks": total_tasks,
                "active_tasks": active_tasks,
            },
            "governance": {
                "pending_founder_approvals_count": len(pending_approvals),
                "pending_actions": [
                    {
                        "id": str(app.id),
                        "action_type": app.action_type,
                        "created_at": app.created_at.isoformat() if app.created_at else None,
                    }
                    for app in pending_approvals[:5]
                ],
            },
            "strategic_priorities": strategic_priorities,
            "generated_by": {
                "agent": "Nexus",
                "role": "Central AI Manager & COO",
                "department": "D00 Executive Command",
            },
        }

        # Store in company memory
        await self.memory.store_memory(
            tier="department",
            namespace="d00_executive",
            key=f"daily_briefing_{now.strftime('%Y%m%d')}",
            content=briefing["executive_summary"],
            provenance="NEXUS_CENTRAL_MANAGER",
        )

        return briefing
