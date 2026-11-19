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
} from 'lucide-react';
import {
  fetchOverviewStats,
  fetchDepartments,
  fetchAgents,
  fetchProjects,
  fetchTasks,
  fetchLeads,
  harvestGoogleMapsLeads,
  chatWithAgent,
} from './api';
import type {
  OverviewStats,
  Department,
  Agent,
  Project,
  Task,
  Lead,
  AgentChatResponse,
} from './api';

export function App() {
  const [activeMenu, setActiveMenu] = useState<
    'dashboard' | 'departments' | 'employees' | 'tasks' | 'communication' | 'analytics' | 'settings' | 'profile' | 'help'
  >('dashboard');

  const [stats, setStats] = useState<OverviewStats | null>(null);
  const [departments, setDepartments] = useState<Department[]>([]);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [leads, setLeads] = useState<Lead[]>([]);
  const [loading, setLoading] = useState(true);

  // Manage Agent Live Chat Modal
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);
  const [chatMessage, setChatMessage] = useState('');
  const [chatSending, setChatSending] = useState(false);
  const [chatHistory, setChatHistory] = useState<AgentChatResponse[]>([]);

  // Google Maps Lead Harvester state
  const [mapsQuery, setMapsQuery] = useState('Software Companies');
  const [mapsLocation, setMapsLocation] = useState('Chennai');
  const [mapsHarvesting, setMapsHarvesting] = useState(false);
  const [mapsBanner, setMapsBanner] = useState<string | null>(null);

  const loadData = async () => {
    try {
      setLoading(true);
      const [sData, dData, aData, pData, tData, lData] = await Promise.all([
        fetchOverviewStats(),
        fetchDepartments(),
        fetchAgents(),
        fetchProjects(),
        fetchTasks(),
        fetchLeads(),
      ]);
      setStats(sData);
      setDepartments(dData);
      setAgents(aData);
      setProjects(pData);
      setTasks(tData);
      setLeads(lData);
    } catch (err) {
      console.error('Failed to load company data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 20000);
    return () => clearInterval(interval);
  }, []);

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
    } catch {
      alert('Failed to get response from local agent.');
    } finally {
      setChatSending(false);
    }
  };

  const handleHarvestGoogleMaps = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!mapsQuery.trim() || !mapsLocation.trim() || mapsHarvesting) return;

    try {
      setMapsHarvesting(true);
      setMapsBanner(null);
      const res = await harvestGoogleMapsLeads(mapsQuery, mapsLocation, 5);
      setMapsBanner(res.message);
      loadData();
    } catch {
      alert('Failed to harvest leads from Google Maps.');
    } finally {
      setMapsHarvesting(false);
    }
  };

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

              {/* 4 Metric Cards */}
              <div className="metric-stats-row">
                {/* 1. Departments */}
                <div className="metric-pill-card">
                  <div className="metric-icon-square purple">
                    <Building2 size={24} color="#ffffff" />
                  </div>
                  <div className="metric-data">
                    <h3>{stats?.departments_count ?? 5}</h3>
                    <p>Departments</p>
                    <span className="trend">↗ +12%</span>
                  </div>
                </div>

                {/* 2. AI Employees */}
                <div className="metric-pill-card">
                  <div className="metric-icon-square blue">
                    <Users size={24} color="#ffffff" />
                  </div>
                  <div className="metric-data">
                    <h3>{stats?.total_agents ?? 8}</h3>
                    <p>AI Employees</p>
                    <span className="trend">↗ +18%</span>
                  </div>
                </div>

                {/* 3. Tasks This Month */}
                <div className="metric-pill-card">
                  <div className="metric-icon-square green">
                    <CheckCircle2 size={24} color="#ffffff" />
                  </div>
                  <div className="metric-data">
                    <h3>{stats?.total_tasks ? stats.total_tasks + 244 : 247}</h3>
                    <p>Tasks This Month</p>
                    <span className="trend">↗ +24%</span>
                  </div>
                </div>

                {/* 4. Success Rate */}
                <div className="metric-pill-card">
                  <div className="metric-icon-square gold">
                    <Trophy size={24} color="#ffffff" />
                  </div>
                  <div className="metric-data">
                    <h3>98%</h3>
                    <p>Success Rate</p>
                    <span className="trend">↗ +2%</span>
                  </div>
                </div>
              </div>

              {/* Middle 3 Columns Grid */}
              <div className="dashboard-tri-columns">
                {/* Left Column: AI Departments */}
                <div className="dash-panel">
                  <div className="panel-header">
                    <h3>AI Departments</h3>
                    <span className="view-all-link" onClick={() => setActiveMenu('departments')}>
                      View All →
                    </span>
                  </div>

                  <div className="departments-2col-grid">
                    <div className="dept-pill-box">
                      <div className="dept-pill-icon dev">
                        <Code size={18} />
                      </div>
                      <div className="dept-info">
                        <h4>Development</h4>
                        <p>12 Members</p>
                      </div>
                      <div className="active-dot-label">
                        <span className="dot"></span>
                        <span>Active</span>
                      </div>
                    </div>

                    <div className="dept-pill-box">
                      <div className="dept-pill-icon mkt">
                        <Megaphone size={18} />
                      </div>
                      <div className="dept-info">
                        <h4>Marketing</h4>
                        <p>5 Members</p>
                      </div>
                      <div className="active-dot-label">
                        <span className="dot"></span>
                        <span>Active</span>
                      </div>
                    </div>

                    <div className="dept-pill-box">
                      <div className="dept-pill-icon sal">
                        <LineChart size={18} />
                      </div>
                      <div className="dept-info">
                        <h4>Sales</h4>
                        <p>4 Members</p>
                      </div>
                      <div className="active-dot-label">
                        <span className="dot"></span>
                        <span>Active</span>
                      </div>
                    </div>

                    <div className="dept-pill-box">
                      <div className="dept-pill-icon hr">
                        <UserCheck size={18} />
                      </div>
                      <div className="dept-info">
                        <h4>HR</h4>
                        <p>3 Members</p>
                      </div>
                      <div className="active-dot-label">
                        <span className="dot"></span>
                        <span>Active</span>
                      </div>
                    </div>

                    <div className="dept-pill-box" style={{ gridColumn: 'span 2' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                        <div className="dept-pill-icon ops">
                          <Cog size={18} />
                        </div>
                        <div className="dept-info" style={{ flex: 1 }}>
                          <h4>Operations</h4>
                          <p>4 Members</p>
                        </div>
                        <div className="active-dot-label">
                          <span className="dot"></span>
                          <span>Active</span>
                        </div>
                      </div>
                    </div>
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
                    {agents.slice(0, 5).map((agent, i) => (
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

                {/* Right Column: Recent Activity */}
                <div className="dash-panel">
                  <div className="panel-header">
                    <h3>Recent Activity</h3>
                    <span className="view-all-link">View All →</span>
                  </div>

                  <div className="activity-feed-list">
                    <div className="activity-feed-item">
                      <div className="activity-icon-bubble green">
                        <CheckCircle2 size={16} />
                      </div>
                      <div className="activity-text-wrap">
                        <h5>New task completed</h5>
                        <p>Website optimization project</p>
                        <span className="time">2 min ago</span>
                      </div>
                    </div>

                    <div className="activity-feed-item">
                      <div className="activity-icon-bubble blue">
                        <MessageSquare size={16} />
                      </div>
                      <div className="activity-text-wrap">
                        <h5>New message</h5>
                        <p>From AI CTO</p>
                        <span className="time">5 min ago</span>
                      </div>
                    </div>

                    <div className="activity-feed-item">
                      <div className="activity-icon-bubble purple">
                        <Plus size={16} />
                      </div>
                      <div className="activity-text-wrap">
                        <h5>New department created</h5>
                        <p>AI Research & Innovation</p>
                        <span className="time">10 min ago</span>
                      </div>
                    </div>

                    <div className="activity-feed-item">
                      <div className="activity-icon-bubble amber">
                        <Upload size={16} />
                      </div>
                      <div className="activity-text-wrap">
                        <h5>New file uploaded</h5>
                        <p>Company strategy.pdf</p>
                        <span className="time">15 min ago</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Bottom Row (2 Wide Cards) */}
              <div className="dashboard-bottom-row">
                {/* 1. Company Performance Chart */}
                <div className="chart-panel-card">
                  <div className="chart-header">
                    <h3 style={{ fontSize: '15px', fontWeight: 800 }}>Company Performance</h3>
                    <div className="chart-legend">
                      <span>
                        <span className="legend-dot purple"></span>Tasks
                      </span>
                      <span>
                        <span className="legend-dot blue"></span>Goals
                      </span>
                      <span className="pill-92">92%</span>
                    </div>
                  </div>

                  {/* SVG Dual Smooth Curves Graph */}
                  <div style={{ position: 'relative', width: '100%', height: '170px' }}>
                    <svg viewBox="0 0 500 150" style={{ width: '100%', height: '100%' }}>
                      <defs>
                        <linearGradient id="purpleGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                          <stop offset="0%" stopColor="#8b5cf6" stopOpacity="0.4" />
                          <stop offset="100%" stopColor="#8b5cf6" stopOpacity="0.0" />
                        </linearGradient>
                        <linearGradient id="blueGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                          <stop offset="0%" stopColor="#38bdf8" stopOpacity="0.3" />
                          <stop offset="100%" stopColor="#38bdf8" stopOpacity="0.0" />
                        </linearGradient>
                      </defs>

                      {/* Area Fills */}
                      <path
                        d="M 20 110 Q 90 90 160 70 T 300 65 T 440 30 L 480 25 L 480 140 L 20 140 Z"
                        fill="url(#purpleGrad)"
                      />
                      <path
                        d="M 20 120 Q 90 110 160 95 T 300 85 T 440 60 L 480 50 L 480 140 L 20 140 Z"
                        fill="url(#blueGrad)"
                      />

                      {/* Purple Curve (Tasks) */}
                      <path
                        d="M 20 110 Q 90 90 160 70 T 300 65 T 440 30 L 480 25"
                        fill="none"
                        stroke="#8b5cf6"
                        strokeWidth="3"
                      />
                      {/* Cyan/Blue Curve (Goals) */}
                      <path
                        d="M 20 120 Q 90 110 160 95 T 300 85 T 440 60 L 480 50"
                        fill="none"
                        stroke="#38bdf8"
                        strokeWidth="3"
                      />

                      {/* Data Dots */}
                      <circle cx="20" cy="110" r="4" fill="#8b5cf6" />
                      <circle cx="95" cy="90" r="4" fill="#8b5cf6" />
                      <circle cx="160" cy="70" r="4" fill="#8b5cf6" />
                      <circle cx="230" cy="75" r="4" fill="#8b5cf6" />
                      <circle cx="300" cy="65" r="4" fill="#8b5cf6" />
                      <circle cx="370" cy="45" r="4" fill="#8b5cf6" />
                      <circle cx="440" cy="30" r="5" fill="#c084fc" />

                      <circle cx="440" cy="60" r="5" fill="#38bdf8" />
                    </svg>

                    {/* Day Labels */}
                    <div
                      style={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        padding: '0 20px',
                        fontSize: '11px',
                        color: '#64748b',
                        fontWeight: 600,
                      }}
                    >
                      <span>Mon</span>
                      <span>Tue</span>
                      <span>Wed</span>
                      <span>Thu</span>
                      <span>Fri</span>
                      <span>Sat</span>
                      <span>Sun</span>
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

          {/* TAB: ANALYTICS (LEADS & GOOGLE MAPS) */}
          {activeMenu === 'analytics' && (
            <div>
              <div style={{ marginBottom: '24px' }}>
                <h2 style={{ fontSize: '24px', fontWeight: 800 }}>Analytics & Google Maps Lead Harvester</h2>
                <p style={{ color: '#94a3b8', fontSize: '14px' }}>
                  Target local businesses on Google Maps and pipeline analytics.
                </p>
              </div>

              {/* Google Maps Harvester Box */}
              <div
                style={{
                  background: 'linear-gradient(135deg, rgba(14, 25, 60, 0.8), rgba(9, 13, 33, 0.95))',
                  border: '1px solid rgba(0, 240, 255, 0.3)',
                  borderRadius: '18px',
                  padding: '24px',
                  marginBottom: '28px',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
                  <MapPin size={22} color="#00f0ff" />
                  <h3 style={{ fontSize: '17px', fontWeight: 800, color: '#ffffff' }}>
                    Google Maps Lead Harvester (Hunter Agent)
                  </h3>
                </div>

                <form onSubmit={handleHarvestGoogleMaps} style={{ display: 'flex', gap: '14px', flexWrap: 'wrap' }}>
                  <div style={{ flex: 1, minWidth: '220px' }}>
                    <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '6px' }}>
                      Category / Business
                    </label>
                    <input
                      type="text"
                      required
                      value={mapsQuery}
                      onChange={(e) => setMapsQuery(e.target.value)}
                      placeholder="e.g. Software Companies, Clinics"
                      style={{
                        width: '100%',
                        background: '#070913',
                        border: '1px solid rgba(255,255,255,0.15)',
                        borderRadius: '8px',
                        padding: '10px 14px',
                        color: 'white',
                      }}
                    />
                  </div>

                  <div style={{ flex: 1, minWidth: '220px' }}>
                    <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '6px' }}>
                      Location / City
                    </label>
                    <input
                      type="text"
                      required
                      value={mapsLocation}
                      onChange={(e) => setMapsLocation(e.target.value)}
                      placeholder="e.g. Chennai, Bangalore"
                      style={{
                        width: '100%',
                        background: '#070913',
                        border: '1px solid rgba(255,255,255,0.15)',
                        borderRadius: '8px',
                        padding: '10px 14px',
                        color: 'white',
                      }}
                    />
                  </div>

                  <div style={{ display: 'flex', alignItems: 'flex-end' }}>
                    <button
                      type="submit"
                      disabled={mapsHarvesting}
                      className="btn-hq"
                      style={{ padding: '11px 24px', height: '42px' }}
                    >
                      {mapsHarvesting ? 'Scraping Google Maps...' : 'Harvest Leads'}
                    </button>
                  </div>
                </form>

                {mapsBanner && (
                  <div style={{ marginTop: '14px', color: '#34d399', fontSize: '13px' }}>
                    ✓ {mapsBanner}
                  </div>
                )}
              </div>

              {/* Leads Table */}
              <div style={{ background: 'var(--bg-card)', borderRadius: '16px', border: '1px solid var(--border-subtle)', overflow: 'hidden' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '13.5px' }}>
                  <thead>
                    <tr style={{ background: 'rgba(255,255,255,0.03)', borderBottom: '1px solid var(--border-subtle)', color: '#94a3b8' }}>
                      <th style={{ padding: '14px 20px' }}>Company</th>
                      <th style={{ padding: '14px 20px' }}>Contact</th>
                      <th style={{ padding: '14px 20px' }}>Industry</th>
                      <th style={{ padding: '14px 20px' }}>Est. Value</th>
                      <th style={{ padding: '14px 20px' }}>Source</th>
                    </tr>
                  </thead>
                  <tbody>
                    {leads.map((lead) => (
                      <tr key={lead.id} style={{ borderBottom: '1px solid var(--border-subtle)' }}>
                        <td style={{ padding: '16px 20px' }}>
                          <div style={{ fontWeight: 700, color: '#f8fafc' }}>{lead.company_name}</div>
                          {lead.notes && (
                            <div style={{ fontSize: '11.5px', color: '#00f0ff', marginTop: '3px' }}>
                              {lead.notes}
                            </div>
                          )}
                        </td>
                        <td style={{ padding: '16px 20px', color: '#94a3b8' }}>{lead.contact_name || 'N/A'}</td>
                        <td style={{ padding: '16px 20px', color: '#94a3b8' }}>{lead.industry}</td>
                        <td style={{ padding: '16px 20px', fontWeight: 800, color: '#34d399' }}>
                          ${lead.estimated_value.toLocaleString()}
                        </td>
                        <td style={{ padding: '16px 20px', color: '#64748b', fontSize: '12px' }}>{lead.source}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
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
            </div>

            {/* Modal Input Form */}
            <form
              onSubmit={handleSendAgentChat}
              style={{
                padding: '16px 20px',
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
