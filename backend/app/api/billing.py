"""API v1 routes for Billing, Invoicing, Payments, and Legal Contracts."""
import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.invoice import Invoice
from app.models.contract import Contract
from app.services.billing_contract_service import BillingContractService

router = APIRouter(prefix="/billing", tags=["billing"])


class InvoiceCreateRequest(BaseModel):
    client_name: str
    client_email: Optional[str] = None
    client_phone: Optional[str] = None
    project_id: Optional[str] = None
    proposal_id: Optional[str] = None
    line_items: List[Dict[str, Any]]
    gst_rate_pct: float = 18.0
    currency: str = "INR"


class InvoicePayRequest(BaseModel):
    payment_reference_id: str = "PAY-DIRECT-ONLINE"


class ContractCreateRequest(BaseModel):
    client_name: str
    title: str
    total_value_inr: float
    project_id: Optional[str] = None
    scope_summary: str = "Custom software engineering and deployment."


@router.get("/invoices")
async def list_invoices(db: AsyncSession = Depends(get_db)):
    """List all client invoices."""
    res = await db.execute(select(Invoice).order_by(Invoice.created_at.desc()))
    invoices = res.scalars().all()
    return [
        {
            "id": str(inv.id),
            "invoice_number": inv.invoice_number,
            "client_name": inv.client_name,
            "total_amount": inv.total_amount,
            "subtotal": inv.subtotal,
            "gst_amount": inv.gst_amount,
            "status": inv.status,
            "payment_link": inv.payment_link,
            "due_date": inv.due_date.isoformat() if inv.due_date else None,
            "paid_at": inv.paid_at.isoformat() if inv.paid_at else None,
            "created_at": inv.created_at.isoformat(),
        }
        for inv in invoices
    ]


@router.post("/invoices")
async def create_invoice(req: InvoiceCreateRequest, db: AsyncSession = Depends(get_db)):
    """Creates a new GST invoice with payment link."""
    service = BillingContractService(db)
    proj_uuid = uuid.UUID(req.project_id) if req.project_id else None
    prop_uuid = uuid.UUID(req.proposal_id) if req.proposal_id else None

    invoice = await service.create_invoice(
        client_name=req.client_name,
        client_email=req.client_email,
        client_phone=req.client_phone,
        project_id=proj_uuid,
        proposal_id=prop_uuid,
        line_items=req.line_items,
        gst_rate_pct=req.gst_rate_pct,
        currency=req.currency,
    )
    return {
        "id": str(invoice.id),
        "invoice_number": invoice.invoice_number,
        "total_amount": invoice.total_amount,
        "payment_link": invoice.payment_link,
        "status": invoice.status,
    }


@router.post("/invoices/{invoice_id}/pay")
async def pay_invoice(invoice_id: str, req: InvoicePayRequest, db: AsyncSession = Depends(get_db)):
    """Marks invoice as paid and triggers auto-onboarding workflow."""
    service = BillingContractService(db)
    try:
        inv_uuid = uuid.UUID(invoice_id)
        return await service.mark_invoice_paid(inv_uuid, req.payment_reference_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/contracts")
async def list_contracts(db: AsyncSession = Depends(get_db)):
    """List legal agreements and contracts."""
    res = await db.execute(select(Contract).order_by(Contract.created_at.desc()))
    contracts = res.scalars().all()
    return [
        {
            "id": str(c.id),
            "contract_number": c.contract_number,
            "client_name": c.client_name,
            "title": c.title,
            "total_value_inr": c.total_value_inr,
            "status": c.status,
            "terms_text": c.terms_text,
            "founder_signed_at": c.founder_signed_at.isoformat() if c.founder_signed_at else None,
            "created_at": c.created_at.isoformat(),
        }
        for c in contracts
    ]


@router.post("/contracts")
async def create_contract(req: ContractCreateRequest, db: AsyncSession = Depends(get_db)):
    """Drafts a legal Master Service Agreement."""
    service = BillingContractService(db)
    proj_uuid = uuid.UUID(req.project_id) if req.project_id else None
    contract = await service.create_service_contract(
        client_name=req.client_name,
        title=req.title,
        total_value_inr=req.total_value_inr,
        project_id=proj_uuid,
        scope_summary=req.scope_summary,
    )
    return {
        "id": str(contract.id),
        "contract_number": contract.contract_number,
        "status": contract.status,
        "terms_text": contract.terms_text,
    }


@router.post("/contracts/{contract_id}/sign")
async def sign_contract_by_founder(contract_id: str, db: AsyncSession = Depends(get_db)):
    """Founder DEEPAKUMAR.S signs the contract."""
    service = BillingContractService(db)
    try:
        c_uuid = uuid.UUID(contract_id)
        return await service.founder_sign_contract(c_uuid)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
