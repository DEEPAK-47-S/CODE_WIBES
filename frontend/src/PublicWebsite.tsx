import React, { useState } from 'react';
import {
  Code,
  ShieldCheck,
  Cpu,
  Layers,
  ArrowRight,
  CheckCircle,
  ExternalLink,
  Sparkles,
} from 'lucide-react';
import { createLead } from './api';

export const PublicWebsite: React.FC<{ onOpenDashboard: () => void }> = ({ onOpenDashboard }) => {
  const [quoteForm, setQuoteForm] = useState({
    name: '',
    company: '',
    email: '',
    phone: '',
    service: 'Full-Stack Web Development',
    message: '',
  });
  const [submitted, setSubmitted] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const handleSubmitQuote = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!quoteForm.company || !quoteForm.email) return;

    setSubmitting(true);
    try {
      await createLead({
        company_name: quoteForm.company,
        contact_name: quoteForm.name,
        contact_email: quoteForm.email,
        industry: quoteForm.service,
        estimated_value: 50000,
        source: 'Public Website Contact Form',
        notes: `Phone: ${quoteForm.phone} | Requirements: ${quoteForm.message}`,
      });
      setSubmitted(true);
    } catch (err) {
      console.error('Failed to submit quote:', err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div style={{ backgroundColor: '#101827', color: '#F3F4F6', minHeight: '100vh', fontFamily: 'system-ui, sans-serif' }}>
      {/* Top Navbar */}
      <header style={{ borderBottom: '1px solid rgba(255,255,255,0.08)', position: 'sticky', top: 0, zIndex: 50, backdropFilter: 'blur(12px)', backgroundColor: 'rgba(16, 24, 39, 0.9)' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '16px 24px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{ background: 'linear-gradient(135deg, #2563EB, #60A5FA)', padding: '8px', borderRadius: '8px' }}>
              <Code size={22} color="#FFFFFF" />
            </div>
            <div>
              <span style={{ fontSize: '18px', fontWeight: 800, letterSpacing: '0.5px', color: '#FFFFFF' }}>CODE WIBES</span>
              <span style={{ fontSize: '11px', display: 'block', color: '#60A5FA', fontWeight: 600 }}>TECHNOLOGIES</span>
            </div>
          </div>

          <nav style={{ display: 'flex', gap: '24px', alignItems: 'center', fontSize: '14px', fontWeight: 500 }}>
            <a href="#services" style={{ color: '#C0C7D1', textDecoration: 'none' }}>Services</a>
            <a href="#about" style={{ color: '#C0C7D1', textDecoration: 'none' }}>About</a>
            <a href="#portfolio" style={{ color: '#C0C7D1', textDecoration: 'none' }}>Portfolio</a>
            <a href="#process" style={{ color: '#C0C7D1', textDecoration: 'none' }}>Our Process</a>
            <a href="#quote" style={{ color: '#60A5FA', textDecoration: 'none', fontWeight: 600 }}>Get a Quote</a>
            <button
              onClick={onOpenDashboard}
              style={{
                backgroundColor: '#2563EB',
                color: '#FFFFFF',
                border: 'none',
                padding: '8px 16px',
                borderRadius: '6px',
                cursor: 'pointer',
                fontWeight: 600,
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
              }}
            >
              Company HQ <ExternalLink size={14} />
            </button>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section style={{ padding: '80px 24px', textAlign: 'center', background: 'radial-gradient(ellipse at top, rgba(37,99,235,0.18) 0%, rgba(16,24,39,0) 70%)' }}>
        <div style={{ maxWidth: '900px', margin: '0 auto' }}>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', background: 'rgba(37,99,235,0.15)', border: '1px solid rgba(37,99,235,0.4)', borderRadius: '9999px', padding: '6px 16px', marginBottom: '24px' }}>
            <Sparkles size={16} color="#60A5FA" />
            <span style={{ fontSize: '13px', color: '#93C5FD', fontWeight: 600 }}>Coimbatore & Global Software Solutions</span>
          </div>

          <h1 style={{ fontSize: '52px', fontWeight: 800, lineHeight: 1.15, marginBottom: '20px', color: '#FFFFFF', letterSpacing: '-0.5px' }}>
            Turning Ideas Into <span style={{ color: '#60A5FA', background: 'linear-gradient(90deg, #60A5FA, #93C5FD)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>Digital Solutions</span>.
          </h1>

          <p style={{ fontSize: '18px', color: '#9CA3AF', lineHeight: 1.6, maxWidth: '720px', margin: '0 auto 36px' }}>
            CODE WIBES TECHNOLOGIES builds production-ready, custom software architectures, enterprise web applications, and digital systems orchestrated by autonomous AI departments.
          </p>

          <div style={{ display: 'flex', gap: '16px', justifyContent: 'center' }}>
            <a
              href="#quote"
              style={{
                backgroundColor: '#2563EB',
                color: '#FFFFFF',
                padding: '14px 28px',
                borderRadius: '8px',
                fontWeight: 700,
                textDecoration: 'none',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '8px',
                boxShadow: '0 4px 14px rgba(37,99,235,0.4)',
              }}
            >
              Start Your Project <ArrowRight size={18} />
            </a>
            <a
              href="#services"
              style={{
                backgroundColor: 'rgba(255,255,255,0.06)',
                color: '#F3F4F6',
                padding: '14px 28px',
                borderRadius: '8px',
                fontWeight: 600,
                textDecoration: 'none',
                border: '1px solid rgba(255,255,255,0.12)',
              }}
            >
              Explore Services
            </a>
          </div>
        </div>
      </section>

      {/* Services Grid */}
      <section id="services" style={{ padding: '80px 24px', maxWidth: '1200px', margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '56px' }}>
          <h2 style={{ fontSize: '32px', fontWeight: 800, color: '#FFFFFF', marginBottom: '12px' }}>Our Core Services</h2>
          <p style={{ color: '#9CA3AF', fontSize: '16px' }}>Engineered with precision for growth-focused businesses.</p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '24px' }}>
          {[
            {
              icon: <Code size={26} color="#60A5FA" />,
              title: 'Full-Stack Web Development',
              desc: 'Robust, fast, responsive web applications built using React 19, TypeScript, Python FastAPI, and PostgreSQL.',
            },
            {
              icon: <Layers size={26} color="#60A5FA" />,
              title: 'UI/UX Design Systems',
              desc: 'Dark-mode aesthetic architectures, accessible typography, conversion-focused wireframes, and responsive design systems.',
            },
            {
              icon: <Cpu size={26} color="#60A5FA" />,
              title: 'AI & Workflow Automation',
              desc: 'Autonomous agent pipelines, CRM lead enrichment, smart data extraction, and intelligent customer discovery.',
            },
            {
              icon: <ShieldCheck size={26} color="#60A5FA" />,
              title: 'Security & QA Auditing',
              desc: 'OWASP Top 10 penetration auditing, automated regression suites, contract testing, and zero-defect delivery.',
            },
          ].map((s, idx) => (
            <div
              key={idx}
              style={{
                backgroundColor: '#1E293B',
                padding: '32px',
                borderRadius: '12px',
                border: '1px solid rgba(255,255,255,0.06)',
                transition: 'transform 0.2s ease',
              }}
            >
              <div style={{ marginBottom: '16px' }}>{s.icon}</div>
              <h3 style={{ fontSize: '20px', fontWeight: 700, color: '#FFFFFF', marginBottom: '10px' }}>{s.title}</h3>
              <p style={{ color: '#9CA3AF', fontSize: '14px', lineHeight: 1.6 }}>{s.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Our Process Section */}
      <section id="process" style={{ padding: '80px 24px', backgroundColor: '#0B1120' }}>
        <div style={{ maxWidth: '1100px', margin: '0 auto', textAlign: 'center' }}>
          <h2 style={{ fontSize: '32px', fontWeight: 800, color: '#FFFFFF', marginBottom: '48px' }}>The CODE WIBES Process</h2>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '20px', textAlign: 'left' }}>
            {[
              { step: '01', title: 'Discovery & Brief', desc: 'Structured customer requirement analysis and goal identification.' },
              { step: '02', title: 'Estimation & Approval', desc: 'Founder-approved transparent milestone budget and acceptance criteria.' },
              { step: '03', title: 'Isolated Workspace', desc: 'Dedicated engineering factory workspace on isolated Git feature branch.' },
              { step: '04', title: 'QA & Staging', desc: 'Rigorous regression testing and live staging preview URL.' },
            ].map((p, idx) => (
              <div key={idx} style={{ backgroundColor: '#1E293B', padding: '24px', borderRadius: '10px', border: '1px solid rgba(255,255,255,0.06)' }}>
                <span style={{ fontSize: '28px', fontWeight: 900, color: '#2563EB', display: 'block', marginBottom: '8px' }}>{p.step}</span>
                <h4 style={{ fontSize: '17px', fontWeight: 700, color: '#FFFFFF', marginBottom: '6px' }}>{p.title}</h4>
                <p style={{ color: '#9CA3AF', fontSize: '13px', lineHeight: 1.5 }}>{p.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Get a Quote Section */}
      <section id="quote" style={{ padding: '80px 24px', maxWidth: '800px', margin: '0 auto' }}>
        <div style={{ backgroundColor: '#1E293B', padding: '40px', borderRadius: '16px', border: '1px solid rgba(37,99,235,0.3)', boxShadow: '0 8px 32px rgba(0,0,0,0.4)' }}>
          <h2 style={{ fontSize: '28px', fontWeight: 800, color: '#FFFFFF', marginBottom: '8px', textAlign: 'center' }}>Request a Quotation</h2>
          <p style={{ color: '#9CA3AF', fontSize: '15px', textAlign: 'center', marginBottom: '32px' }}>
            Fill out your project details. Our solution architecture team will compile a verified requirement proposal.
          </p>

          {submitted ? (
            <div style={{ textAlign: 'center', padding: '32px', backgroundColor: 'rgba(16, 185, 129, 0.1)', borderRadius: '12px', border: '1px solid #10B981' }}>
              <CheckCircle size={40} color="#10B981" style={{ margin: '0 auto 12px' }} />
              <h3 style={{ color: '#10B981', fontSize: '20px', fontWeight: 700, marginBottom: '6px' }}>Inquiry Received!</h3>
              <p style={{ color: '#D1FAE5', fontSize: '14px' }}>
                Thank you! Your requirements have been logged into the CODE WIBES Lead Intelligence system.
              </p>
            </div>
          ) : (
            <form onSubmit={handleSubmitQuote} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
                <div>
                  <label style={{ display: 'block', fontSize: '13px', color: '#C0C7D1', marginBottom: '6px', fontWeight: 600 }}>Your Name</label>
                  <input
                    type="text"
                    required
                    value={quoteForm.name}
                    onChange={(e) => setQuoteForm({ ...quoteForm, name: e.target.value })}
                    style={{ width: '100%', padding: '10px 12px', backgroundColor: '#0F172A', border: '1px solid #334155', borderRadius: '6px', color: '#FFFFFF', boxSizing: 'border-box' }}
                    placeholder="e.g. Ramesh Kumar"
                  />
                </div>
                <div>
                  <label style={{ display: 'block', fontSize: '13px', color: '#C0C7D1', marginBottom: '6px', fontWeight: 600 }}>Company Name *</label>
                  <input
                    type="text"
                    required
                    value={quoteForm.company}
                    onChange={(e) => setQuoteForm({ ...quoteForm, company: e.target.value })}
                    style={{ width: '100%', padding: '10px 12px', backgroundColor: '#0F172A', border: '1px solid #334155', borderRadius: '6px', color: '#FFFFFF', boxSizing: 'border-box' }}
                    placeholder="e.g. Apex Textiles"
                  />
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
                <div>
                  <label style={{ display: 'block', fontSize: '13px', color: '#C0C7D1', marginBottom: '6px', fontWeight: 600 }}>Business Email *</label>
                  <input
                    type="email"
                    required
                    value={quoteForm.email}
                    onChange={(e) => setQuoteForm({ ...quoteForm, email: e.target.value })}
                    style={{ width: '100%', padding: '10px 12px', backgroundColor: '#0F172A', border: '1px solid #334155', borderRadius: '6px', color: '#FFFFFF', boxSizing: 'border-box' }}
                    placeholder="contact@company.com"
                  />
                </div>
                <div>
                  <label style={{ display: 'block', fontSize: '13px', color: '#C0C7D1', marginBottom: '6px', fontWeight: 600 }}>Phone Number</label>
                  <input
                    type="tel"
                    value={quoteForm.phone}
                    onChange={(e) => setQuoteForm({ ...quoteForm, phone: e.target.value })}
                    style={{ width: '100%', padding: '10px 12px', backgroundColor: '#0F172A', border: '1px solid #334155', borderRadius: '6px', color: '#FFFFFF', boxSizing: 'border-box' }}
                    placeholder="+91 98765 43210"
                  />
                </div>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '13px', color: '#C0C7D1', marginBottom: '6px', fontWeight: 600 }}>Service Required</label>
                <select
                  value={quoteForm.service}
                  onChange={(e) => setQuoteForm({ ...quoteForm, service: e.target.value })}
                  style={{ width: '100%', padding: '10px 12px', backgroundColor: '#0F172A', border: '1px solid #334155', borderRadius: '6px', color: '#FFFFFF', boxSizing: 'border-box' }}
                >
                  <option>Full-Stack Web Development</option>
                  <option>Enterprise SaaS Application</option>
                  <option>UI/UX Design Systems</option>
                  <option>AI & Workflow Automation</option>
                </select>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '13px', color: '#C0C7D1', marginBottom: '6px', fontWeight: 600 }}>Project Scope / Requirements</label>
                <textarea
                  rows={4}
                  value={quoteForm.message}
                  onChange={(e) => setQuoteForm({ ...quoteForm, message: e.target.value })}
                  style={{ width: '100%', padding: '10px 12px', backgroundColor: '#0F172A', border: '1px solid #334155', borderRadius: '6px', color: '#FFFFFF', boxSizing: 'border-box' }}
                  placeholder="Describe your goals, required pages, and desired timeline..."
                />
              </div>

              <button
                type="submit"
                disabled={submitting}
                style={{
                  backgroundColor: '#2563EB',
                  color: '#FFFFFF',
                  padding: '12px',
                  borderRadius: '6px',
                  fontWeight: 700,
                  border: 'none',
                  cursor: submitting ? 'not-allowed' : 'pointer',
                  opacity: submitting ? 0.7 : 1,
                  marginTop: '8px',
                }}
              >
                {submitting ? 'Submitting...' : 'Submit Inquiry'}
              </button>
            </form>
          )}
        </div>
      </section>

      {/* Footer */}
      <footer style={{ borderTop: '1px solid rgba(255,255,255,0.08)', padding: '40px 24px', textAlign: 'center', backgroundColor: '#0B1120' }}>
        <p style={{ color: '#9CA3AF', fontSize: '14px', margin: '0 0 8px' }}>
          &copy; 2026 <strong>CODE WIBES TECHNOLOGIES</strong>. All rights reserved.
        </p>
        <p style={{ color: '#6B7280', fontSize: '12px', margin: 0 }}>
          Coimbatore, Tamil Nadu, India · Turning Ideas Into Digital Solutions.
        </p>
      </footer>
    </div>
  );
};
