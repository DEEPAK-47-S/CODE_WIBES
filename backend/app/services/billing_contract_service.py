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
