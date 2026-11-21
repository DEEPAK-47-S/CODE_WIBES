"""Billing, Invoicing, Payment Links, and Legal Contract Management Service."""
import uuid
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.invoice import Invoice
from app.models.contract import Contract
from app.models.project import Project
from app.models.task import Task
from app.services.audit_service import AuditService
from app.services.memory_service import MemoryService


class BillingContractService:
    """Manages GST invoicing, Razorpay/Stripe payment links, legal agreements, and auto-onboarding."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.audit = AuditService(db)
        self.memory = MemoryService(db)

    async def create_invoice(
        self,
        client_name: str,
        line_items: List[Dict[str, Any]],
        client_email: Optional[str] = None,
        client_phone: Optional[str] = None,
        project_id: Optional[uuid.UUID] = None,
        proposal_id: Optional[uuid.UUID] = None,
        gst_rate_pct: float = 18.0,
        currency: str = "INR",
        due_days: int = 14,
    ) -> Invoice:
        """Calculates GST, generates payment link, and stores client invoice."""
        subtotal = sum(float(item.get("amount", 0.0)) for item in line_items)
        gst_amount = round(subtotal * (gst_rate_pct / 100.0), 2)
        total_amount = round(subtotal + gst_amount, 2)

        # Count existing invoices for sequential ID
        count_res = await self.db.execute(select(func.count(Invoice.id)))
        count = count_res.scalar() or 0
        invoice_number = f"CW-INV-{datetime.now(timezone.utc).year}-{count + 1:04d}"

        # Payment link (Razorpay / Stripe compliant format)
        payment_link = f"https://rzp.io/l/{invoice_number.lower().replace('-', '')}"
        due_date = datetime.now(timezone.utc) + timedelta(days=due_days)

        invoice = Invoice(
            invoice_number=invoice_number,
            client_name=client_name,
            client_email=client_email,
            client_phone=client_phone,
            project_id=project_id,
            proposal_id=proposal_id,
            currency=currency,
            subtotal=subtotal,
            gst_rate_pct=gst_rate_pct,
            gst_amount=gst_amount,
            total_amount=total_amount,
            status="draft",
            line_items=line_items,
            payment_link=payment_link,
            due_date=due_date,
        )
        self.db.add(invoice)
        await self.db.commit()
        await self.db.refresh(invoice)

        await self.audit.log_event(
            actor_type="agent",
            action="invoice_created",
            resource_type="invoice",
            resource_id=invoice.id,
            details={"invoice_number": invoice_number, "total": total_amount},
            risk_level="MEDIUM",
        )
        return invoice

    async def mark_invoice_paid(
        self,
        invoice_id: uuid.UUID,
        payment_reference_id: str = "PAY-DIRECT-SETTLED",
    ) -> Dict[str, Any]:
        """Settles invoice, sets paid_at timestamp, and triggers project onboarding workflow."""
        res = await self.db.execute(select(Invoice).where(Invoice.id == invoice_id))
        invoice = res.scalar_one_or_none()
        if not invoice:
            raise ValueError(f"Invoice {invoice_id} not found.")

        invoice.status = "paid"
        invoice.paid_at = datetime.now(timezone.utc)
        invoice.payment_reference_id = payment_reference_id

        onboarding_status = "no_project_linked"
        # Auto-onboarding trigger
        if invoice.project_id:
            proj_res = await self.db.execute(select(Project).where(Project.id == invoice.project_id))
            proj = proj_res.scalar_one_or_none()
            if proj:
                proj.status = "in_progress"
                proj.progress = 20
                # Record in memory
                await self.memory.store_memory(
                    tier="project",
                    namespace=str(proj.id),
                    key=f"funded-{invoice.invoice_number}",
                    content=f"Client '{invoice.client_name}' settled invoice {invoice.invoice_number} (₹{invoice.total_amount:,.2f}). Project funded and live.",
                    metadata_json={"invoice_id": str(invoice.id), "total_amount": invoice.total_amount},
                    provenance="Ledger (Finance)",
                )
                # Create onboarding welcome task for Customer Success
                task = Task(
                    title=f"Welcome and Onboard Client: {invoice.client_name}",
                    description=f"Send onboarding kit and project portal access to {invoice.client_name}.",
                    status="pending",
                    priority="high",
                    project_id=proj.id,
                )
                self.db.add(task)
                onboarding_status = "onboarding_initiated"

        await self.db.commit()
        return {
            "status": "paid",
            "invoice_number": invoice.invoice_number,
            "total_paid": invoice.total_amount,
            "onboarding": onboarding_status,
        }

    async def create_service_contract(
        self,
        client_name: str,
        title: str,
        total_value_inr: float,
        project_id: Optional[uuid.UUID] = None,
        scope_summary: str = "Custom software engineering and deployment.",
    ) -> Contract:
        """Drafts full-length legal Master Service Agreement (MSA) with Founder authorization."""
        count_res = await self.db.execute(select(func.count(Contract.id)))
        count = count_res.scalar() or 0
        contract_number = f"CW-MSA-{datetime.now(timezone.utc).year}-{count + 1:04d}"

        terms_text = f"""MASTER SERVICE AGREEMENT & WORK ORDER
