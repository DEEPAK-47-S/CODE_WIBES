import React, { useState, useEffect } from 'react';
import { Plus, ExternalLink } from 'lucide-react';
import {
  fetchInvoices,
  createInvoice,
  payInvoice,
  fetchContracts,
  founderSignContract,
  type InvoiceItem,
  type ContractItem,
  type Project,
} from '../api';

export function BillingContractsView({ projects }: { projects: Project[] }) {
  const [subTab, setSubTab] = useState<'invoices' | 'contracts'>('invoices');
  const [invoices, setInvoices] = useState<InvoiceItem[]>([]);
  const [contracts, setContracts] = useState<ContractItem[]>([]);

  // Invoice Form State
  const [clientName, setClientName] = useState('');
  const [amount, setAmount] = useState('45000');
  const [selectedProj, setSelectedProj] = useState('');

  const loadData = async () => {
    try {
      const [invs, cntrs] = await Promise.all([fetchInvoices(), fetchContracts()]);
      setInvoices(invs);
      setContracts(cntrs);
    } catch {
      console.error('Failed to load billing data');
    }
  };


  useEffect(() => {
    loadData();
  }, []);

  const handleCreateInvoice = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!clientName.trim() || !amount) return;
    try {
      await createInvoice({
        client_name: clientName,
        project_id: selectedProj || undefined,
        line_items: [
          { description: 'Full-Stack Software Architecture & Engineering', amount: parseFloat(amount) },
        ],
        gst_rate_pct: 18.0,
      });
      setClientName('');
      loadData();
    } catch {
      alert('Failed to generate invoice.');
    }
  };

  const handlePayInvoice = async (invId: string) => {
    try {
      await payInvoice(invId, 'RZP-DIRECT-CAPTURED');
      loadData();
    } catch {
      alert('Failed to settle invoice.');
    }
  };

  const handleSignContract = async (contractId: string) => {
    try {
      await founderSignContract(contractId);
      loadData();
    } catch {
      alert('Failed to sign contract.');
    }
  };

  return (
    <div style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Header & Sub-Navigation */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2 style={{ fontSize: '22px', fontWeight: 700, color: '#f8fafc', margin: 0 }}>
            Billing, Invoicing & Legal Governance
          </h2>
          <p style={{ color: '#94a3b8', fontSize: '13px', margin: '4px 0 0 0' }}>
            GST-compliant invoices, automated Razorpay payment links, and Founder-signed Master Service Agreements.
          </p>
        </div>
        <div style={{ display: 'flex', gap: '8px', background: '#0f172a', padding: '4px', borderRadius: '10px', border: '1px solid #1e293b' }}>
          <button
            onClick={() => setSubTab('invoices')}
            style={{ background: subTab === 'invoices' ? '#3b82f6' : 'transparent', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '6px', fontSize: '12px', fontWeight: 600, cursor: 'pointer' }}
          >
            Invoices & Payments ({invoices.length})
          </button>
          <button
            onClick={() => setSubTab('contracts')}
            style={{ background: subTab === 'contracts' ? '#3b82f6' : 'transparent', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '6px', fontSize: '12px', fontWeight: 600, cursor: 'pointer' }}
          >
            Contracts & SLA ({contracts.length})
          </button>
        </div>
      </div>

      {subTab === 'invoices' ? (
        <>
          {/* Quick Invoice Creator */}
          <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '14px', padding: '20px' }}>
            <h3 style={{ fontSize: '15px', fontWeight: 700, color: '#f8fafc', margin: '0 0 16px 0' }}>
              Create GST Tax Invoice (18% GST Auto-Calculated)
            </h3>
            <form onSubmit={handleCreateInvoice} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr auto', gap: '16px', alignItems: 'flex-end' }}>
              <div>
                <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '6px', fontWeight: 600 }}>Client Name</label>
                <input
                  type="text"
                  placeholder="e.g. SRM Technologies Ltd"
                  value={clientName}
                  onChange={(e) => setClientName(e.target.value)}
                  style={{ width: '100%', background: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '10px 14px', color: 'white', fontSize: '13px', outline: 'none' }}
                />
              </div>
              <div>
                <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '6px', fontWeight: 600 }}>Subtotal (INR ₹)</label>
                <input
                  type="number"
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                  style={{ width: '100%', background: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '10px 14px', color: 'white', fontSize: '13px', outline: 'none' }}
                />
              </div>
              <div>
                <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '6px', fontWeight: 600 }}>Attach Project (Optional)</label>
                <select
                  value={selectedProj}
                  onChange={(e) => setSelectedProj(e.target.value)}
                  style={{ width: '100%', background: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '10px 14px', color: 'white', fontSize: '13px', outline: 'none' }}
                >
                  <option value="">Direct Client Billing</option>
                  {projects.map((p) => (
                    <option key={p.id} value={p.id}>{p.name}</option>
                  ))}
                </select>
              </div>
              <button
                type="submit"
                style={{ background: '#10b981', color: 'white', border: 'none', borderRadius: '8px', padding: '10px 20px', fontWeight: 600, fontSize: '13px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px' }}
              >
                <Plus size={16} /> Generate Invoice
              </button>
            </form>
          </div>

          {/* Invoices List */}
          <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '14px', padding: '20px' }}>
            <h3 style={{ fontSize: '16px', fontWeight: 700, color: '#f8fafc', margin: '0 0 16px 0' }}>
              Historical Invoices & Settlement Log
            </h3>
            {invoices.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '40px', color: '#64748b', fontSize: '14px' }}>
                No invoices generated yet. Create your first client invoice above.
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {invoices.map((inv) => (
                  <div key={inv.id} style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '10px', padding: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '4px' }}>
                        <span style={{ fontWeight: 700, color: '#60a5fa', fontSize: '14px' }}>{inv.invoice_number}</span>
                        <span style={{ fontSize: '13px', color: '#f8fafc', fontWeight: 600 }}>{inv.client_name}</span>
                        <span style={{ background: inv.status === 'paid' ? '#065f46' : '#78350f', color: inv.status === 'paid' ? '#34d399' : '#fcd34d', fontSize: '11px', fontWeight: 700, padding: '2px 8px', borderRadius: '6px' }}>
                          {inv.status.toUpperCase()}
                        </span>
                      </div>
                      <div style={{ fontSize: '12px', color: '#94a3b8' }}>
                        Subtotal: ₹{inv.subtotal.toLocaleString()} + 18% GST (₹{inv.gst_amount.toLocaleString()}) = <strong>₹{inv.total_amount.toLocaleString()}</strong>
                      </div>
                    </div>
                    <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
                      <a
                        href={`http://127.0.0.1:8000/api/v1/billing/invoices/${inv.id}/print`}
                        target="_blank"
                        rel="noreferrer"
                        style={{ color: '#34d399', fontSize: '12px', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '4px', background: 'rgba(52, 211, 153, 0.1)', padding: '5px 10px', borderRadius: '6px', border: '1px solid rgba(52, 211, 153, 0.25)' }}
                      >
                        🖨️ Print GST Invoice
                      </a>
                      {inv.payment_link && (
                        <a
                          href={inv.payment_link}
                          target="_blank"
                          rel="noreferrer"
                          style={{ color: '#38bdf8', fontSize: '12px', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '4px' }}
                        >
                          Checkout Link <ExternalLink size={12} />
                        </a>
                      )}
                      {inv.status !== 'paid' && (
                        <button
                          onClick={() => handlePayInvoice(inv.id)}
                          style={{ background: '#059669', color: 'white', border: 'none', borderRadius: '6px', padding: '6px 12px', fontSize: '12px', fontWeight: 600, cursor: 'pointer' }}
                        >
                          Simulate Settle & Onboard
                        </button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </>
      ) : (
        /* Contracts View */
        <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '14px', padding: '20px' }}>
          <h3 style={{ fontSize: '16px', fontWeight: 700, color: '#f8fafc', margin: '0 0 16px 0' }}>
            Master Service Agreements (MSA)
          </h3>
          {contracts.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '40px', color: '#64748b', fontSize: '14px' }}>
              No contracts generated yet.
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              {contracts.map((c) => (
                <div key={c.id} style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '10px', padding: '16px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                    <div>
                      <span style={{ color: '#a78bfa', fontWeight: 700, fontSize: '14px' }}>{c.contract_number}</span>
                      <span style={{ color: '#f8fafc', fontWeight: 600, fontSize: '14px', marginLeft: '12px' }}>{c.title}</span>
                    </div>
                    <span style={{ background: c.status === 'founder_approved' ? '#065f46' : '#1e3a8a', color: 'white', fontSize: '11px', fontWeight: 700, padding: '3px 10px', borderRadius: '6px' }}>
                      {c.status.toUpperCase()}
                    </span>
                  </div>
                  <pre style={{ background: '#090d16', padding: '12px', borderRadius: '6px', color: '#94a3b8', fontSize: '11px', maxHeight: '120px', overflowY: 'auto', whiteSpace: 'pre-wrap' }}>
                    {c.terms_text}
                  </pre>
                  <div style={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'center', gap: '10px', marginTop: '10px' }}>
                    <a
                      href={`http://127.0.0.1:8000/api/v1/billing/contracts/${c.id}/print`}
                      target="_blank"
                      rel="noreferrer"
                      style={{ color: '#a78bfa', fontSize: '12px', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '4px', background: 'rgba(167, 139, 250, 0.1)', padding: '6px 12px', borderRadius: '6px', border: '1px solid rgba(167, 139, 250, 0.25)' }}
                    >
                      🖨️ Print Agreement
                    </a>
                    {c.status !== 'founder_approved' && (
                      <button
                        onClick={() => handleSignContract(c.id)}
                        style={{ background: '#2563eb', color: 'white', border: 'none', borderRadius: '6px', padding: '6px 14px', fontSize: '12px', fontWeight: 600, cursor: 'pointer' }}
                      >
                        Founder Digital Sign-Off (DEEPAKUMAR.S)
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
