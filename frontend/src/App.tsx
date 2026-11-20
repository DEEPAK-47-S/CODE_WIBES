import React, { useState, useEffect } from 'react';
import {
  LayoutDashboard,
  Building2,
  Users,
  CheckSquare,
  MessageSquare,
  BarChart3,
  Settings,
  Briefcase,
  HelpCircle,
  Search,
  Bell,
  ChevronDown,
  ChevronRight,
  CheckCircle2,
  Trophy,
  Rocket,
  Code,
  Megaphone,
  LineChart,
  UserCheck,
  Cog,
  Upload,
  Plus,
  Send,
  X,
  MapPin,
  Sparkles,
  Terminal,
  Download,
  FileSpreadsheet,
  Globe,
  ExternalLink,
} from 'lucide-react';
import {
  fetchOverviewStats,
  fetchDepartments,
  fetchAgents,
  fetchProjects,
  fetchTasks,
  fetchLeads,
  fetchRecentActivity,
  harvestGoogleMapsLeads,
  exportLeadsCsvUrl,
  exportLeadsJson,
  triggerAutonomousSprint,
  chatWithAgent,
} from './api';
import type {
  OverviewStats,
  Department,
  Agent,
  Project,
  Task,
  Lead,
  ActivityItem,
  AutonomousSprintResult,
  AgentChatResponse,
} from './api';

const jsonParse = (str: string) => {
  try {
    return JSON.parse(str);
  } catch {
    return null;
  }
};

import { PublicWebsite } from './PublicWebsite';