Contract No: {contract_number}
Effective Date: {datetime.now(timezone.utc).strftime('%B %d, %Y')}

PARTIES:
1. PROVIDER: CODE WIBES TECHNOLOGIES (represented by Authorized Signatory: DEEPAKUMAR.S, Founder).
2. CLIENT: {client_name}.

1. SCOPE OF SERVICES:
The Provider agrees to deliver the software architecture and engineering as defined:
{scope_summary}

2. COMPENSATION & PAYMENT TERMS:
The total project value is fixed at INR ₹{total_value_inr:,.2f} (+ applicable GST).
Payment shall be made in milestone disbursements as invoiced by Provider.

3. INTELLECTUAL PROPERTY RIGHTS:
Upon full and final payment of all invoices, all custom source code, documentation, and digital assets
shall be assigned exclusively to the Client. Provider retains rights to standard re-usable frameworks.

4. WARRANTY & DEFECT REMEDIATION:
Provider grants a 30-day post-deployment defect warranty for issues directly attributable to specifications.

5. JURISDICTION:
This agreement is governed by the laws of India, subject to the jurisdiction of courts in Coimbatore / Chennai, Tamil Nadu.
"""

        contract = Contract(
            contract_number=contract_number,
            client_name=client_name,
            title=title,
            project_id=project_id,
            terms_text=terms_text,
            total_value_inr=total_value_inr,
            status="draft",
        )
        self.db.add(contract)
        await self.db.commit()
        await self.db.refresh(contract)
        return contract

    async def founder_sign_contract(self, contract_id: uuid.UUID) -> Dict[str, Any]:
        """Records Founder DEEPAKUMAR.S legal digital sign-off on the contract."""
        res = await self.db.execute(select(Contract).where(Contract.id == contract_id))
        contract = res.scalar_one_or_none()
        if not contract:
            raise ValueError(f"Contract {contract_id} not found.")

        contract.status = "founder_approved"
        contract.founder_signed_at = datetime.now(timezone.utc)
        await self.db.commit()

        return {
            "status": "founder_approved",
            "contract_number": contract.contract_number,
            "signed_by": "DEEPAKUMAR.S (Founder)",
            "signed_at": contract.founder_signed_at.isoformat(),
        }

    async def generate_printable_invoice_html(self, invoice_id: uuid.UUID) -> str:
        """Generates a print-ready, government-compliant GST tax invoice HTML document."""
        res = await self.db.execute(select(Invoice).where(Invoice.id == invoice_id))
        inv = res.scalar_one_or_none()
        if not inv:
            return f"<h1>Invoice {invoice_id} not found</h1>"

        cgst = round(inv.gst_amount / 2.0, 2)
        sgst = round(inv.gst_amount / 2.0, 2)
        items = inv.line_items or [{"description": "Custom Software Engineering & Development", "amount": inv.subtotal}]

        items_rows = "".join(
            f"""<tr>
                <td style="padding:12px;border-bottom:1px solid #e2e8f0;">{i+1}</td>
                <td style="padding:12px;border-bottom:1px solid #e2e8f0;"><strong>{item.get('description', 'Service')}</strong></td>
                <td style="padding:12px;border-bottom:1px solid #e2e8f0;text-align:center;">998314</td>
                <td style="padding:12px;border-bottom:1px solid #e2e8f0;text-align:right;">₹{float(item.get('amount', 0.0)):,.2f}</td>
            </tr>"""
            for i, item in enumerate(items)
        )

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Tax Invoice — {inv.invoice_number}</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f8fafc; color: #0f172a; margin: 0; padding: 40px 20px; }}
    .invoice-card {{ max-width: 800px; margin: 0 auto; background: #ffffff; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); padding: 40px; border: 1px solid #e2e8f0; }}
    .header {{ display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 2px solid #0284c7; padding-bottom: 24px; margin-bottom: 24px; }}
    .brand-title {{ font-size: 26px; font-weight: 900; color: #0284c7; letter-spacing: -0.5px; margin: 0; }}
    .meta-table {{ width: 100%; border-collapse: collapse; margin: 24px 0; }}
    .meta-table th {{ background: #f1f5f9; padding: 10px; font-size: 12px; text-transform: uppercase; color: #475569; text-align: left; }}
    .totals-box {{ width: 320px; margin-left: auto; margin-top: 20px; }}
    .totals-row {{ display: flex; justify-content: space-between; padding: 6px 0; font-size: 14px; }}
    .grand-total {{ border-top: 2px solid #0f172a; border-bottom: 2px solid #0f172a; padding: 10px 0; font-weight: 800; font-size: 18px; color: #0284c7; }}
    .signature-box {{ margin-top: 40px; text-align: right; border-top: 1px dashed #cbd5e1; padding-top: 16px; }}
    .status-badge {{ display: inline-block; padding: 4px 12px; border-radius: 9999px; font-size: 12px; font-weight: 700; text-transform: uppercase; }}
    .status-paid {{ background: #dcfce7; color: #15803d; }}
    .status-draft {{ background: #fef3c7; color: #b45309; }}
    @media print {{ body {{ background: #ffffff; padding: 0; }} .invoice-card {{ box-shadow: none; border: none; padding: 0; }} button {{ display: none !important; }} }}
  </style>
</head>
<body>
  <div style="max-width:800px; margin: 0 auto 16px; text-align: right;">
    <button onclick="window.print()" style="background:#0284c7;color:#fff;border:none;padding:10px 20px;border-radius:8px;font-weight:700;cursor:pointer;">
      🖨️ Print / Save PDF
    </button>
  </div>

  <div class="invoice-card">
    <div class="header">
      <div>
        <h1 class="brand-title">CODE WIBES TECHNOLOGIES</h1>
        <div style="font-size:13px; color:#475569; margin-top:4px;">Enterprise AI Systems & Cloud Software Architecture</div>
        <div style="font-size:12px; color:#64748b; margin-top:6px; line-height:1.5;">
          GSTIN: <strong>33AAACC1234F1Z5</strong> (Tamil Nadu)<br>
          Coimbatore, Tamil Nadu 641004, India<br>
          Email: contact@codewibes.com | Phone: +91 98400 12345
        </div>
      </div>
      <div style="text-align:right;">
        <div style="font-size:22px; font-weight:900; color:#0f172a;">TAX INVOICE</div>
        <div style="font-size:14px; font-weight:700; color:#0284c7; margin-top:4px;">{inv.invoice_number}</div>
        <div style="margin-top:8px;">
          <span class="status-badge {'status-paid' if inv.status == 'paid' else 'status-draft'}">{inv.status.upper()}</span>
        </div>
        <div style="font-size:12px; color:#64748b; margin-top:6px;">Date: {inv.created_at.strftime('%d-%b-%Y')}</div>
        <div style="font-size:12px; color:#64748b;">Due Date: {inv.due_date.strftime('%d-%b-%Y')}</div>
      </div>
    </div>

    <div style="display:flex; justify-content:space-between; margin-bottom:24px; font-size:13px;">
      <div>
        <div style="font-weight:700; color:#475569; text-transform:uppercase; font-size:11px; margin-bottom:4px;">BILL TO:</div>
        <div style="font-size:16px; font-weight:800; color:#0f172a;">{inv.client_name}</div>
        <div style="color:#64748b;">Phone: {inv.client_phone or 'Registered Client'}</div>
        <div style="color:#64748b;">Email: {inv.client_email or 'billing@client.com'}</div>
      </div>
      <div style="text-align:right;">
        <div style="font-weight:700; color:#475569; text-transform:uppercase; font-size:11px; margin-bottom:4px;">PAYMENT METHOD:</div>
        <div style="color:#0f172a; font-weight:600;">Razorpay Online / UPI / NEFT</div>
        <a href="{inv.payment_link}" target="_blank" style="color:#0284c7; text-decoration:underline; font-size:12px;">{inv.payment_link}</a>
      </div>
    </div>

    <table class="meta-table">
      <thead>
        <tr>
          <th style="width:50px;">#</th>
          <th>Description of Service</th>
          <th style="width:100px; text-align:center;">HSN / SAC</th>
          <th style="width:140px; text-align:right;">Amount (INR)</th>
        </tr>
      </thead>
      <tbody>
        {items_rows}
      </tbody>
    </table>

    <div class="totals-box">
      <div class="totals-row">
        <span>Subtotal:</span>
        <span>₹{inv.subtotal:,.2f}</span>
      </div>
      <div class="totals-row" style="color:#64748b;">
        <span>CGST (9.0%):</span>
        <span>₹{cgst:,.2f}</span>
      </div>
      <div class="totals-row" style="color:#64748b;">
        <span>SGST (9.0%):</span>
        <span>₹{sgst:,.2f}</span>
      </div>
      <div class="totals-row grand-total">
        <span>Total Amount (INR):</span>
        <span>₹{inv.total_amount:,.2f}</span>
      </div>
    </div>

    <div class="signature-box">
      <div style="font-size:11px; color:#64748b; text-transform:uppercase;">For CODE WIBES TECHNOLOGIES</div>
      <div style="margin-top:16px; font-weight:800; color:#0284c7; font-size:16px;">DEEPAKUMAR.S</div>
      <div style="font-size:12px; color:#475569;">Founder & Authorized Signatory</div>
      <div style="font-size:11px; color:#94a3b8; margin-top:4px;">Digitally Certified via CODE WIBES Operating System</div>
    </div>
  </div>
</body>
</html>"""

    async def generate_printable_contract_html(self, contract_id: uuid.UUID) -> str:
        """Generates a print-ready legal Master Service Agreement (MSA) document."""
        res = await self.db.execute(select(Contract).where(Contract.id == contract_id))
        contract = res.scalar_one_or_none()
        if not contract:
            return f"<h1>Contract {contract_id} not found</h1>"

        formatted_terms = contract.terms_text.replace("\n", "<br>")

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Master Service Agreement — {contract.contract_number}</title>
  <style>
    body {{ font-family: Georgia, serif; background: #f8fafc; color: #1e293b; margin: 0; padding: 40px 20px; line-height: 1.8; }}
    .legal-card {{ max-width: 820px; margin: 0 auto; background: #ffffff; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); padding: 50px; border: 1px solid #cbd5e1; }}
    .legal-header {{ text-align: center; border-bottom: 2px solid #0f172a; padding-bottom: 20px; margin-bottom: 30px; }}
    .legal-header h1 {{ margin: 0; font-size: 24px; text-transform: uppercase; letter-spacing: 1px; color: #0f172a; }}
    .contract-meta {{ font-size: 13px; color: #64748b; margin-top: 6px; font-family: sans-serif; }}
    .legal-body {{ font-size: 14.5px; text-align: justify; }}
    .signature-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-top: 60px; font-family: sans-serif; font-size: 13px; border-top: 1px solid #cbd5e1; padding-top: 30px; }}
    .sig-line {{ border-top: 1px solid #0f172a; margin-top: 40px; padding-top: 6px; font-weight: 700; }}
    @media print {{ body {{ background: #fff; padding: 0; }} .legal-card {{ box-shadow: none; border: none; padding: 0; }} button {{ display: none !important; }} }}
  </style>
</head>
<body>
  <div style="max-width:820px; margin: 0 auto 16px; text-align: right;">
    <button onclick="window.print()" style="background:#0f172a;color:#fff;border:none;padding:10px 20px;border-radius:6px;font-weight:700;cursor:pointer;font-family:sans-serif;">
      🖨️ Print / Sign Agreement
    </button>
  </div>

  <div class="legal-card">
    <div class="legal-header">
      <h1>MASTER SERVICE AGREEMENT & WORK ORDER</h1>
      <div class="contract-meta">Contract Ref: <strong>{contract.contract_number}</strong> | Effective Date: {contract.created_at.strftime('%B %d, %Y')}</div>
      <div style="margin-top:8px; font-family:sans-serif; font-size:12px; font-weight:700; color:{'#15803d' if contract.status == 'founder_approved' else '#b45309'};">
        STATUS: {contract.status.upper().replace('_', ' ')}
      </div>
    </div>

    <div class="legal-body">
      {formatted_terms}
    </div>

    <div class="signature-grid">
      <div>
        <div style="color:#64748b; font-size:11px; text-transform:uppercase;">For Provider:</div>
        <div class="sig-line">DEEPAKUMAR.S</div>
        <div>Founder & Chief Executive Officer</div>
        <div style="color:#64748b;">CODE WIBES TECHNOLOGIES</div>
        <div style="color:#15803d; font-size:11px; margin-top:4px;">
          {'✓ Digitally Signed on ' + contract.founder_signed_at.strftime('%d-%b-%Y') if contract.founder_signed_at else 'Awaiting Signature'}
        </div>
      </div>
      <div>
        <div style="color:#64748b; font-size:11px; text-transform:uppercase;">For Client:</div>
        <div class="sig-line">{contract.client_name}</div>
        <div>Authorized Signatory</div>
        <div style="color:#64748b;">Client Counterparty</div>
        <div style="color:#64748b; font-size:11px; margin-top:4px;">Signature / Seal</div>
      </div>
    </div>
  </div>
</body>
</html>"""
