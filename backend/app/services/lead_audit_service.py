"""Lead Audit Service — Autonomous website auditing, score generation, and outreach pitches."""
import re
import time
import uuid
from typing import Any, Dict, List, Optional
import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lead import Lead
from app.models.prospect_audit import ProspectAudit
from app.services.approval_service import ApprovalService
from app.services.audit_service import AuditService


class LeadAuditService:
    """Performs deep technical audits on prospect websites and drafts Founder-approved pitches."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.approval = ApprovalService(db)
        self.audit = AuditService(db)

    async def audit_website(
        self,
        target_url: str,
        business_name: str,
        lead_id: Optional[uuid.UUID] = None,
    ) -> ProspectAudit:
        """Inspects target URL, evaluates SEO/performance heuristics, and creates ProspectAudit."""
        normalized_url = target_url.strip()
        if not normalized_url.startswith(("http://", "https://")):
            normalized_url = f"https://{normalized_url}"

        issues: List[Dict[str, Any]] = []
        solutions: List[Dict[str, Any]] = []
        ssl_active = normalized_url.startswith("https://")
        mobile_friendly = False
        perf_score = 70
        seo_score = 65

        start_time = time.time()
        try:
            async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
                resp = await client.get(normalized_url)
                latency_ms = int((time.time() - start_time) * 1000)
                html = resp.text.lower()
                status_code = resp.status_code

                if status_code != 200:
                    issues.append({"severity": "HIGH", "issue": f"Website returned HTTP status {status_code}"})
                    perf_score -= 30

                # Latency check
                if latency_ms > 1500:
                    issues.append({"severity": "MEDIUM", "issue": f"Slow server TTFB latency ({latency_ms}ms)"})
                    perf_score -= 20
                else:
                    perf_score += 15

                # Viewport check
                if 'name="viewport"' in html or "name='viewport'" in html:
                    mobile_friendly = True
                else:
                    issues.append({"severity": "HIGH", "issue": "Missing mobile responsive viewport meta tag"})
                    perf_score -= 25

                # SEO checks
                if "<title>" not in html:
                    issues.append({"severity": "HIGH", "issue": "Missing HTML <title> tag"})
                    seo_score -= 25
                if 'name="description"' not in html and "name='description'" not in html:
                    issues.append({"severity": "MEDIUM", "issue": "Missing meta description for search engine ranking"})
                    seo_score -= 20
                if "<h1>" not in html:
                    issues.append({"severity": "LOW", "issue": "Missing primary <h1> header hierarchy"})
                    seo_score -= 10
                if 'property="og:' not in html:
                    issues.append({"severity": "LOW", "issue": "Missing Open Graph social preview meta tags"})
                    seo_score -= 10

        except Exception as e:
            issues.append({"severity": "CRITICAL", "issue": f"Connection unreachable or timed out: {type(e).__name__}"})
            perf_score = 30
            seo_score = 30

        # Bound scores
        perf_score = max(10, min(100, perf_score))
        seo_score = max(10, min(100, seo_score))
        overall_score = int((perf_score * 0.5) + (seo_score * 0.5))

        # Generate Solutions
        solutions.append({
            "category": "Architecture",
            "solution": "Modern React + Vite + Tailwind frontend architecture with sub-second page loads.",
        })
        solutions.append({
            "category": "Mobile & UX",
            "solution": "100% fluid mobile-first responsive layout with touch-friendly navigation.",
        })
        solutions.append({
            "category": "Conversion & SEO",
            "solution": "Structured JSON-LD schema, dynamic meta tags, and WhatsApp click-to-chat conversion button.",
        })

        report_html = f"""
        <div style="font-family: system-ui; max-width: 800px; padding: 24px; background: #0f172a; color: #f8fafc; border-radius: 12px;">
            <h2 style="color: #38bdf8; margin-top: 0;">Audit Report: {business_name}</h2>
            <p style="color: #94a3b8;">Target URL: <a href="{normalized_url}" style="color: #60a5fa;">{normalized_url}</a></p>
            <div style="display: flex; gap: 16px; margin: 20px 0;">
                <div style="background: #1e293b; padding: 16px; border-radius: 8px; flex: 1; text-align: center;">
                    <div style="font-size: 28px; font-weight: bold; color: {'#4ade80' if overall_score >= 70 else '#facc15' if overall_score >= 50 else '#f87171'};">{overall_score}/100</div>
                    <div style="font-size: 13px; color: #94a3b8;">Overall Score</div>
                </div>
                <div style="background: #1e293b; padding: 16px; border-radius: 8px; flex: 1; text-align: center;">
                    <div style="font-size: 28px; font-weight: bold; color: #60a5fa;">{perf_score}/100</div>
                    <div style="font-size: 13px; color: #94a3b8;">Performance</div>
                </div>
                <div style="background: #1e293b; padding: 16px; border-radius: 8px; flex: 1; text-align: center;">
                    <div style="font-size: 28px; font-weight: bold; color: #a78bfa;">{seo_score}/100</div>
                    <div style="font-size: 13px; color: #94a3b8;">SEO & Discovery</div>
                </div>
            </div>
            <h3 style="color: #cbd5e1; border-bottom: 1px solid #334155; padding-bottom: 8px;">Key Technical Issues</h3>
            <ul>
                {"".join([f"<li style='color: #f87171; margin-bottom: 6px;'><strong>[{i['severity']}]</strong> {i['issue']}</li>" for i in issues]) if issues else "<li style='color: #4ade80;'>No critical technical defects detected.</li>"}
            </ul>
            <h3 style="color: #cbd5e1; border-bottom: 1px solid #334155; padding-bottom: 8px; margin-top: 24px;">Recommended CODE WIBES Solutions</h3>
            <ul>
                {"".join([f"<li style='color: #38bdf8; margin-bottom: 6px;'><strong>{s['category']}:</strong> {s['solution']}</li>" for s in solutions])}
            </ul>
        </div>
        """

        audit = ProspectAudit(
            lead_id=lead_id,
            target_url=normalized_url,
            business_name=business_name,
            overall_score=overall_score,
            performance_score=perf_score,
            seo_score=seo_score,
            mobile_friendly=mobile_friendly,
            ssl_active=ssl_active,
            issues_found=issues,
            proposed_solutions=solutions,
            audit_report_html=report_html,
        )
        self.db.add(audit)
        await self.db.commit()
        await self.db.refresh(audit)

        await self.audit.log_event(
            actor_type="agent",
            action="website_audit_completed",
            resource_type="prospect_audit",
            resource_id=audit.id,
            details={"url": normalized_url, "score": overall_score},
            risk_level="LOW",
        )
        return audit

    async def generate_outreach_pitch(self, audit_id: uuid.UUID) -> Dict[str, Any]:
        """Drafts personalized outreach pitch and intercepts behind Founder Approval."""
        res = await self.db.execute(select(ProspectAudit).where(ProspectAudit.id == audit_id))
        audit_record = res.scalar_one_or_none()
        if not audit_record:
            raise ValueError(f"Audit record {audit_id} not found.")

        issue_bullet = audit_record.issues_found[0]["issue"] if audit_record.issues_found else "legacy tech stack"

        pitch = (
            f"Subject: Modernizing {audit_record.business_name}'s web presence — Speed & SEO audit\n\n"
            f"Dear Team {audit_record.business_name},\n\n"
            f"We recently analyzed your digital presence at {audit_record.target_url}. "
            f"Our technical audit scored your web platform at {audit_record.overall_score}/100, "
            f"identifying key optimization opportunities including: {issue_bullet}.\n\n"
            f"At CODE WIBES TECHNOLOGIES, we build ultra-fast, high-converting digital web solutions "
            f"with sub-second load times, mobile-first design, and seamless customer capture.\n\n"
            f"Would you be open to a 5-minute review of our full interactive audit report?\n\n"
            f"Best regards,\n"
            f"DEEPAKUMAR.S & The CODE WIBES Engineering Team\n"
            f"https://codewibes.com"
        )

        audit_record.outreach_pitch_draft = pitch
        await self.db.flush()

        # Intercept behind Founder Approval
        approval_req = await self.approval.create_request(
            action_type="OUTBOUND_CLIENT_PROPOSAL",
            title=f"Send Technical Audit Outreach: {audit_record.business_name}",
            description=f"Automated pitch drafted for {audit_record.target_url}. Awaiting Founder approval before sending.",
            preview_payload={
                "audit_id": str(audit_record.id),
                "business_name": audit_record.business_name,
                "url": audit_record.target_url,
                "pitch": pitch,
            },
            risk_level="MEDIUM",
        )
        await self.db.commit()

        return {
            "audit_id": str(audit_record.id),
            "approval_id": str(approval_req.id),
            "status": "awaiting_founder_approval",
            "pitch_draft": pitch,
        }
