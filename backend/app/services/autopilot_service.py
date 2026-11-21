"""Master Autonomous Auto-Pilot Service — Orchestrates the complete 10-department company lifecycle."""
import uuid
from typing import Any, Dict, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lead import Lead
from app.models.project import Project
from app.services.lead_audit_service import LeadAuditService
from app.services.communication_service import CommunicationService
from app.services.voice_service import VoiceService
from app.services.requirement_proposal_service import RequirementProposalService
from app.services.website_factory_service import WebsiteFactoryService
from app.services.billing_contract_service import BillingContractService
from app.services.marketing_service import MarketingService
from app.services.audit_service import AuditService
from app.services.memory_service import MemoryService


class AutopilotService:
    """Executes the complete autonomous end-to-end company workflow from lead to live staging & billing."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.audit_svc = AuditService(db)
        self.memory = MemoryService(db)

    async def run_full_company_pipeline(
        self,
        business_name: str,
        website_url: str,
        phone: str = "+91 98400 12345",
        location: str = "Coimbatore, Tamil Nadu",
        category: str = "Enterprise Manufacturing & Retail",
    ) -> Dict[str, Any]:
        """Runs the entire 10-department autonomous pipeline for a prospective client."""
        settings = await self.audit_svc.get_or_create_settings()
        if settings.emergency_pause_all_agents:
            raise PermissionError("Autonomous pipeline halted: Emergency Pause is active.")

        pipeline_log: List[Dict[str, str]] = []

        # -----------------------------------------------------------------
        # STAGE 1: Lead Intelligence (D02 - Hunter & Cartographer)
        # -----------------------------------------------------------------
        res_lead = await self.db.execute(select(Lead).where(Lead.company_name == business_name))
        lead = res_lead.scalar_one_or_none()
        if not lead:
            lead = Lead(
                company_name=business_name,
                place_id=f"pl-{uuid.uuid4().hex[:12]}",
                industry=category,
                district=location,
                phone=phone,
                website=website_url,
                rating=4.8,
                review_count=35,
                source="AUTONOMOUS_DISCOVERY",
                status="new",
            )
            self.db.add(lead)
            await self.db.commit()
            await self.db.refresh(lead)

        pipeline_log.append({
            "stage": "Stage 1: Lead Discovery",
            "department": "D02 Lead Intelligence",
            "agent": "Hunter",
            "outcome": f"Lead '{business_name}' qualified and registered.",
        })

        # -----------------------------------------------------------------
        # STAGE 2: Technical Web & SEO Audit (D02 - WebAudit & D09 - RankCraft)
        # -----------------------------------------------------------------
        lead_audit_svc = LeadAuditService(self.db)
        audit_res = await lead_audit_svc.audit_website(
            target_url=website_url,
            business_name=business_name,
            lead_id=lead.id,
        )
        pipeline_log.append({
            "stage": "Stage 2: Technical Web Audit",
            "department": "D02 / D09 SEO",
            "agent": "WebAudit & RankCraft",
            "outcome": f"Site scored {audit_res.overall_score}/100. Issues identified: {len(audit_res.issues_found)}.",
        })

        # -----------------------------------------------------------------
        # STAGE 3: Multi-Channel Contact & WhatsApp (D03 - Venture & AriaVoice)
        # -----------------------------------------------------------------
        comm_svc = CommunicationService(self.db)
        wa_res = await comm_svc.draft_whatsapp_outreach(
            lead_id=lead.id,
            audit_score=audit_res.overall_score,
        )
        voice_svc = VoiceService(self.db)
        voice_res = await voice_svc.initiate_voice_call(
            phone_number=phone,
            lead_id=lead.id,
            script_purpose=f"Solution discovery for {business_name}",
            is_test_call=True,
        )
        pipeline_log.append({
            "stage": "Stage 3: Multi-Channel Outreach",
            "department": "D03 Sales & Voice",
            "agent": "Venture & AriaVoice",
            "outcome": f"WhatsApp pitch drafted (Click-to-chat ready) + Test Voice Call recorded ({voice_res.get('status')}).",
        })

        # -----------------------------------------------------------------
        # STAGE 4: Requirements & Proposal Architecture (D04 - Blueprint)
        # -----------------------------------------------------------------
        req_svc = RequirementProposalService(self.db)
        brief = await req_svc.create_requirement_brief(
            client_name=business_name,
            business_goals=f"Modernize {business_name}'s web presence with sub-second performance.",
            required_pages=["Home", "Services", "Portfolio", "Quote & Contact"],
            required_features=["Mobile Responsive Layout", "FastAPI Lead Capture", "WhatsApp Live Chat"],
            lead_id=lead.id,
            tech_stack_preference="React + Tailwind + FastAPI",
            target_timeline_weeks=2,
        )
        proposal = await req_svc.generate_proposal_draft(brief_id=brief.id, estimated_hours=40, rate_per_hour_inr=1500.0)
        pipeline_log.append({
            "stage": "Stage 4: Requirement Architecture",
            "department": "D04 Solution Architecture",
            "agent": "Blueprint & AnalystPrime",
            "outcome": f"Brief #{str(brief.id)[:8]} and Proposal drafted (Total: ₹{proposal.total_cost_inr:,.2f}).",
        })

        # -----------------------------------------------------------------
        # STAGE 5: UI/UX & Website Factory 2.0 (D05 - Aura & D06 - Forge)
        # -----------------------------------------------------------------
        proj = Project(
            name=f"Digital Platform: {business_name}",
            description=f"Autonomous delivery for {business_name} orchestrated by NEXUS.",
            status="in_progress",
            priority="high",
            progress=40,
        )
        self.db.add(proj)
        await self.db.commit()
        await self.db.refresh(proj)

        factory = WebsiteFactoryService(self.db)
        codebase_res = await factory.create_isolated_project_workspace(
            project_id=proj.id,
            project_name=business_name,
            tech_stack="React + Tailwind + FastAPI",
            pages=brief.required_pages,
            features=brief.required_features,
        )
        pipeline_log.append({
            "stage": "Stage 5: Software Engineering",
            "department": "D06 Software Engineering",
            "agent": "Forge & ReactEngine",
            "outcome": f"Generated {len(codebase_res.get('files_generated', []))} source files. Live Staging: {codebase_res.get('staging_preview_url')}.",
        })

        # -----------------------------------------------------------------
        # STAGE 6: GST Billing, Invoicing & Payments (D01 - Ledger)
        # -----------------------------------------------------------------
        billing_svc = BillingContractService(self.db)
        line_items = [
            {"description": "UI/UX & Mobile-First Component Engineering", "amount": 25000.0},
            {"description": "FastAPI Microservice & Database Integration", "amount": 35000.0},
        ]
        invoice = await billing_svc.create_invoice(
            client_name=business_name,
            project_id=proj.id,
            proposal_id=proposal.id,
            line_items=line_items,
            gst_rate_pct=18.0,
        )
        contract = await billing_svc.create_service_contract(
            client_name=business_name,
            title=f"MSA: Digital Platform for {business_name}",
            total_value_inr=invoice.total_amount,
            project_id=proj.id,
        )
        pipeline_log.append({
            "stage": "Stage 6: Billing & Legal Governance",
            "department": "D01 Operations & Finance",
            "agent": "Ledger & Justiciar",
            "outcome": f"Invoice {invoice.invoice_number} generated (₹{invoice.total_amount:,.2f}) + Contract {contract.contract_number} drafted.",
        })

        # -----------------------------------------------------------------
        # STAGE 7: Marketing & Thought Leadership (D09 - Echo & StoryArc)
        # -----------------------------------------------------------------
        marketing_svc = MarketingService(self.db)
        post = await marketing_svc.generate_thought_leadership_post(
            platform="linkedin",
            topic=f"Autonomous Web Delivery for {business_name}",
            key_insight=f"Accelerated time-to-market for regional retail and manufacturing in {location}.",
        )
        pipeline_log.append({
            "stage": "Stage 7: Marketing & Growth",
            "department": "D09 Marketing & Growth",
            "agent": "Echo & StoryArc",
            "outcome": f"LinkedIn case study post drafted: '{post.title}'.",
        })

        # -----------------------------------------------------------------
        # STAGE 8: Memory Checkpointing (NEXUS Central AI Manager)
        # -----------------------------------------------------------------
        await self.memory.store_memory(
            tier="project",
            namespace=str(proj.id),
            key="autonomous-pipeline-completion",
            content=f"Successfully executed full autonomous delivery lifecycle for {business_name}.",
            metadata_json={"audit_score": audit_res.overall_score, "invoice_total": invoice.total_amount},
            provenance="NEXUS (Chief of Staff)",
        )

        return {
            "status": "success",
            "business_name": business_name,
            "project_id": str(proj.id),
            "lead_id": str(lead.id),
            "audit_score": audit_res.overall_score,
            "staging_preview_url": codebase_res.get("staging_preview_url"),
            "invoice_number": invoice.invoice_number,
            "total_inr": invoice.total_amount,
            "payment_link": invoice.payment_link,
            "contract_number": contract.contract_number,
            "whatsapp_click_to_chat": wa_res.get("click_to_chat_url"),
            "pipeline_log": pipeline_log,
        }
