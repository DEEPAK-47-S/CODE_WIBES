import React, { useState, useEffect } from 'react';
import { ExternalLink, Download, ShieldCheck, CreditCard, FileText, Send, CheckCircle2, Clock } from 'lucide-react';
import { fetchClientPortalData, submitClientChangeRequest, type ClientPortalData, type Project } from '../api';

export function ClientPortalView({ projects }: { projects: Project[] }) {
  const [selectedProjectId, setSelectedProjectId] = useState<string>(projects[0]?.id || '');
  const [portalData, setPortalData] = useState<ClientPortalData | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  // Change request form state
  const [crTitle, setCrTitle] = useState<string>('');
  const [crDescription, setCrDescription] = useState<string>('');
  const [crPriority, setCrPriority] = useState<string>('medium');
  const [crSubmitting, setCrSubmitting] = useState<boolean>(false);
  const [crSuccessMsg, setCrSuccessMsg] = useState<string | null>(null);

  const loadPortal = async (pId: string) => {
    if (!pId) return;
    setLoading(true);
    try {
      const data = await fetchClientPortalData(pId);
      setPortalData(data);
    } catch {
      console.error('Failed to load client portal data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (projects.length > 0) {
      const idToLoad = selectedProjectId || projects[0].id;
      setSelectedProjectId(idToLoad);
      loadPortal(idToLoad);
    }
  }, [projects]);

  const handleSubmitCR = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedProjectId || !crTitle.trim()) return;
    setCrSubmitting(true);
    setCrSuccessMsg(null);
    try {
      const res = await submitClientChangeRequest(selectedProjectId, {
        title: crTitle,
        description: crDescription,
        priority: crPriority,
      });
      setCrSuccessMsg(res.message || 'Change request submitted successfully to Architecture team.');
      setCrTitle('');
      setCrDescription('');
      loadPortal(selectedProjectId);
    } catch {
      alert('Failed to submit change request.');
    } finally {
      setCrSubmitting(false);
    }
  };

  return (
    <div style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Client Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
            <span style={{ background: '#0284c7', color: 'white', padding: '2px 8px', borderRadius: '4px', fontSize: '11px', fontWeight: 800 }}>
              CLIENT SELF-SERVICE PORTAL
            </span>
            <span style={{ color: '#94a3b8', fontSize: '12px' }}>External Counterparty Experience</span>
          </div>
          <h2 style={{ fontSize: '24px', fontWeight: 800, color: '#f8fafc', margin: 0 }}>
            {portalData?.project.name || 'Client Project Hub'}
          </h2>
        </div>

        {/* Project Selector for Founder preview */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <label style={{ fontSize: '12px', color: '#94a3b8' }}>Preview As Client:</label>
          <select
            value={selectedProjectId}
            onChange={(e) => {
              setSelectedProjectId(e.target.value);
              loadPortal(e.target.value);
            }}
            style={{ background: '#0f172a', border: '1px solid #334155', borderRadius: '8px', padding: '8px 14px', color: 'white', fontSize: '13px', outline: 'none' }}
          >
            {projects.map((p) => (
              <option key={p.id} value={p.id}>{p.name}</option>
            ))}
          </select>
        </div>
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '60px', color: '#94a3b8' }}>Loading Client Portal...</div>
      ) : portalData ? (
        <>
          {/* Top Banner: Status & Certification */}
          <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '14px', padding: '20px', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px' }}>
            <div>
              <div style={{ color: '#94a3b8', fontSize: '11px', fontWeight: 700 }}>PROJECT STATUS</div>
              <div style={{ color: '#38bdf8', fontSize: '18px', fontWeight: 800, marginTop: '4px' }}>
                {portalData.project.status.toUpperCase()}
              </div>
              <div style={{ color: '#64748b', fontSize: '12px', marginTop: '2px' }}>
                Architecture & Engineering by CODE WIBES
              </div>
            </div>

            <div>
              <div style={{ color: '#94a3b8', fontSize: '11px', fontWeight: 700 }}>QA & CYBERSECURITY</div>
              <div style={{ color: '#34d399', fontSize: '16px', fontWeight: 800, marginTop: '4px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <ShieldCheck size={18} color="#34d399" /> {portalData.qa_certification.certification}
              </div>
              <div style={{ color: '#64748b', fontSize: '12px', marginTop: '2px' }}>
                OWASP Compliant • Score: {portalData.qa_certification.overall_score}/100
              </div>
            </div>

            <div>
              <div style={{ color: '#94a3b8', fontSize: '11px', fontWeight: 700 }}>DELIVERABLES</div>
              <div style={{ display: 'flex', gap: '10px', marginTop: '8px' }}>
                <a
                  href={portalData.project.staging_url}
                  target="_blank"
                  rel="noreferrer"
                  style={{ background: '#0284c7', color: 'white', textDecoration: 'none', padding: '6px 12px', borderRadius: '6px', fontSize: '12px', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '4px' }}
                >
                  Live Staging <ExternalLink size={12} />
                </a>
                <a
                  href={`http://127.0.0.1:8000${portalData.project.download_zip_url}`}
                  download
                  style={{ background: '#1e293b', color: '#38bdf8', border: '1px solid #334155', textDecoration: 'none', padding: '6px 12px', borderRadius: '6px', fontSize: '12px', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '4px' }}
                >
                  Codebase <Download size={12} />
                </a>
              </div>
            </div>
          </div>

          {/* Middle Row: Invoices & Legal Contracts */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '20px' }}>
            {/* Invoices */}
            <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '14px', padding: '20px' }}>
              <h3 style={{ fontSize: '16px', fontWeight: 700, color: '#f8fafc', margin: '0 0 16px 0', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <CreditCard size={18} color="#38bdf8" /> GST Tax Invoices
              </h3>

              {portalData.invoices.length === 0 ? (
                <div style={{ color: '#64748b', fontSize: '13px' }}>No active invoices.</div>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                  {portalData.invoices.map((inv) => (
                    <div key={inv.id} style={{ background: '#1e293b', borderRadius: '8px', padding: '12px', border: '1px solid #334155', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <div>
                        <div style={{ fontWeight: 700, color: '#f8fafc', fontSize: '13px' }}>{inv.invoice_number}</div>
                        <div style={{ fontSize: '12px', color: '#94a3b8' }}>Amount: ₹{inv.total_amount.toLocaleString()} (incl. 18% GST)</div>
                        <span style={{ fontSize: '10px', fontWeight: 700, color: inv.status === 'paid' ? '#34d399' : '#fbbf24' }}>
                          {inv.status.toUpperCase()}
                        </span>
                      </div>
                      <div style={{ display: 'flex', gap: '8px' }}>
                        <a
                          href={`http://127.0.0.1:8000${inv.print_url}`}
                          target="_blank"
                          rel="noreferrer"
                          style={{ color: '#38bdf8', fontSize: '11px', textDecoration: 'none', background: 'rgba(56,189,248,0.1)', padding: '5px 8px', borderRadius: '4px' }}
                        >
                          🖨️ View GST Invoice
                        </a>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Contracts */}
            <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '14px', padding: '20px' }}>
              <h3 style={{ fontSize: '16px', fontWeight: 700, color: '#f8fafc', margin: '0 0 16px 0', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <FileText size={18} color="#a78bfa" /> Legal Master Agreements (MSA)
              </h3>

              {portalData.contracts.length === 0 ? (
                <div style={{ color: '#64748b', fontSize: '13px' }}>No signed agreements on file.</div>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                  {portalData.contracts.map((c) => (
                    <div key={c.id} style={{ background: '#1e293b', borderRadius: '8px', padding: '12px', border: '1px solid #334155', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <div>
                        <div style={{ fontWeight: 700, color: '#f8fafc', fontSize: '13px' }}>{c.contract_number}</div>
                        <div style={{ fontSize: '12px', color: '#94a3b8' }}>{c.title}</div>
                        <span style={{ fontSize: '10px', fontWeight: 700, color: c.founder_signed ? '#34d399' : '#60a5fa' }}>
                          {c.founder_signed ? '✓ SIGNED BY DEEPAKUMAR.S' : 'AWAITING COUNTERPARTY'}
                        </span>
                      </div>
                      <a
                        href={`http://127.0.0.1:8000${c.print_url}`}
                        target="_blank"
                        rel="noreferrer"
                        style={{ color: '#a78bfa', fontSize: '11px', textDecoration: 'none', background: 'rgba(167,139,250,0.1)', padding: '5px 8px', borderRadius: '4px' }}
                      >
                        🖨️ View Signed MSA
                      </a>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Bottom Section: Client Change Request Engine */}
          <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '14px', padding: '20px' }}>
            <h3 style={{ fontSize: '16px', fontWeight: 700, color: '#f8fafc', margin: '0 0 4px 0' }}>
              Submit Feature Request or Scope Revision
            </h3>
            <p style={{ color: '#94a3b8', fontSize: '12px', margin: '0 0 16px 0' }}>
              Directly submit new module requests or changes. Our AI Architecture team (D02) will scope the deliverables and submit for Founder sign-off.
            </p>

            {crSuccessMsg && (
              <div style={{ background: 'rgba(34, 197, 94, 0.1)', border: '1px solid #22c55e', color: '#4ade80', padding: '10px 14px', borderRadius: '8px', fontSize: '13px', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <CheckCircle2 size={16} /> {crSuccessMsg}
              </div>
            )}

            <form onSubmit={handleSubmitCR} style={{ display: 'grid', gridTemplateColumns: '2fr 1fr auto', gap: '14px', alignItems: 'flex-start' }}>
              <div>
                <input
                  type="text"
                  required
                  placeholder="Feature Title (e.g. Add Multi-Currency Stripe Checkout)"
                  value={crTitle}
                  onChange={(e) => setCrTitle(e.target.value)}
                  style={{ width: '100%', background: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '10px 14px', color: 'white', fontSize: '13px', outline: 'none', marginBottom: '8px' }}
                />
                <textarea
                  rows={2}
                  placeholder="Detailed specifications, required fields, or user flow..."
                  value={crDescription}
                  onChange={(e) => setCrDescription(e.target.value)}
                  style={{ width: '100%', background: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '10px 14px', color: 'white', fontSize: '13px', outline: 'none', resize: 'vertical' }}
                />
              </div>

              <div>
                <select
                  value={crPriority}
                  onChange={(e) => setCrPriority(e.target.value)}
                  style={{ width: '100%', background: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '10px 14px', color: 'white', fontSize: '13px', outline: 'none' }}
                >
                  <option value="low">Low Priority (Next Iteration)</option>
                  <option value="medium">Medium Priority (Standard Sprint)</option>
                  <option value="high">High Priority (Urgent Scope Addition)</option>
                </select>
              </div>

              <button
                type="submit"
                disabled={crSubmitting}
                style={{ background: '#0284c7', color: 'white', border: 'none', padding: '10px 18px', borderRadius: '8px', fontWeight: 700, fontSize: '13px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px' }}
              >
                <Send size={14} />
                {crSubmitting ? 'Submitting...' : 'Submit Request'}
              </button>
            </form>

            {/* List of Previous Change Requests */}
            {portalData.change_requests.length > 0 && (
              <div style={{ marginTop: '20px', borderTop: '1px solid #1e293b', paddingTop: '16px' }}>
                <h4 style={{ fontSize: '13px', color: '#94a3b8', margin: '0 0 10px 0', textTransform: 'uppercase' }}>
                  Submitted Revisions & Progress
                </h4>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                  {portalData.change_requests.map((cr) => (
                    <div key={cr.id} style={{ background: '#1e293b', padding: '10px 14px', borderRadius: '8px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <div>
                        <div style={{ fontWeight: 600, color: '#f8fafc', fontSize: '13px' }}>{cr.title}</div>
                        <div style={{ color: '#94a3b8', fontSize: '11px' }}>{cr.description}</div>
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <span style={{ fontSize: '11px', color: '#94a3b8', display: 'flex', alignItems: 'center', gap: '4px' }}>
                          <Clock size={12} /> {cr.estimated_hours}h est.
                        </span>
                        <span style={{ background: 'rgba(56,189,248,0.15)', color: '#38bdf8', padding: '2px 8px', borderRadius: '4px', fontSize: '10px', fontWeight: 700 }}>
                          {cr.status.toUpperCase()}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </>
      ) : (
        <div style={{ textAlign: 'center', padding: '40px', color: '#64748b' }}>
          Select or create a project to view the client self-service portal.
        </div>
      )}
    </div>
  );
}
