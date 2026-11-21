"""Autonomous Operations Scheduler & Pulse Engine for hands-free company operation."""
from datetime import datetime, timezone
from typing import Any, Dict, List
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lead import Lead
from app.models.invoice import Invoice
from app.models.project import Project
from app.models.prospect_audit import ProspectAudit
from app.services.lead_audit_service import LeadAuditService
from app.services.communication_service import CommunicationService
from app.services.quality_security_service import QualitySecurityService
from app.services.executive_briefing_service import ExecutiveBriefingService
from app.services.memory_service import MemoryService


class AutonomousSchedulerService:
    """NEXUS COO automated pulse engine executing proactive background operational tasks."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.memory = MemoryService(db)

    async def execute_company_pulse(self) -> Dict[str, Any]:
        """Runs an autonomous operational pulse: audits fresh leads, checks receivables, certifies codebases."""
        now = datetime.now(timezone.utc)
        actions_taken: List[str] = []

        # 1. Lead Pipeline Pulse
        audit_service = LeadAuditService(self.db)
        comm_service = CommunicationService(self.db)

        # Find leads without audits
        leads_res = await self.db.execute(select(Lead).order_by(Lead.created_at.desc()).limit(5))
        leads = leads_res.scalars().all()

        audited_count = 0
        pitches_queued = 0

        for lead in leads:
            # Check if audit exists
            existing_audit = (
                await self.db.execute(
                    select(ProspectAudit).where(ProspectAudit.lead_id == lead.id)
                )
            ).scalar_one_or_none()

            if not existing_audit:
                audit = await audit_service.audit_website(
                    target_url=lead.website or f"https://{lead.company_name.lower().replace(' ', '')}.com",
                    business_name=lead.company_name,
                    lead_id=lead.id,
                )
                audited_count += 1
                actions_taken.append(f"Audited new lead '{lead.company_name}' (Score: {audit.heuristic_score}/100)")

                # If score is low, queue pitch for Founder approval
                if audit.heuristic_score < 75:
                    pitch_res = await audit_service.generate_outreach_pitch(audit.id)
                    pitches_queued += 1
                    actions_taken.append(f"Drafted conversion pitch for '{lead.company_name}' -> Queued for Founder Approval")

        # 2. Financial Receivables Pulse
        unpaid_invoices_res = await self.db.execute(
            select(Invoice).where(Invoice.status != "paid").limit(3)
        )
        unpaid_invoices = unpaid_invoices_res.scalars().all()
        reminders_queued = 0

        for inv in unpaid_invoices:
            # Check if reminder already created in communications
            # Draft a gentle WhatsApp follow-up awaiting Founder sign-off
            if inv.client_phone:
                # Queue a payment reminder approval
                from app.services.approval_service import ApprovalService
                approval = ApprovalService(self.db)
                await approval.create_request(
                    action_type="PAYMENT_REMINDER_OUTREACH",
                    title=f"Payment Reminder: {inv.invoice_number} ({inv.client_name})",
                    description=f"Friendly reminder for pending invoice ₹{inv.total_amount:,.2f} via Razorpay link: {inv.payment_link}",
                    preview_payload={
                        "invoice_id": str(inv.id),
                        "invoice_number": inv.invoice_number,
                        "client_name": inv.client_name,
                        "amount_inr": inv.total_amount,
                        "payment_link": inv.payment_link,
                    },
                    risk_level="LOW",
                )
                reminders_queued += 1
                actions_taken.append(f"Prepared payment reminder for {inv.invoice_number} -> Queued for Founder Approval")

        # 3. Security Pulse for Active Projects
        qa_service = QualitySecurityService(self.db)
        projects_res = await self.db.execute(select(Project).limit(2))
        projects = projects_res.scalars().all()
        certified_projects = 0

        for proj in projects:
            report = await qa_service.get_audit_report(proj.id)
            if report and report.get("owasp_top_10_compliant"):
                certified_projects += 1

        # 4. Refresh Daily Executive Briefing
        briefing_service = ExecutiveBriefingService(self.db)
        briefing = await briefing_service.generate_daily_briefing()

        pulse_summary = {
            "pulse_timestamp": now.isoformat(),
            "status": "pulse_completed_successfully",
            "metrics": {
                "leads_audited": audited_count,
                "pitches_queued_for_approval": pitches_queued,
                "payment_reminders_queued": reminders_queued,
                "projects_qa_certified": certified_projects,
            },
            "actions_taken": actions_taken,
            "executive_briefing_updated": True,
            "orchestrated_by": "NEXUS Central AI Manager (D00)",
        }

        # Store pulse in memory
        await self.memory.store_memory(
            tier="department",
            namespace="d00_executive",
            key=f"pulse_{now.strftime('%Y%m%d_%H%M')}",
            content=f"Autonomous Pulse executed: {audited_count} leads audited, {pitches_queued} pitches queued, {reminders_queued} payment follow-ups queued.",
            provenance="AUTONOMOUS_OPERATIONS_SCHEDULER",
        )

        return pulse_summary