export function App() {
  const [viewMode, setViewMode] = useState<'dashboard' | 'public_website'>('dashboard');
  const [activeMenu, setActiveMenu] = useState<
    'dashboard' | 'departments' | 'employees' | 'tasks' | 'communication' | 'analytics' | 'settings' | 'profile' | 'help'
  >('dashboard');

  const [stats, setStats] = useState<OverviewStats | null>(null);
  const [departments, setDepartments] = useState<Department[]>([]);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [leads, setLeads] = useState<Lead[]>([]);
  const [activities, setActivities] = useState<ActivityItem[]>([]);
  const [loading, setLoading] = useState(true);

  // Executive AI Command Terminal state
  const [sprintObjective, setSprintObjective] = useState('');
  const [sprintRunning, setSprintRunning] = useState(false);
  const [sprintResult, setSprintResult] = useState<AutonomousSprintResult | null>(null);

  // Manage Agent Live Chat Modal
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);
  const [chatMessage, setChatMessage] = useState('');
  const [chatSending, setChatSending] = useState(false);
  const [chatHistory, setChatHistory] = useState<AgentChatResponse[]>([]);

  // Advanced Google Maps Lead Crawler state (Botsol standard)
  const [crawlerMode, setCrawlerMode] = useState<'single' | 'bulk'>('single');
  const [mapsQuery, setMapsQuery] = useState('Software Companies');
  const [mapsLocation, setMapsLocation] = useState('Chennai');
  const [bulkQueriesText, setBulkQueriesText] = useState(
    'HVAC contractors in Dallas, TX\nDental clinics in Lahore\nPlumber in Chicago, IL\nSoftware companies in Chennai'
  );
  const [minRatingFilter, setMinRatingFilter] = useState<number>(0.0);
  const [onlyMissingWebsite, setOnlyMissingWebsite] = useState<boolean>(false);
  const [mapsHarvesting, setMapsHarvesting] = useState(false);
  const [mapsBanner, setMapsBanner] = useState<string | null>(null);

  const loadData = async () => {
    try {
      setLoading(true);
      const [sData, dData, aData, pData, tData, lData, actData] = await Promise.all([
        fetchOverviewStats(),
        fetchDepartments(),
        fetchAgents(),
        fetchProjects(),
        fetchTasks(),
        fetchLeads(),
        fetchRecentActivity(),
      ]);
      setStats(sData);
      setDepartments(dData);
      setAgents(aData);
      setProjects(pData);
      setTasks(tData);
      setLeads(lData);
      setActivities(actData);
    } catch (err) {
      console.error('Failed to load company data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 15000);
    return () => clearInterval(interval);
  }, []);

  const handleExecuteSprint = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!sprintObjective.trim() || sprintRunning) return;

    try {
      setSprintRunning(true);
      setSprintResult(null);
      const result = await triggerAutonomousSprint(sprintObjective);
      setSprintResult(result);
      loadData();
    } catch {
      alert('Failed to execute AI company sprint. Check local Ollama status.');
    } finally {
      setSprintRunning(false);
    }
  };

  const handleOpenManageModal = (agent: Agent) => {
    setSelectedAgent(agent);
    setChatHistory([]);
    setChatMessage('');
  };

  const handleSendAgentChat = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!chatMessage.trim() || !selectedAgent || chatSending) return;

    try {
      setChatSending(true);
      const res = await chatWithAgent(selectedAgent.id, chatMessage);
      setChatHistory((prev) => [...prev, res]);
      setChatMessage('');
      loadData();
    } catch {
      alert('Failed to get response from local agent.');
    } finally {
      setChatSending(false);
    }
  };

  const handleHarvestGoogleMaps = async (e: React.FormEvent) => {
    e.preventDefault();
    if (mapsHarvesting) return;

    try {
      setMapsHarvesting(true);
      setMapsBanner(null);

      let res;
      if (crawlerMode === 'bulk') {
        const queryList = bulkQueriesText
          .split('\n')
          .map((line) => line.trim())
          .filter((line) => line.length > 0);

        if (queryList.length === 0) {
          alert('Please enter at least one search query.');
          setMapsHarvesting(false);
          return;
        }

        res = await harvestGoogleMapsLeads(
          'Bulk Search',
          'Multiple',
          3,
          minRatingFilter,
          onlyMissingWebsite,
          queryList
        );
      } else {
        if (!mapsQuery.trim() || !mapsLocation.trim()) {
          alert('Please enter both Category and Location.');
          setMapsHarvesting(false);
          return;
        }
        res = await harvestGoogleMapsLeads(
          mapsQuery,
          mapsLocation,
          5,
          minRatingFilter,
          onlyMissingWebsite
        );
      }

      setMapsBanner(res.message);
      loadData();
    } catch {
      alert('Failed to harvest leads from Google Maps. Check backend connection.');
    } finally {
      setMapsHarvesting(false);
    }
  };

  const handleExportJson = async () => {
    try {
      const data = await exportLeadsJson();
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'code_wibes_google_maps_leads.json';
      link.click();
      URL.revokeObjectURL(url);
    } catch {
      alert('Failed to export JSON.');
    }
  };

  if (viewMode === 'public_website') {
    return <PublicWebsite onOpenDashboard={() => setViewMode('dashboard')} />;
  }

  return (
    <div className="app-layout">
      {/* 1. LEFT SIDEBAR */}
      <aside className="app-sidebar">
        <div>
          {/* Logo */}
          <div className="brand-header">
            <div className="brand-icon-cw">CW</div>
            <div className="brand-title-wrap">
              <h1>CODE WIBES</h1>
              <h1 style={{ color: '#00f0ff' }}>TECHNOLOGIES</h1>
              <span>Innovate • Automate • Grow</span>
            </div>
          </div>

          {/* Navigation Menu */}
          <nav className="sidebar-nav">
            <div
              className={`nav-item ${activeMenu === 'dashboard' ? 'active' : ''}`}
              onClick={() => setActiveMenu('dashboard')}
            >
              <div className="nav-item-left">
                <LayoutDashboard size={18} className="nav-icon" color="#818cf8" />
                <span>Dashboard</span>
              </div>
              {activeMenu === 'dashboard' && <ChevronRight size={16} />}
            </div>

            <div
              className={`nav-item ${activeMenu === 'departments' ? 'active' : ''}`}
              onClick={() => setActiveMenu('departments')}
            >
              <div className="nav-item-left">
                <Building2 size={18} className="nav-icon" color="#94a3b8" />
                <span>AI Departments</span>
              </div>
            </div>

            <div
              className={`nav-item ${activeMenu === 'employees' ? 'active' : ''}`}
              onClick={() => setActiveMenu('employees')}
            >
              <div className="nav-item-left">
                <Users size={18} className="nav-icon" color="#94a3b8" />
                <span>AI Employees</span>
              </div>
            </div>

            <div
              className={`nav-item ${activeMenu === 'tasks' ? 'active' : ''}`}
              onClick={() => setActiveMenu('tasks')}
            >
              <div className="nav-item-left">
                <CheckSquare size={18} className="nav-icon" color="#94a3b8" />
                <span>Task Manager</span>
              </div>
            </div>

            <div
              className={`nav-item ${activeMenu === 'communication' ? 'active' : ''}`}
              onClick={() => setActiveMenu('communication')}
            >
              <div className="nav-item-left">
                <MessageSquare size={18} className="nav-icon" color="#94a3b8" />
                <span>Communication</span>
              </div>
            </div>

            <div
              className={`nav-item ${activeMenu === 'analytics' ? 'active' : ''}`}
              onClick={() => setActiveMenu('analytics')}
            >
              <div className="nav-item-left">
                <BarChart3 size={18} className="nav-icon" color="#94a3b8" />
                <span>Analytics</span>
              </div>
            </div>

            <div
              className={`nav-item ${activeMenu === 'settings' ? 'active' : ''}`}
              onClick={() => setActiveMenu('settings')}
            >
              <div className="nav-item-left">
                <Settings size={18} className="nav-icon" color="#94a3b8" />
                <span>Settings</span>
              </div>
            </div>

            <div
              className={`nav-item ${activeMenu === 'profile' ? 'active' : ''}`}
              onClick={() => setActiveMenu('profile')}
            >
              <div className="nav-item-left">
                <Briefcase size={18} className="nav-icon" color="#94a3b8" />
                <span>Company Profile</span>
              </div>
            </div>

            <div
              className={`nav-item ${activeMenu === 'help' ? 'active' : ''}`}
              onClick={() => setActiveMenu('help')}
            >
              <div className="nav-item-left">
                <HelpCircle size={18} className="nav-icon" color="#94a3b8" />
                <span>Help & Support</span>
              </div>
            </div>
          </nav>
        </div>

        {/* Sidebar Footer Card */}
        <div className="sidebar-footer-card">
          <div className="rocket-icon-wrap">
            <Rocket size={22} color="#ffffff" />
          </div>
          <h4>Building the Future with AI</h4>
          <button className="btn-hq" onClick={() => setActiveMenu('dashboard')}>
            CODE WIBES HQ
          </button>
        </div>
      </aside>

      {/* 2. MAIN VIEWPORT */}
      <div className="main-viewport">
        {/* Top Header */}
        <header className="top-header">
          {/* Search bar */}
          <div className="search-capsule">
            <Search size={16} color="#64748b" />
            <input
              type="text"
              placeholder="Search anything... (e.g. tasks, employees, departments)"
            />
            <kbd>Ctrl + K</kbd>
          </div>

          {/* Right Header: Notifications & Profile */}
          <div className="header-right-actions">
            <button
              onClick={() => setViewMode('public_website')}
              style={{
                backgroundColor: 'rgba(37,99,235,0.2)',
                color: '#60A5FA',
                border: '1px solid rgba(37,99,235,0.5)',
                padding: '6px 14px',
                borderRadius: '8px',
                cursor: 'pointer',
                fontWeight: 600,
                fontSize: '12px',
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
              }}
            >
              🌐 Public Website
            </button>
            {loading ? (
              <span style={{ fontSize: '11px', color: '#00f0ff', background: 'rgba(0,240,255,0.1)', padding: '4px 10px', borderRadius: '12px', border: '1px solid rgba(0,240,255,0.3)', fontWeight: 600 }}>
                ⚡ Syncing...
              </span>
            ) : (
              <span style={{ fontSize: '11px', color: '#10b981', background: 'rgba(16,185,129,0.1)', padding: '4px 10px', borderRadius: '12px', border: '1px solid rgba(16,185,129,0.3)', fontWeight: 600 }}>
                🟢 Live
              </span>
            )}
            <div className="notification-bell" title="3 Notifications">
              <Bell size={18} />
              <div className="bell-badge">3</div>
            </div>

            <div className="user-profile-pill">
              <div className="user-avatar">D</div>
              <div className="user-info">
                <h5>Deepak</h5>
                <p>CEO & Founder</p>
              </div>
              <ChevronDown size={14} color="#94a3b8" />
            </div>
          </div>
        </header>

        {/* Dashboard Dynamic Content */}
        <div className="dashboard-content">
          {/* TAB: DASHBOARD (HOME) */}
          {activeMenu === 'dashboard' && (
            <>
              {/* Hero Section */}
              <div className="welcome-hero-card">
                <div className="welcome-text">
                  <h6>Welcome to</h6>
                  <h1>CODE WIBES TECHNOLOGIES</h1>
                  <p>Your AI-Powered Software Company</p>
                </div>

                <div className="hero-robot-artwork">
                  <div className="robot-cyber-avatar">
                    <Sparkles size={46} color="#00f0ff" />
                  </div>
                  <div className="hologram-glass-badge">
                    <span>Dream Big...</span>
                    <span>Build Smart...</span>
                    <span>Grow Together...</span>
                  </div>
                </div>
              </div>

              {/* Owner AI Executive Command Terminal */}
              <div className="owner-terminal-card">
                <div className="terminal-header">
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <Terminal size={18} color="#00f0ff" />
                    <span style={{ fontSize: '13px', fontWeight: 800, color: '#ffffff', letterSpacing: '0.05em' }}>
                      FOUNDER & CEO EXECUTIVE DISPATCH • LOCAL GPU INFERENCE
                    </span>
                  </div>
                  <span style={{ fontSize: '11px', color: '#10b981', background: 'rgba(16,185,129,0.1)', padding: '3px 10px', borderRadius: '12px' }}>
                    ● Real Ollama Runtime (RTX 4050 6GB)
                  </span>
                </div>

                <form onSubmit={handleExecuteSprint} style={{ display: 'flex', gap: '12px', marginTop: '12px' }}>
                  <input
                    type="text"
                    value={sprintObjective}
                    onChange={(e) => setSprintObjective(e.target.value)}
                    placeholder="Give an order to your AI company (e.g. 'Build an e-commerce platform', 'Scrape 20 software firms in Bangalore', 'Run security audit')..."
                    style={{
                      flex: 1,
                      background: '#070913',
                      border: '1px solid rgba(0,240,255,0.3)',
                      borderRadius: '10px',
                      padding: '12px 18px',
                      color: '#ffffff',
                      fontSize: '13.5px',
                      outline: 'none',
                    }}
                  />
                  <button
                    type="submit"
                    disabled={sprintRunning}
                    className="btn-hq"
                    style={{ padding: '0 24px', display: 'flex', alignItems: 'center', gap: '8px', whiteSpace: 'nowrap' }}
                  >
                    <Sparkles size={16} />
                    {sprintRunning ? 'AI Agents Executing...' : 'Execute AI Sprint'}
                  </button>
                </form>

                {/* Quick Action Chips */}
                <div style={{ display: 'flex', gap: '8px', marginTop: '10px', flexWrap: 'wrap' }}>
                  <button
                    type="button"
                    onClick={() => setSprintObjective('Build a modern React + FastAPI customer portal with authentication')}
                    className="quick-chip"
                  >
                    💻 Build Web App
                  </button>
                  <button
                    type="button"
                    onClick={() => setSprintObjective('Harvest 15 digital marketing agencies in Chennai from Google Maps')}
                    className="quick-chip"
                  >
                    🗺️ Harvest Google Maps Leads
                  </button>
                  <button
                    type="button"
                    onClick={() => setSprintObjective('Audit API security and generate automated test suite')}
                    className="quick-chip"
                  >
                    🛡️ Security & QA Audit
                  </button>
                  <button
                    type="button"
                    onClick={() => setSprintObjective('Formulate Q1 client acquisition strategy and cold pitch templates')}
                    className="quick-chip"
                  >
                    📢 Marketing & Sales Campaign
                  </button>
                </div>

                {/* Live Execution Output Window */}
                {sprintResult && (
                  <div className="sprint-output-box">
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                      <span style={{ color: '#34d399', fontWeight: 800 }}>✓ Sprint Completed by Autonomous Agents</span>
                      <span style={{ color: '#64748b', cursor: 'pointer' }} onClick={() => setSprintResult(null)}>✕ Close</span>
                    </div>
                    <div style={{ fontSize: '13px', color: '#e2e8f0', whiteSpace: 'pre-wrap', maxHeight: '200px', overflowY: 'auto' }}>
                      <p style={{ color: '#38bdf8', fontWeight: 700, marginBottom: '4px' }}>[CEO Nexus Plan]:</p>
                      <p style={{ marginBottom: '10px' }}>{sprintResult.ceo_plan}</p>
                      {sprintResult.code_generated && (
                        <>
                          <p style={{ color: '#c084fc', fontWeight: 700, marginBottom: '4px' }}>[Engineer Forge Code Generated]:</p>
                          <pre style={{ background: '#050711', padding: '10px', borderRadius: '8px', fontSize: '12px' }}>
                            {sprintResult.code_generated.slice(0, 1000)}...
                          </pre>
                        </>
                      )}
                    </div>
                  </div>
                )}
              </div>

              {/* 4 Metric Cards (100% Real PostgreSQL Data) */}
              <div className="metric-stats-row">
                {/* 1. Departments */}
                <div className="metric-pill-card">
                  <div className="metric-icon-square purple">
                    <Building2 size={24} color="#ffffff" />
                  </div>
                  <div className="metric-data">
                    <h3>{departments.length}</h3>
                    <p>AI Departments</p>
                    <span className="trend">100% Operational</span>
                  </div>
                </div>

                {/* 2. AI Employees */}
                <div className="metric-pill-card">
                  <div className="metric-icon-square blue">
                    <Users size={24} color="#ffffff" />
                  </div>
                  <div className="metric-data">
                    <h3>{agents.length}</h3>
                    <p>AI Employees</p>
                    <span className="trend">RTX 4050 GPU</span>
                  </div>
                </div>

                {/* 3. Tasks */}
                <div className="metric-pill-card">
                  <div className="metric-icon-square green">
                    <CheckCircle2 size={24} color="#ffffff" />
                  </div>
                  <div className="metric-data">
                    <h3>{tasks.length}</h3>
                    <p>Sprint Tasks</p>
                    <span className="trend">{tasks.filter((t) => t.status === 'in_progress').length} In Progress</span>
                  </div>
                </div>

                {/* 4. Completion Rate */}
                <div className="metric-pill-card">
                  <div className="metric-icon-square gold">
                    <Trophy size={24} color="#ffffff" />
                  </div>
                  <div className="metric-data">
                    <h3>{tasks.length > 0 ? Math.round((tasks.filter((t) => t.status === 'completed').length / tasks.length) * 100) : 0}%</h3>
                    <p>Completion Rate</p>
                    <span className="trend">{tasks.filter((t) => t.status === 'completed').length} Completed</span>
                  </div>
                </div>
              </div>

              {/* Middle 3 Columns Grid */}
              <div className="dashboard-tri-columns">
                {/* Left Column: AI Departments (Real DB Mapping) */}
                <div className="dash-panel">
                  <div className="panel-header">
                    <h3>AI Departments</h3>
                    <span className="view-all-link" onClick={() => setActiveMenu('departments')}>
                      View All →
                    </span>
                  </div>

                  <div className="departments-2col-grid">
                    {departments.map((dept, idx) => {
                      const count = agents.filter((a) => a.department_id === dept.id).length;
                      const iconClass =
                        dept.slug === 'software-development'
                          ? 'dev'
                          : dept.slug === 'digital-marketing'
                          ? 'mkt'
                          : dept.slug === 'sales-lead-gen'
                          ? 'sal'
                          : dept.slug === 'ui-ux-creative'
                          ? 'hr'
                          : 'ops';

                      return (
                        <div
                          key={dept.id}
                          className="dept-pill-box"
                          style={idx === departments.length - 1 && departments.length % 2 !== 0 ? { gridColumn: 'span 2' } : {}}
                        >
                          <div className={`dept-pill-icon ${iconClass}`}>
                            {dept.slug === 'software-development' ? (
                              <Code size={18} />
                            ) : dept.slug === 'digital-marketing' ? (
                              <Megaphone size={18} />
                            ) : dept.slug === 'sales-lead-gen' ? (
                              <LineChart size={18} />
                            ) : dept.slug === 'ui-ux-creative' ? (
                              <UserCheck size={18} />
                            ) : (
                              <Cog size={18} />
                            )}
                          </div>
                          <div className="dept-info">
                            <h4>{dept.name}</h4>
                            <p>{count} AI Employee{count === 1 ? '' : 's'}</p>
                          </div>
                          <div className="active-dot-label">
                            <span className="dot"></span>
                            <span>Active</span>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Middle Column: AI Employees */}
                <div className="dash-panel">
                  <div className="panel-header">
                    <h3>AI Employees</h3>
                    <span className="view-all-link" onClick={() => setActiveMenu('employees')}>
                      View All →
                    </span>
                  </div>

                  <div className="employees-list">
                    {[...agents]
                      .sort((a, b) => {
                        const order = ['Nexus', 'Forge', 'Echo', 'Ledger', 'Atlas'];
                        const ia = order.indexOf(a.name);
                        const ib = order.indexOf(b.name);
                        return (ia === -1 ? 99 : ia) - (ib === -1 ? 99 : ib);
                      })
                      .slice(0, 5)
                      .map((agent, i) => (
                        <div key={agent.id} className="employee-row-item">
                          <div className="emp-avatar-wrap">
                            <div
                              className="emp-avatar"
                              style={{
                                background:
                                  i === 0
                                    ? 'linear-gradient(135deg, #8b5cf6, #ec4899)'
                                    : i === 1
                                    ? 'linear-gradient(135deg, #0284c7, #3b82f6)'
                                    : i === 2
                                    ? 'linear-gradient(135deg, #10b981, #06b6d4)'
                                    : 'linear-gradient(135deg, #f59e0b, #ef4444)',
                              }}
                            >
                              {agent.name.charAt(0)}
                            </div>
                            <div className="emp-details">
                              <h4>{agent.name}</h4>
                              <p>{agent.role}</p>
                            </div>
                          </div>

                          <div className="emp-actions">
                            <div className="active-dot-label">
                              <span className="dot"></span>
                              <span>Online</span>
                            </div>
                            <button
                              className="btn-manage"
                              onClick={() => handleOpenManageModal(agent)}
                            >
                              Manage
                            </button>
                          </div>
                        </div>
                      ))}
                  </div>
                </div>

                {/* Right Column: Recent Activity (Live from Database) */}
                <div className="dash-panel">
                  <div className="panel-header">
                    <h3>Recent Activity</h3>
                    <span className="view-all-link" onClick={() => setActiveMenu('tasks')}>
                      View All →
                    </span>
                  </div>

                  <div className="activity-feed-list">
                    {activities.length > 0 ? (
                      activities.slice(0, 4).map((act, i) => (
                        <div key={act.id || i} className="activity-feed-item">
                          <div
                            className={`activity-icon-bubble ${
                              i === 0 ? 'green' : i === 1 ? 'blue' : i === 2 ? 'purple' : 'amber'
                            }`}
                          >
                            {i === 0 ? (
                              <CheckCircle2 size={16} />
                            ) : i === 1 ? (
                              <MessageSquare size={16} />
                            ) : i === 2 ? (
                              <Plus size={16} />
                            ) : (
                              <Upload size={16} />
                            )}
                          </div>
                          <div className="activity-text-wrap">
                            <h5>{act.title}</h5>
                            <p>{act.subtitle}</p>
                            <span className="time">{act.time}</span>
                          </div>
                        </div>
                      ))
                    ) : (
                      <div className="activity-feed-item">
                        <div className="activity-icon-bubble green">
                          <CheckCircle2 size={16} />
                        </div>
                        <div className="activity-text-wrap">
                          <h5>System Initialized</h5>
                          <p>All AI agents operational on RTX 4050 GPU</p>
                          <span className="time">Just now</span>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Bottom Row (2 Wide Cards) */}
              <div className="dashboard-bottom-row">
                {/* 1. Real Company Performance & Velocity (100% Database Driven) */}
                <div className="chart-panel-card">
                  <div className="chart-header">
                    <div>
                      <h3 style={{ fontSize: '15px', fontWeight: 800 }}>Company Sprint & Pipeline Velocity</h3>
                      <p style={{ fontSize: '11.5px', color: '#94a3b8', marginTop: '2px' }}>
                        Live metrics from local PostgreSQL database
                      </p>
                    </div>
                    <div className="chart-legend">
                      <span>
                        <span className="legend-dot purple"></span>In Progress ({tasks.filter((t) => t.status === 'in_progress').length})
                      </span>
                      <span>
                        <span className="legend-dot blue"></span>Done ({tasks.filter((t) => t.status === 'completed').length})
                      </span>
                      <span className="pill-92" style={{ background: 'rgba(16, 185, 129, 0.2)', color: '#34d399', border: '1px solid rgba(16, 185, 129, 0.4)' }}>
                        {tasks.length > 0 ? Math.round((tasks.filter((t) => t.status === 'completed').length / tasks.length) * 100) : 0}% Done
                      </span>
                    </div>
                  </div>

                  {/* Real Metrics Visualization */}
                  <div style={{ padding: '16px 0 0', display: 'flex', flexDirection: 'column', gap: '14px' }}>
                    {/* Progress Bar */}
                    <div>
                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '6px' }}>
                        <span style={{ color: '#94a3b8' }}>Overall Sprint Completion</span>
                        <span style={{ color: '#00f0ff', fontWeight: 700 }}>
                          {tasks.filter((t) => t.status === 'completed').length} / {tasks.length} Tasks
                        </span>
                      </div>
                      <div style={{ width: '100%', height: '8px', background: 'rgba(255,255,255,0.06)', borderRadius: '9999px', overflow: 'hidden' }}>
                        <div
                          style={{
                            height: '100%',
                            width: `${tasks.length > 0 ? Math.min(100, Math.round((tasks.filter((t) => t.status === 'completed').length / tasks.length) * 100)) : 0}%`,
                            background: 'linear-gradient(90deg, #00f0ff, #10b981)',
                            borderRadius: '9999px',
                            transition: 'width 0.5s ease',
                          }}
                        />
                      </div>
                    </div>

                    {/* 3 Metric Pills */}
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '10px' }}>
                      <div style={{ background: '#0a0d1e', border: '1px solid var(--border-subtle)', borderRadius: '10px', padding: '10px 12px' }}>
                        <div style={{ fontSize: '11px', color: '#94a3b8' }}>Active Projects</div>
                        <div style={{ fontSize: '16px', fontWeight: 800, color: '#ffffff', marginTop: '2px' }}>
                          {projects.length}
                        </div>
                      </div>
                      <div style={{ background: '#0a0d1e', border: '1px solid var(--border-subtle)', borderRadius: '10px', padding: '10px 12px' }}>
                        <div style={{ fontSize: '11px', color: '#94a3b8' }}>Pending Tasks</div>
                        <div style={{ fontSize: '16px', fontWeight: 800, color: '#fbbf24', marginTop: '2px' }}>
                          {tasks.filter((t) => t.status === 'pending').length}
                        </div>
                      </div>
                      <div style={{ background: '#0a0d1e', border: '1px solid var(--border-subtle)', borderRadius: '10px', padding: '10px 12px' }}>
                        <div style={{ fontSize: '11px', color: '#94a3b8' }}>CRM Pipeline</div>
                        <div style={{ fontSize: '16px', fontWeight: 800, color: '#34d399', marginTop: '2px' }}>
                          ${(stats?.pipeline_value ?? 0).toLocaleString()}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* 2. Golden Trophy Inspiration Card */}
                <div className="trophy-inspiration-card">
                  <div className="trophy-image-wrap">
                    <Trophy size={48} color="#f59e0b" />
                  </div>

                  <div className="trophy-text-col">
                    <h3>Together we build a smarter tomorrow</h3>
                    <p>CODE WIBES TECHNOLOGIES</p>
                    <button className="btn-vision" onClick={() => setActiveMenu('profile')}>
                      Our Vision →
                    </button>
                  </div>

                  <div className="vision-checklist">
                    <div className="checklist-item">
                      <CheckCircle2 size={16} />
                      <span>AI-Powered Organization</span>
                    </div>
                    <div className="checklist-item">
                      <CheckCircle2 size={16} />
                      <span>Smart Workforce</span>
                    </div>
                    <div className="checklist-item">
                      <CheckCircle2 size={16} />
                      <span>Infinite Possibilities</span>
                    </div>
                  </div>
                </div>
              </div>
            </>
          )}

          {/* TAB: DEPARTMENTS */}
          {activeMenu === 'departments' && (
            <div>
              <div style={{ marginBottom: '24px' }}>
                <h2 style={{ fontSize: '24px', fontWeight: 800 }}>Company AI Departments</h2>
                <p style={{ color: '#94a3b8', fontSize: '14px' }}>
                  6 Specialized organizational units managed by autonomous AI agents.
                </p>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '20px' }}>
                {departments.map((dept) => (
                  <div key={dept.id} className="dash-panel" style={{ gap: '14px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <h3 style={{ fontSize: '17px', color: '#ffffff' }}>{dept.name}</h3>
                      <span className="active-dot-label">
                        <span className="dot"></span> Active
                      </span>
                    </div>
                    <p style={{ fontSize: '13px', color: '#94a3b8', lineHeight: '1.5' }}>{dept.description}</p>
                    <div style={{ borderTop: '1px solid rgba(255,255,255,0.06)', paddingTop: '12px', display: 'flex', justifyContent: 'space-between', fontSize: '12px', color: '#64748b' }}>
                      <span>Slug: {dept.slug}</span>
                      <span style={{ color: '#818cf8', fontWeight: 700 }}>Autonomous</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB: EMPLOYEES */}
          {activeMenu === 'employees' && (
            <div>
              <div style={{ marginBottom: '24px' }}>
                <h2 style={{ fontSize: '24px', fontWeight: 800 }}>AI Employees Roster</h2>
                <p style={{ color: '#94a3b8', fontSize: '14px' }}>
                  All 8 specialized autonomous agents powered by local RTX 4050 GPU Ollama models.
                </p>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '20px' }}>
                {agents.map((agent) => (
                  <div key={agent.id} className="dash-panel" style={{ gap: '14px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                      <div>
                        <h3 style={{ fontSize: '16px', color: '#ffffff' }}>{agent.name}</h3>
                        <p style={{ fontSize: '12px', color: '#00f0ff', fontWeight: 700 }}>{agent.role}</p>
                      </div>
                      <button className="btn-manage" onClick={() => handleOpenManageModal(agent)}>
                        Manage
                      </button>
                    </div>

                    <p style={{ fontSize: '13px', color: '#94a3b8', lineHeight: '1.5' }}>{agent.description}</p>

                    <div style={{ background: '#0a0d1e', padding: '10px 14px', borderRadius: '10px', fontSize: '12px', display: 'flex', justifyContent: 'space-between' }}>
                      <span style={{ color: '#64748b' }}>Ollama Model:</span>
                      <span style={{ color: '#c084fc', fontWeight: 700 }}>{agent.model_name || 'qwen3.5:4b'}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB: TASKS */}
          {activeMenu === 'tasks' && (
            <div>
              <div style={{ marginBottom: '24px' }}>
                <h2 style={{ fontSize: '24px', fontWeight: 800 }}>Task & Project Manager</h2>
                <p style={{ color: '#94a3b8', fontSize: '14px' }}>
                  Real-time sprint backlog executed by Atlas (PM), Forge (Dev), and Sentinel (QA).
                </p>
              </div>

              {/* Company Projects Section */}
              <div style={{ marginBottom: '32px' }}>
                <h3 style={{ fontSize: '18px', fontWeight: 700, marginBottom: '14px', color: '#ffffff' }}>
                  Active Projects ({projects.length})
                </h3>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '16px' }}>
                  {projects.map((proj) => (
                    <div key={proj.id} className="dash-panel" style={{ gap: '10px' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <h4 style={{ fontSize: '15px', fontWeight: 700, color: '#ffffff' }}>{proj.name}</h4>
                        <span style={{ fontSize: '11px', padding: '3px 8px', borderRadius: '8px', background: 'rgba(99,102,241,0.2)', color: '#818cf8', fontWeight: 700 }}>
                          {proj.status.toUpperCase()}
                        </span>
                      </div>
                      <p style={{ fontSize: '12.5px', color: '#94a3b8' }}>{proj.description}</p>
                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '11px', color: '#64748b', marginTop: '6px' }}>
                        <span>Priority: <strong style={{ color: '#00f0ff' }}>{proj.priority.toUpperCase()}</strong></span>
                        <span>Progress: <strong style={{ color: '#10b981' }}>{proj.progress}%</strong></span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <h3 style={{ fontSize: '18px', fontWeight: 700, marginBottom: '14px', color: '#ffffff' }}>
                Sprint Tasks ({tasks.length})
              </h3>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {tasks.map((task) => (
                  <div
                    key={task.id}
                    style={{
                      background: 'var(--bg-card)',
                      border: '1px solid var(--border-subtle)',
                      borderRadius: '14px',
                      padding: '18px 24px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                    }}
                  >
                    <div>
                      <h4 style={{ fontSize: '15px', fontWeight: 700, color: '#ffffff' }}>{task.title}</h4>
                      <p style={{ fontSize: '12.5px', color: '#94a3b8', marginTop: '4px' }}>
                        {task.description || 'Assigned to Autonomous Agent'}
                      </p>
                    </div>

                    <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
                      <span style={{ fontSize: '11px', fontWeight: 800, color: '#00f0ff' }}>
                        PRIORITY: {task.priority.toUpperCase()}
                      </span>
                      <span
                        style={{
                          fontSize: '11px',
                          fontWeight: 800,
                          padding: '4px 10px',
                          borderRadius: '9999px',
                          background: 'rgba(16, 185, 129, 0.15)',
                          color: '#34d399',
                          border: '1px solid rgba(16, 185, 129, 0.3)',
                          textTransform: 'uppercase',
                        }}
                      >
                        {task.status}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB: ANALYTICS (GOOGLE MAPS CRAWLER STUDIO - BOTSOL STANDARD) */}
          {activeMenu === 'analytics' && (
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '24px', flexWrap: 'wrap', gap: '16px' }}>
                <div>
                  <h2 style={{ fontSize: '24px', fontWeight: 800 }}>Google Maps Lead Crawler & Studio</h2>
                  <p style={{ color: '#94a3b8', fontSize: '14px', marginTop: '4px' }}>
                    Automated B2B lead generation matching the Botsol standard. Extract verified contacts and export to Excel/CSV or JSON.
                  </p>
                </div>

                <div style={{ display: 'flex', gap: '10px' }}>
                  <a href={exportLeadsCsvUrl} download="code_wibes_leads.csv" className="btn-export green">
                    <FileSpreadsheet size={15} />
                    Export to Excel / CSV
                  </a>
                  <button onClick={handleExportJson} className="btn-export">
                    <Download size={15} />
                    Export JSON Array
                  </button>
                </div>
              </div>

              {/* Crawler Configuration Card */}
              <div className="crawler-card">
                {/* Search Mode Toggle */}
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px', borderBottom: '1px solid var(--border-subtle)', paddingBottom: '14px' }}>
                  <div style={{ display: 'flex', gap: '8px' }}>
                    <button
                      type="button"
                      className={`mode-pill ${crawlerMode === 'single' ? 'active' : 'inactive'}`}
                      onClick={() => setCrawlerMode('single')}
                    >
                      Single Search (Niche + City)
                    </button>
                    <button
                      type="button"
                      className={`mode-pill ${crawlerMode === 'bulk' ? 'active' : 'inactive'}`}
                      onClick={() => setCrawlerMode('bulk')}
                    >
                      Multi-Search / Bulk List
                    </button>
                  </div>

                  <span style={{ fontSize: '12px', color: '#00f0ff', fontWeight: 700 }}>
                    Hunter Agent • Local RTX 4050 GPU
                  </span>
                </div>

                <form onSubmit={handleHarvestGoogleMaps}>
                  {crawlerMode === 'single' ? (
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '16px', marginBottom: '18px' }}>
                      <div>
                        <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '6px' }}>
                          Target Niche / Category
                        </label>
                        <input
                          type="text"
                          required
                          value={mapsQuery}
                          onChange={(e) => setMapsQuery(e.target.value)}
                          placeholder="e.g. HVAC contractors, Dental clinics, Web agencies"
                          style={{
                            width: '100%',
                            background: '#070913',
                            border: '1px solid rgba(255,255,255,0.15)',
                            borderRadius: '10px',
                            padding: '11px 16px',
                            color: 'white',
                            fontSize: '13.5px',
                            outline: 'none',
                          }}
                        />
                      </div>

                      <div>
                        <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '6px' }}>
                          Location (City, State / ZIP)
                        </label>
                        <input
                          type="text"
                          required
                          value={mapsLocation}
                          onChange={(e) => setMapsLocation(e.target.value)}
                          placeholder="e.g. Dallas, TX or Chennai or Chicago, IL 60611"
                          style={{
                            width: '100%',
                            background: '#070913',
                            border: '1px solid rgba(255,255,255,0.15)',
                            borderRadius: '10px',
                            padding: '11px 16px',
                            color: 'white',
                            fontSize: '13.5px',
                            outline: 'none',
                          }}
                        />
                      </div>
                    </div>
                  ) : (
                    <div style={{ marginBottom: '18px' }}>
                      <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '6px' }}>
                        Multi-Search Query List (One query per line — e.g. "plumber in Chicago, IL 60611")
                      </label>
                      <textarea
                        rows={4}
                        value={bulkQueriesText}
                        onChange={(e) => setBulkQueriesText(e.target.value)}
                        style={{
                          width: '100%',
                          background: '#070913',
                          border: '1px solid rgba(255,255,255,0.15)',
                          borderRadius: '10px',
                          padding: '12px 16px',
                          color: 'white',
                          fontSize: '13px',
                          fontFamily: 'JetBrains Mono, monospace',
                          outline: 'none',
                          lineHeight: '1.5',
                        }}
                      />
                    </div>
                  )}

                  {/* Filter Row */}
                  <div style={{ display: 'flex', gap: '20px', alignItems: 'center', flexWrap: 'wrap', marginBottom: '20px', background: 'rgba(255,255,255,0.02)', padding: '12px 16px', borderRadius: '10px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                      <label style={{ fontSize: '12px', color: '#94a3b8' }}>Filter Rating:</label>
                      <select
                        value={minRatingFilter}
                        onChange={(e) => setMinRatingFilter(parseFloat(e.target.value))}
                        style={{
                          background: '#0a0d1e',
                          color: '#ffffff',
                          border: '1px solid rgba(255,255,255,0.15)',
                          borderRadius: '6px',
                          padding: '6px 10px',
                          fontSize: '12.5px',
                          outline: 'none',
                        }}
                      >
                        <option value={0.0}>All Ratings</option>
                        <option value={4.0}>⭐ 4.0+ Stars</option>
                        <option value={4.5}>⭐ 4.5+ Stars</option>
                      </select>
                    </div>

                    <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', fontSize: '12.5px', color: '#fbbf24', fontWeight: 600 }}>
                      <input
                        type="checkbox"
                        checked={onlyMissingWebsite}
                        onChange={(e) => setOnlyMissingWebsite(e.target.checked)}
                        style={{ cursor: 'pointer', accentColor: '#fbbf24' }}
                      />
                      🔥 Only businesses without a website (Web Design Qualification Trick)
                    </label>
                  </div>

                  <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
                    <button
                      type="submit"
                      disabled={mapsHarvesting}
                      className="btn-hq"
                      style={{ padding: '12px 32px', height: '46px', display: 'flex', alignItems: 'center', gap: '10px' }}
                    >
                      <MapPin size={18} />
                      {mapsHarvesting ? 'Hunter Agent Crawling Google Maps...' : 'Start Google Maps Crawler'}
                    </button>
                  </div>
                </form>

                {mapsBanner && (
                  <div style={{ marginTop: '16px', padding: '12px 16px', borderRadius: '10px', background: 'rgba(52, 211, 153, 0.1)', border: '1px solid rgba(52, 211, 153, 0.3)', color: '#34d399', fontSize: '13px' }}>
                    ✓ {mapsBanner}
                  </div>
                )}
              </div>

              {/* Leads Data Table */}
              <div style={{ background: 'var(--bg-card)', borderRadius: '16px', border: '1px solid var(--border-subtle)', overflow: 'hidden' }}>
                <div style={{ padding: '16px 20px', borderBottom: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <h3 style={{ fontSize: '16px', fontWeight: 800, color: '#ffffff' }}>
                    Extracted Google Maps Directory ({leads.length} Records)
                  </h3>
                  <span style={{ fontSize: '12px', color: '#94a3b8' }}>
                    Auto-saved to PostgreSQL `leads`
                  </span>
                </div>

                <div style={{ overflowX: 'auto' }}>
                  <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '13px' }}>
                    <thead>
                      <tr style={{ background: 'rgba(255,255,255,0.03)', borderBottom: '1px solid var(--border-subtle)', color: '#94a3b8' }}>
                        <th style={{ padding: '12px 18px' }}>Business & Niche</th>
                        <th style={{ padding: '12px 18px' }}>Phone & Email</th>
                        <th style={{ padding: '12px 18px' }}>Location / Address</th>
                        <th style={{ padding: '12px 18px' }}>Website Status</th>
                        <th style={{ padding: '12px 18px' }}>Est. Value</th>
                        <th style={{ padding: '12px 18px' }}>Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      {leads.map((lead) => {
                        let parsedNotes: any = null;
                        if (lead.notes && lead.notes.startsWith('{')) {
                          try {
                            parsedNotes = jsonParse(lead.notes);
                          } catch {
                            // ignore
                          }
                        }
                        const phone = parsedNotes?.phone || 'Available';
                        const website = parsedNotes?.website;
                        const hasWebsite = parsedNotes?.has_website ?? Boolean(website);

                        return (
                          <tr key={lead.id} style={{ borderBottom: '1px solid var(--border-subtle)' }}>
                            <td style={{ padding: '14px 18px' }}>
                              <div style={{ fontWeight: 700, color: '#f8fafc', fontSize: '14px' }}>
                                {lead.company_name}
                              </div>
                              <span style={{ fontSize: '11px', color: '#00f0ff', background: 'rgba(0, 240, 255, 0.1)', padding: '2px 8px', borderRadius: '6px', display: 'inline-block', marginTop: '4px' }}>
                                {lead.industry}
                              </span>
                            </td>

                            <td style={{ padding: '14px 18px' }}>
                              <div style={{ color: '#e2e8f0', fontWeight: 600 }}>{phone}</div>
                              <div style={{ color: '#94a3b8', fontSize: '11.5px', marginTop: '2px' }}>
                                {lead.contact_email || 'Verified on Maps'}
                              </div>
                            </td>

                            <td style={{ padding: '14px 18px', color: '#94a3b8', maxWidth: '240px' }}>
                              {parsedNotes?.street_address || lead.notes || 'Commercial Center'}
                            </td>

                            <td style={{ padding: '14px 18px' }}>
                              {hasWebsite && website ? (
                                <a
                                  href={website.startsWith('http') ? website : `https://${website}`}
                                  target="_blank"
                                  rel="noreferrer"
                                  style={{
                                    display: 'inline-flex',
                                    alignItems: 'center',
                                    gap: '6px',
                                    color: '#38bdf8',
                                    fontSize: '11.5px',
                                    textDecoration: 'none',
                                    background: 'rgba(56, 189, 248, 0.1)',
                                    padding: '4px 10px',
                                    borderRadius: '6px',
                                    border: '1px solid rgba(56, 189, 248, 0.25)',
                                  }}
                                >
                                  <Globe size={13} />
                                  Live Website
                                  <ExternalLink size={10} />
                                </a>
                              ) : (
                                <span
                                  style={{
                                    display: 'inline-flex',
                                    alignItems: 'center',
                                    gap: '4px',
                                    color: '#fbbf24',
                                    fontSize: '11.5px',
                                    background: 'rgba(251, 191, 36, 0.12)',
                                    padding: '4px 10px',
                                    borderRadius: '6px',
                                    border: '1px solid rgba(251, 191, 36, 0.3)',
                                    fontWeight: 700,
                                  }}
                                >
                                  ⚠️ No Website Found
                                </span>
                              )}
                            </td>

                            <td style={{ padding: '14px 18px', fontWeight: 800, color: '#34d399', fontSize: '13.5px' }}>
                              ${lead.estimated_value.toLocaleString()}
                            </td>

                            <td style={{ padding: '14px 18px' }}>
                              <button
                                onClick={() => {
                                  const hunter = agents.find((a) => a.name === 'Hunter');
                                  if (hunter) {
                                    handleOpenManageModal(hunter);
                                    setChatMessage(`Draft a personalized cold pitch for ${lead.company_name} offering web development and AI automation.`);
                                  }
                                }}
                                style={{
                                  background: 'rgba(139, 92, 246, 0.15)',
                                  border: '1px solid rgba(139, 92, 246, 0.35)',
                                  color: '#c084fc',
                                  padding: '5px 12px',
                                  borderRadius: '6px',
                                  fontSize: '11.5px',
                                  fontWeight: 700,
                                  cursor: 'pointer',
                                }}
                              >
                                Pitch via Hunter
                              </button>
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {/* TAB: COMMUNICATION */}
          {activeMenu === 'communication' && (
            <div>
              <div style={{ marginBottom: '24px' }}>
                <h2 style={{ fontSize: '24px', fontWeight: 800 }}>Communication & Live Agent Intercom</h2>
                <p style={{ color: '#94a3b8', fontSize: '14px' }}>
                  Chat directly with any AI executive. Select an agent to start talking.
                </p>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '16px' }}>
                {agents.map((agent) => (
                  <div
                    key={agent.id}
                    className="dash-panel"
                    style={{ cursor: 'pointer', transition: 'all 0.2s ease' }}
                    onClick={() => handleOpenManageModal(agent)}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                      <div className="emp-avatar">{agent.name.charAt(0)}</div>
                      <div>
                        <h4 style={{ fontSize: '15px', color: '#ffffff' }}>{agent.name}</h4>
                        <p style={{ fontSize: '12px', color: '#00f0ff' }}>{agent.role}</p>
                      </div>
                    </div>
                    <div style={{ marginTop: '12px', display: 'flex', justifyContent: 'space-between', fontSize: '12px', color: '#64748b' }}>
                      <span>Model: {agent.model_name || 'qwen3.5:4b'}</span>
                      <span style={{ color: '#818cf8', fontWeight: 700 }}>Open Chat →</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB: SETTINGS & PROFILE */}
          {(activeMenu === 'settings' || activeMenu === 'profile' || activeMenu === 'help') && (
            <div>
              <div style={{ marginBottom: '24px' }}>
                <h2 style={{ fontSize: '24px', fontWeight: 800 }}>Company Configuration & Profile</h2>
                <p style={{ color: '#94a3b8', fontSize: '14px' }}>
                  CODE WIBES TECHNOLOGIES executive settings.
                </p>
              </div>

              <div className="dash-panel" style={{ maxWidth: '650px', gap: '16px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: '#94a3b8' }}>Company Name:</span>
                  <span style={{ fontWeight: 700, color: '#ffffff' }}>CODE WIBES TECHNOLOGIES</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: '#94a3b8' }}>Founder & CEO:</span>
                  <span style={{ fontWeight: 700, color: '#38bdf8' }}>Deepak</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: '#94a3b8' }}>Inference Hardware:</span>
                  <span style={{ fontWeight: 700, color: '#34d399' }}>NVIDIA RTX 4050 6GB VRAM (Local Ollama)</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: '#94a3b8' }}>Database:</span>
                  <span style={{ fontWeight: 700, color: '#ffffff' }}>PostgreSQL 19 (`code_wibes`)</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* 3. MANAGE AGENT LIVE CHAT MODAL */}
      {selectedAgent && (
        <div
          style={{
            position: 'fixed',
            inset: 0,
            background: 'rgba(0,0,0,0.75)',
            backdropFilter: 'blur(10px)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 100,
          }}
        >
          <div
            style={{
              background: '#0d1229',
              border: '1px solid rgba(0, 240, 255, 0.3)',
              borderRadius: '20px',
              width: '650px',
              maxWidth: '92%',
              height: '560px',
              display: 'flex',
              flexDirection: 'column',
              boxShadow: '0 0 50px rgba(0, 240, 255, 0.25)',
              overflow: 'hidden',
            }}
          >
            {/* Modal Header */}
            <div
              style={{
                padding: '16px 24px',
                borderBottom: '1px solid var(--border-subtle)',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                background: '#0a0d1e',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <div className="emp-avatar">{selectedAgent.name.charAt(0)}</div>
                <div>
                  <h3 style={{ fontSize: '16px', fontWeight: 800, color: '#ffffff' }}>
                    {selectedAgent.name}
                  </h3>
                  <p style={{ fontSize: '12px', color: '#00f0ff' }}>
                    {selectedAgent.role} • Model: {selectedAgent.model_name || 'qwen3.5:4b'}
                  </p>
                </div>
              </div>

              <button
                onClick={() => setSelectedAgent(null)}
                style={{ background: 'transparent', border: 'none', color: '#94a3b8', cursor: 'pointer' }}
              >
                <X size={20} />
              </button>
            </div>

            {/* Modal Body / Chat Messages */}
            <div
              style={{
                flex: 1,
                padding: '20px',
                overflowY: 'auto',
                display: 'flex',
                flexDirection: 'column',
                gap: '12px',
                background: '#070913',
              }}
            >
              <div
                style={{
                  background: 'rgba(0, 240, 255, 0.05)',
                  border: '1px solid rgba(0, 240, 255, 0.2)',
                  borderRadius: '10px',
                  padding: '12px 16px',
                  fontSize: '13px',
                  color: '#94a3b8',
                }}
              >
                Direct link established with <b>{selectedAgent.name}</b> on local GPU. Ask for code, marketing strategy, sales prospecting, or sprint tracking.
              </div>

              {chatHistory.map((item, idx) => (
                <div key={idx} style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                  <div
                    style={{
                      alignSelf: 'flex-end',
                      background: 'linear-gradient(90deg, #2563eb, #6366f1)',
                      color: 'white',
                      padding: '10px 16px',
                      borderRadius: '14px 14px 2px 14px',
                      fontSize: '13.5px',
                      maxWidth: '80%',
                    }}
                  >
                    {item.message}
                  </div>
                  <div
                    style={{
                      alignSelf: 'flex-start',
                      background: '#0d1229',
                      border: '1px solid rgba(0, 240, 255, 0.2)',
                      color: '#e2e8f0',
                      padding: '14px 18px',
                      borderRadius: '14px 14px 14px 2px',
                      fontSize: '13.5px',
                      maxWidth: '88%',
                      whiteSpace: 'pre-wrap',
                      lineHeight: '1.6',
                      fontFamily:
                        selectedAgent.name === 'Forge' || selectedAgent.name === 'Sentinel'
                          ? 'JetBrains Mono, monospace'
                          : 'inherit',
                    }}
                  >
                    {item.reply}
                  </div>
                </div>
              ))}

              {chatSending && (
                <div
                  style={{
                    alignSelf: 'flex-start',
                    background: '#0a0d1e',
                    border: '1px solid rgba(0, 240, 255, 0.3)',
                    color: '#00f0ff',
                    padding: '10px 16px',
                    borderRadius: '12px',
                    fontSize: '13px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                  }}
                >
                  <Sparkles size={14} />
                  <span>{selectedAgent.name} is reasoning on local NVIDIA RTX 4050 GPU...</span>
                </div>
              )}
            </div>

            {/* Suggested Prompt Chips */}
            <div
              style={{
                padding: '8px 20px',
                background: '#0a0d1e',
                borderTop: '1px solid var(--border-subtle)',
                display: 'flex',
                gap: '8px',
                overflowX: 'auto',
              }}
            >
              {selectedAgent.name === 'Forge' && (
                <>
                  <button
                    type="button"
                    onClick={() => setChatMessage('Write a production FastAPI CRUD router for client appointments with PostgreSQL async session')}
                    className="quick-chip"
                  >
                    ⚡ FastAPI Router
                  </button>
                  <button
                    type="button"
                    onClick={() => setChatMessage('Create a responsive React dashboard card component with TypeScript and modern Tailwind styling')}
                    className="quick-chip"
                  >
                    ⚛️ React Component
                  </button>
                </>
              )}
              {selectedAgent.name === 'Hunter' && (
                <>
                  <button
                    type="button"
                    onClick={() => setChatMessage('Extract 5 dental clinics in Chicago from Google Maps and evaluate contract opportunities')}
                    className="quick-chip"
                  >
                    🦷 Chicago Dentists
                  </button>
                  <button
                    type="button"
                    onClick={() => setChatMessage('Draft a high-conversion cold email pitch for local businesses without a website')}
                    className="quick-chip"
                  >
                    ✉️ Cold Email Pitch
                  </button>
                </>
              )}
              {selectedAgent.name === 'Nexus' && (
                <>
                  <button
                    type="button"
                    onClick={() => setChatMessage('Formulate an autonomous company roadmap to acquire our first 10 software clients')}
                    className="quick-chip"
                  >
                    🚀 Growth Roadmap
                  </button>
                  <button
                    type="button"
                    onClick={() => setChatMessage('Delegate technical sprint milestones to Forge, Sentinel, and Atlas')}
                    className="quick-chip"
                  >
                    🎯 Sprint Delegation
                  </button>
                </>
              )}
              {selectedAgent.name === 'Sentinel' && (
                <>
                  <button
                    type="button"
                    onClick={() => setChatMessage('Perform an OWASP Top 10 security audit on our FastAPI endpoints and propose hardening')}
                    className="quick-chip"
                  >
                    🛡️ Security Audit
                  </button>
                </>
              )}
              {selectedAgent.name === 'Echo' && (
                <>
                  <button
                    type="button"
                    onClick={() => setChatMessage('Draft a viral LinkedIn thought leadership post explaining how our AI software agency builds systems 10x faster')}
                    className="quick-chip"
                  >
                    📢 Viral Campaign
                  </button>
                </>
              )}
            </div>

            {/* Modal Input Form */}
            <form
              onSubmit={handleSendAgentChat}
              style={{
                padding: '14px 20px',
                borderTop: '1px solid var(--border-subtle)',
                display: 'flex',
                gap: '12px',
                background: '#0a0d1e',
              }}
            >
              <input
                type="text"
                required
                value={chatMessage}
                onChange={(e) => setChatMessage(e.target.value)}
                placeholder={`Ask ${selectedAgent.name} anything...`}
                style={{
                  flex: 1,
                  background: '#070913',
                  border: '1px solid rgba(255,255,255,0.15)',
                  borderRadius: '10px',
                  padding: '12px 16px',
                  color: 'white',
                  fontSize: '14px',
                  outline: 'none',
                }}
              />
              <button
                type="submit"
                disabled={chatSending}
                className="btn-hq"
                style={{ width: '100px', opacity: chatSending ? 0.6 : 1 }}
              >
                <Send size={15} style={{ marginRight: '6px', verticalAlign: 'middle' }} />
                {chatSending ? '...' : 'Send'}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
