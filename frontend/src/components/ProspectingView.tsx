import React, { useState } from 'react';
import { Search, CheckCircle2, AlertTriangle, Send } from 'lucide-react';
import { auditProspectWebsite, draftOutreachPitch, type ProspectAuditResult } from '../api';


export function ProspectingView({ onOpenApprovals }: { onOpenApprovals: () => void }) {
  const [targetUrl, setTargetUrl] = useState('');
  const [businessName, setBusinessName] = useState('');
  const [auditing, setAuditing] = useState(false);
  const [auditResult, setAuditResult] = useState<ProspectAuditResult | null>(null);
  const [pitchDrafting, setPitchDrafting] = useState(false);
  const [pitchStatus, setPitchStatus] = useState<string | null>(null);

  const handleRunAudit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!targetUrl.trim() || !businessName.trim()) {
      alert('Please enter both business name and website URL.');
      return;
    }
    setAuditing(true);
    setAuditResult(null);
    setPitchStatus(null);
    try {
      const res = await auditProspectWebsite(targetUrl, businessName);
      setAuditResult(res);
    } catch {
      alert('Failed to audit website. Ensure URL is accessible and backend is running.');
    } finally {
      setAuditing(false);
    }
  };

  const handleGeneratePitch = async () => {
    if (!auditResult) return;
    setPitchDrafting(true);
    try {
      const res = await draftOutreachPitch(auditResult.id);
      setPitchStatus(res.pitch_draft);
    } catch {
      alert('Failed to generate outreach pitch.');
    } finally {
      setPitchDrafting(false);
    }
  };

  return (
    <div style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2 style={{ fontSize: '22px', fontWeight: 700, color: '#f8fafc', margin: 0 }}>
            Client Acquisition & Web Audit Engine
          </h2>
          <p style={{ color: '#94a3b8', fontSize: '13px', margin: '4px 0 0 0' }}>
            Autonomous technical website inspection, SEO heuristics, and Founder-approved cold outreach.
          </p>
        </div>
        <span style={{ background: '#1e293b', border: '1px solid #334155', padding: '6px 14px', borderRadius: '20px', fontSize: '12px', color: '#38bdf8' }}>
          Powered by D02 (Hunter) & D09 (Echo)
        </span>
      </div>

      {/* Audit Input Form */}
      <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '14px', padding: '20px' }}>
        <form onSubmit={handleRunAudit} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr auto', gap: '16px', alignItems: 'flex-end' }}>
          <div>
            <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '6px', fontWeight: 600 }}>
              Prospect Business Name
            </label>
            <input
              type="text"
              placeholder="e.g. Kovai Textile Mills"
              value={businessName}
              onChange={(e) => setBusinessName(e.target.value)}
              style={{ width: '100%', background: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '10px 14px', color: 'white', fontSize: '13px', outline: 'none' }}
            />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '6px', fontWeight: 600 }}>
              Website URL
            </label>
            <input
              type="text"
              placeholder="e.g. kovaitextiles.com"
              value={targetUrl}
              onChange={(e) => setTargetUrl(e.target.value)}
              style={{ width: '100%', background: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '10px 14px', color: 'white', fontSize: '13px', outline: 'none' }}
            />
          </div>
          <button
            type="submit"
            disabled={auditing}
            style={{ background: '#3b82f6', color: 'white', border: 'none', borderRadius: '8px', padding: '10px 20px', fontWeight: 600, fontSize: '13px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px' }}
          >
            <Search size={15} />
            {auditing ? 'Auditing...' : 'Run Technical Audit'}
          </button>
        </form>
      </div>

      {/* Audit Results */}
      {auditResult && (
        <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '14px', padding: '24px', display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h3 style={{ fontSize: '18px', fontWeight: 700, color: '#f8fafc', margin: 0 }}>
              Audit Report: {auditResult.business_name}
            </h3>
            <span style={{ fontSize: '12px', color: '#94a3b8' }}>URL: {auditResult.target_url}</span>
          </div>

          {/* Scores Grid */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px' }}>
            <div style={{ background: '#1e293b', padding: '16px', borderRadius: '10px', textAlign: 'center' }}>
              <div style={{ fontSize: '28px', fontWeight: 800, color: auditResult.overall_score >= 70 ? '#4ade80' : auditResult.overall_score >= 50 ? '#facc15' : '#f87171' }}>
                {auditResult.overall_score}/100
              </div>
              <div style={{ fontSize: '12px', color: '#94a3b8', marginTop: '4px' }}>Overall Digital Score</div>
            </div>
            <div style={{ background: '#1e293b', padding: '16px', borderRadius: '10px', textAlign: 'center' }}>
              <div style={{ fontSize: '28px', fontWeight: 800, color: '#60a5fa' }}>{auditResult.performance_score}/100</div>
              <div style={{ fontSize: '12px', color: '#94a3b8', marginTop: '4px' }}>Performance & TTFB</div>
            </div>
            <div style={{ background: '#1e293b', padding: '16px', borderRadius: '10px', textAlign: 'center' }}>
              <div style={{ fontSize: '28px', fontWeight: 800, color: '#a78bfa' }}>{auditResult.seo_score}/100</div>
              <div style={{ fontSize: '12px', color: '#94a3b8', marginTop: '4px' }}>SEO & Meta Tags</div>
            </div>
            <div style={{ background: '#1e293b', padding: '16px', borderRadius: '10px', textAlign: 'center' }}>
              <div style={{ fontSize: '22px', fontWeight: 700, color: auditResult.mobile_friendly ? '#4ade80' : '#f87171' }}>
                {auditResult.mobile_friendly ? 'Mobile Optimized' : 'Not Responsive'}
              </div>
              <div style={{ fontSize: '12px', color: '#94a3b8', marginTop: '4px' }}>Viewport Heuristic</div>
            </div>
          </div>

          {/* Issues & Solutions Grid */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
            <div style={{ background: '#182032', border: '1px solid #334155', borderRadius: '10px', padding: '16px' }}>
              <h4 style={{ color: '#f87171', fontSize: '14px', margin: '0 0 12px 0', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <AlertTriangle size={15} /> Identified Defects & Deficiencies
              </h4>
              <ul style={{ margin: 0, paddingLeft: '18px', fontSize: '13px', color: '#cbd5e1' }}>
                {auditResult.issues_found.map((iss, idx) => (
                  <li key={idx} style={{ marginBottom: '8px' }}>
                    <strong style={{ color: '#fca5a5' }}>[{iss.severity}]</strong> {iss.issue}
                  </li>
                ))}
              </ul>
            </div>

            <div style={{ background: '#182032', border: '1px solid #334155', borderRadius: '10px', padding: '16px' }}>
              <h4 style={{ color: '#38bdf8', fontSize: '14px', margin: '0 0 12px 0', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <CheckCircle2 size={15} /> Proposed CODE WIBES Modernization
              </h4>
              <ul style={{ margin: 0, paddingLeft: '18px', fontSize: '13px', color: '#cbd5e1' }}>
                {auditResult.proposed_solutions.map((sol, idx) => (
                  <li key={idx} style={{ marginBottom: '8px' }}>
                    <strong style={{ color: '#93c5fd' }}>{sol.category}:</strong> {sol.solution}
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Action Footer */}
          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px', borderTop: '1px solid #1e293b', paddingTop: '16px' }}>
            <button
              onClick={handleGeneratePitch}
              disabled={pitchDrafting}
              style={{ background: '#10b981', color: 'white', border: 'none', borderRadius: '8px', padding: '10px 20px', fontWeight: 600, fontSize: '13px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px' }}
            >
              <Send size={15} />
              {pitchDrafting ? 'Drafting...' : 'Generate Pitch & Submit for Founder Approval'}
            </button>
          </div>

          {/* Pitch Status Banner */}
          {pitchStatus && (
            <div style={{ background: '#064e3b', border: '1px solid #059669', borderRadius: '10px', padding: '16px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                <span style={{ color: '#34d399', fontWeight: 700, fontSize: '13px' }}>
                  ✓ Pitch Drafted & Queued in Founder Approvals!
                </span>
                <button
                  onClick={onOpenApprovals}
                  style={{ background: '#059669', color: 'white', border: 'none', borderRadius: '6px', padding: '6px 12px', fontSize: '12px', cursor: 'pointer', fontWeight: 600 }}
                >
                  Review in Approvals →
                </button>
              </div>
              <pre style={{ background: '#022c22', padding: '12px', borderRadius: '6px', color: '#a7f3d0', fontSize: '12px', whiteSpace: 'pre-wrap', margin: 0 }}>
                {pitchStatus}
              </pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
