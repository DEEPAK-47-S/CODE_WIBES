"""Multi-channel communication service for WhatsApp outreach, click-to-chat links, and messaging."""
import urllib.parse
import uuid
from typing import Any, Dict, Optional
import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lead import Lead
from app.services.approval_service import ApprovalService
from app.services.audit_service import AuditService


class CommunicationService:
    """Manages WhatsApp business messaging, Click-to-Chat URLs, and Founder Approval gates."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.approval = ApprovalService(db)
        self.audit = AuditService(db)

    async def draft_whatsapp_outreach(
        self,
        lead_id: uuid.UUID,
        audit_score: Optional[int] = None,
        key_improvement: str = "Modern mobile-responsive web platform & customer booking engine",
    ) -> Dict[str, Any]:
        """Drafts a personalized WhatsApp proposition and pauses for Founder Approval."""
        res = await self.db.execute(select(Lead).where(Lead.id == lead_id))
        lead = res.scalar_one_or_none()
        if not lead:
            raise ValueError(f"Lead {lead_id} not found.")

        if lead.status == "do_not_contact" or lead.consent_status == "opt_out":
            raise PermissionError("BLOCKED: Lead has opted out of communication.")

        phone = lead.phone or ""
        clean_phone = "".join(filter(str.isdigit, phone))
        if clean_phone.startswith("0"):
            clean_phone = clean_phone[1:]
        if len(clean_phone) == 10:
            clean_phone = f"91{clean_phone}"

        score_text = f" (Tech Audit Score: {audit_score}/100)" if audit_score else ""

        message_body = (
            f"Hello Team {lead.business_name},\n\n"
            f"Greetings from CODE WIBES TECHNOLOGIES! 🚀\n\n"
            f"We reviewed your digital footprint in {lead.district or 'your region'}{score_text}. "
            f"We specialize in engineering sub-second web applications with {key_improvement}.\n\n"
            f"Would you like to see a free, live interactive staging demo crafted specifically for {lead.business_name}?\n\n"
            f"Best regards,\n"
            f"DEEPAKUMAR.S (Founder, CODE WIBES)\n"
            f"https://codewibes.com"
        )

        encoded_text = urllib.parse.quote(message_body)
        click_to_chat_url = f"https://wa.me/{clean_phone}?text={encoded_text}" if clean_phone else None

        # Intercept behind Founder Approval
        approval_req = await self.approval.create_request(
            action_type="WHATSAPP_CLIENT_OUTREACH",
            title=f"WhatsApp Proposition: {lead.business_name}",
            description=f"Automated WhatsApp message drafted for {lead.business_name} ({phone}). Awaiting Founder approval.",
            preview_payload={
                "lead_id": str(lead.id),
                "business_name": lead.business_name,
                "phone": phone,
                "clean_phone": clean_phone,
                "message": message_body,
                "click_to_chat_url": click_to_chat_url,
            },
            risk_level="MEDIUM",
        )

        return {
            "status": "awaiting_founder_approval",
            "approval_id": str(approval_req.id),
            "lead_id": str(lead.id),
            "business_name": lead.business_name,
            "message": message_body,
            "click_to_chat_url": click_to_chat_url,
        }

    async def dispatch_approved_whatsapp(self, approval_id: uuid.UUID) -> Dict[str, Any]:
        """Dispatches WhatsApp message via Meta Cloud API if token configured, or returns verified link."""
        from app.models.approval import ApprovalRequest
        res = await self.db.execute(select(ApprovalRequest).where(ApprovalRequest.id == approval_id))
        app_req = res.scalar_one_or_none()
        if not app_req:
            raise ValueError(f"Approval {approval_id} not found.")

        payload = app_req.preview_payload or {}
        comp_settings = await self.audit.get_or_create_settings()

        # If Meta WhatsApp API Token configured
        if comp_settings.whatsapp_api_token and comp_settings.whatsapp_phone_number_id:
            try:
                url = f"https://graph.facebook.com/v19.0/{comp_settings.whatsapp_phone_number_id}/messages"
                headers = {
                    "Authorization": f"Bearer {comp_settings.whatsapp_api_token}",
                    "Content-Type": "application/json",
                }
                data = {
                    "messaging_product": "whatsapp",
                    "to": payload.get("clean_phone"),
                    "type": "text",
                    "text": {"body": payload.get("message")},
                }
                async with httpx.AsyncClient(timeout=10.0) as client:
                    resp = await client.post(url, headers=headers, json=data)
                    return {
                        "status": "sent_via_meta_api",
                        "status_code": resp.status_code,
                        "response": resp.json(),
                    }
            except Exception as e:
                return {"status": "meta_api_failed", "error": str(e), "fallback_link": payload.get("click_to_chat_url")}

        return {
            "status": "approved_for_manual_or_web_dispatch",
            "click_to_chat_url": payload.get("click_to_chat_url"),
            "message": payload.get("message"),
        }
