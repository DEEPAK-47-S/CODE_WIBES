import React, { useState } from 'react';
import { Code, Download, ExternalLink, Play, CheckCircle2, Layers } from 'lucide-react';
import { generateFactoryCodebase, type Project } from '../api';

export function WebsiteFactoryView({ projects }: { projects: Project[] }) {
  const [selectedProjectId, setSelectedProjectId] = useState<string>(projects[0]?.id || '');
  const [projectName, setProjectName] = useState<string>('Custom Client Solution');
  const [techStack, setTechStack] = useState<string>('React + Tailwind + FastAPI');
  const [generating, setGenerating] = useState<boolean>(false);
  const [stagingUrl, setStagingUrl] = useState<string | null>(null);
  const [filesGenerated, setFilesGenerated] = useState<string[]>([]);

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    const projId = selectedProjectId || crypto.randomUUID();
    setGenerating(true);
    try {
      const res = await generateFactoryCodebase(
        projId,
        projectName,
        techStack,
        ['Home', 'Services', 'Case Studies', 'Pricing', 'Contact'],
        ['Responsive Hero', 'Service Catalog', 'Contact Lead Capture', 'Modern Dark Theme']
      );
      setStagingUrl(res.staging_preview_url);
      setFilesGenerated(res.files_generated || []);
    } catch {
      alert('Failed to generate codebase. Please verify backend service.');
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2 style={{ fontSize: '22px', fontWeight: 700, color: '#f8fafc', margin: 0 }}>
            Website & App Factory 2.0
          </h2>
          <p style={{ color: '#94a3b8', fontSize: '13px', margin: '4px 0 0 0' }}>
            Autonomous multi-file React component generation, live sandbox preview, and verified staging builds.
          </p>
        </div>
        <span style={{ background: '#1e293b', border: '1px solid #334155', padding: '6px 14px', borderRadius: '20px', fontSize: '12px', color: '#60a5fa' }}>
          Lead Architects: Forge (D06) & Aura (D05)
        </span>
      </div>

      {/* Generation Controls */}
      <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '14px', padding: '20px' }}>
        <form onSubmit={handleGenerate} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr auto', gap: '16px', alignItems: 'flex-end' }}>
          <div>
            <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '6px', fontWeight: 600 }}>
              Target Project / Client Name
            </label>
            <input
              type="text"
              value={projectName}
              onChange={(e) => setProjectName(e.target.value)}
              placeholder="e.g. Skyline Dental Studio"
              style={{ width: '100%', background: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '10px 14px', color: 'white', fontSize: '13px', outline: 'none' }}
            />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '6px', fontWeight: 600 }}>
              Architecture & Tech Stack
            </label>
            <select
              value={techStack}
              onChange={(e) => setTechStack(e.target.value)}
              style={{ width: '100%', background: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '10px 14px', color: 'white', fontSize: '13px', outline: 'none' }}
            >
              <option value="React + Tailwind + FastAPI">React + Tailwind + FastAPI</option>
              <option value="Next.js + Tailwind + Node">Next.js + Tailwind + Node</option>
              <option value="Vite + TypeScript + PostgreSQL">Vite + TypeScript + PostgreSQL</option>
            </select>
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '6px', fontWeight: 600 }}>
              Link Existing Project (Optional)
            </label>
            <select
              value={selectedProjectId}
              onChange={(e) => {
                setSelectedProjectId(e.target.value);
                const p = projects.find((x) => x.id === e.target.value);
                if (p) setProjectName(p.name);
              }}
              style={{ width: '100%', background: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '10px 14px', color: 'white', fontSize: '13px', outline: 'none' }}
            >
              <option value="">Generate New Standalone Client Workspace</option>
              {projects.map((p) => (
                <option key={p.id} value={p.id}>{p.name}</option>
              ))}
            </select>
          </div>
          <button
            type="submit"
            disabled={generating}
            style={{ background: '#2563eb', color: 'white', border: 'none', borderRadius: '8px', padding: '10px 20px', fontWeight: 600, fontSize: '13px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px' }}
          >
            <Play size={15} />
            {generating ? 'Engineering...' : 'Build Full Codebase'}
          </button>
        </form>
      </div>

      {/* Generated Files & Staging Preview */}
      {stagingUrl && (
        <div style={{ display: 'grid', gridTemplateColumns: '300px 1fr', gap: '20px' }}>
          {/* Left: Files Manifest */}
          <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '14px', padding: '20px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <h3 style={{ fontSize: '15px', fontWeight: 700, color: '#f8fafc', margin: 0, display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Layers size={16} color="#60a5fa" /> Generated Files
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {filesGenerated.map((f, i) => (
                <div key={i} style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '6px', padding: '8px 12px', fontSize: '12px', color: '#cbd5e1', display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <Code size={13} color="#93c5fd" /> {f}
                </div>
              ))}
            </div>
            <a
              href={`http://127.0.0.1:8000/api/v1/factory/export/${selectedProjectId || 'latest'}`}
              download
              style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px', background: '#1e293b', border: '1px solid #334155', color: '#38bdf8', textDecoration: 'none', borderRadius: '8px', padding: '10px', fontSize: '13px', fontWeight: 600 }}
            >
              <Download size={14} /> Download ZIP Package
            </a>
          </div>

          {/* Right: Live Staging Preview Iframe */}
          <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '14px', padding: '16px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: '13px', fontWeight: 600, color: '#4ade80', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <CheckCircle2 size={14} /> Verified Sandbox Preview Running
              </span>
              <a
                href={stagingUrl}
                target="_blank"
                rel="noreferrer"
                style={{ fontSize: '12px', color: '#60a5fa', display: 'flex', alignItems: 'center', gap: '4px', textDecoration: 'none' }}
              >
                Open in New Tab <ExternalLink size={12} />
              </a>
            </div>
            <div style={{ height: '560px', width: '100%', borderRadius: '10px', overflow: 'hidden', border: '1px solid #334155', background: '#020617' }}>
              <iframe
                src={stagingUrl}
                title="CODE WIBES Staging Preview"
                style={{ width: '100%', height: '100%', border: 'none' }}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
