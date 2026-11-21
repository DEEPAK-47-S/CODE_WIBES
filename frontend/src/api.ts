import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8000/api/v1';

export const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 120000,
});

export interface Department {
  id: string;
  name: string;
  slug: string;
  description: string | null;
  is_active: boolean;
  created_at: string;
}

export interface Agent {
  id: string;
  name: string;
  role: string;
  description: string | null;
  department_id: string | null;
  status: 'active' | 'inactive' | 'busy';
  provider: string;
  model_name: string | null;
  capabilities: Record<string, any> | null;
  is_active: boolean;
  created_at: string;
}

export interface Project {
  id: string;
  name: string;
  description: string | null;
  status: string;
  priority: string;
  progress: number;
  start_date: string | null;
  target_date: string | null;
  created_at: string;
}

export interface Task {
  id: string;
  title: string;
  description: string | null;
  status: string;
  priority: string;
  project_id: string | null;
  assigned_agent_id: string | null;
  due_date: string | null;
  created_at: string;
}

export interface Lead {
  id: string;
  company_name: string;
  contact_name: string | null;
  contact_email: string | null;
  industry: string;
  status: string;
  estimated_value: number;
  source: string;
  notes: string | null;
  created_at: string;
}

export interface OverviewStats {
  total_projects: number;
  active_projects: number;
  completed_projects: number;
  total_tasks: number;
  pending_tasks: number;
  completed_tasks: number;
  active_agents: number;
  total_agents: number;
  departments_count: number;
  total_leads: number;
  pipeline_value: number;
}

export interface OwnerCommandResponse {
  command: string;
  executing_agent: string;
  department: string;
  plan_summary: string;
  delegated_tasks: string[];
  agent_reasoning: string;
  status: string;
}

export interface AutonomousSprintResult {
  objective: string;
  project_id: string;
  ceo_plan?: string;
  nexus_plan?: string;
  code_generated?: string;
  lead_acquired?: string;
  tasks_executed?: Array<{
    task_id: string;
    task_title: string;
    status: string;
    assigned_agent: string;
    attempts: number;
    output_preview: string;
    verifier_decision?: string;
  }>;
  status: string;
}

export interface AgentChatResponse {
  agent_id: string;
  agent_name: string;
  role: string;
  model: string;
  message: string;
  reply: string;
}

export interface GoogleMapsHarvestResponse {
  status: string;
  message: string;
  query: string;
  location: string;
  leads_added: any[];
}

export interface ActivityItem {
  id: string;
  title: string;
  subtitle: string;
  time: string;
  type: string;
  details?: Record<string, any>;
}

export const fetchRecentActivity = async (): Promise<ActivityItem[]> => {
  const res = await apiClient.get<ActivityItem[]>('/analytics/activity');
  return res.data;
};

export const fetchOverviewStats = async (): Promise<OverviewStats> => {
  const res = await apiClient.get<OverviewStats>('/analytics/overview');
  return res.data;
};

export const fetchDepartments = async (): Promise<Department[]> => {
  const res = await apiClient.get<Department[]>('/departments');
  return res.data;
};

export const fetchAgents = async (): Promise<Agent[]> => {
  const res = await apiClient.get<Agent[]>('/agents');
  return res.data;
};

export const fetchProjects = async (): Promise<Project[]> => {
  const res = await apiClient.get<Project[]>('/projects');
  return res.data;
};

export const createProject = async (data: Partial<Project>): Promise<Project> => {
  const res = await apiClient.post<Project>('/projects', data);
  return res.data;
};

export const fetchTasks = async (): Promise<Task[]> => {
  const res = await apiClient.get<Task[]>('/tasks');
  return res.data;
};

export const createTask = async (data: Partial<Task>): Promise<Task> => {
  const res = await apiClient.post<Task>('/tasks', data);
  return res.data;
};

export const fetchLeads = async (): Promise<Lead[]> => {
  const res = await apiClient.get<Lead[]>('/leads');
  return res.data;
};

export const createLead = async (data: Partial<Lead>): Promise<Lead> => {
  const res = await apiClient.post<Lead>('/leads', data);
  return res.data;
};

export const harvestGoogleMapsLeads = async (
  query: string,
  location: string,
  count: number = 5,
  minRating: number = 0.0,
  onlyMissingWebsite: boolean = false,
  multiQueries?: string[]
): Promise<GoogleMapsHarvestResponse> => {
  const res = await apiClient.post<GoogleMapsHarvestResponse>('/leads/google-maps-harvest', {
    query,
    location,
    count,
    min_rating: minRating,
    only_missing_website: onlyMissingWebsite,
    multi_queries: multiQueries,
  });
  return res.data;
};

export const exportLeadsCsvUrl = `${API_BASE}/leads/export/csv`;

export const exportLeadsJson = async (): Promise<any[]> => {
  const res = await apiClient.get<any[]>('/leads/export/json');
  return res.data;
};

export const issueOwnerCommand = async (command: string, targetAgent?: string): Promise<OwnerCommandResponse> => {
  const res = await apiClient.post<OwnerCommandResponse>('/owner/command', {
    command,
    target_agent: targetAgent,
  });
  return res.data;
};

export const triggerAutonomousSprint = async (objective: string): Promise<AutonomousSprintResult> => {
  const res = await apiClient.post<AutonomousSprintResult>('/owner/autonomous-sprint', {
    objective,
  });
  return res.data;
};

export const chatWithAgent = async (agentId: string, message: string): Promise<AgentChatResponse> => {
  const res = await apiClient.post<AgentChatResponse>(`/owner/chat/${agentId}`, {
    message,
  });
  return res.data;
};

export interface CompanySettings {
  id: string;
  emergency_pause_all_agents: boolean;
  disable_external_actions: boolean;
  allow_calling_test_mode: boolean;
  allow_production_calling: boolean;
  founder_verified_phone: string | null;
  max_concurrent_models: number;
  daily_call_limit: number;
  monthly_budget_cap_usd: number;
  updated_at: string | null;
}

export interface OrgChartNode {
  id: string;
  name: string;
  role: string;
  model: string | null;
  code?: string;
}

export interface DepartmentNode {
  department_id: string;
  name: string;
  slug: string;
  head: OrgChartNode | null;
  specialists_count: number;
  specialists: OrgChartNode[];
}

export interface OrgChartData {
  founder: string;
  central_manager: OrgChartNode | null;
  total_departments: number;
  total_agents: number;
  departments: DepartmentNode[];
}

export const fetchCompanySettings = async (): Promise<CompanySettings> => {
  const res = await apiClient.get<CompanySettings>('/settings');
  return res.data;
};

export const updateCompanySettings = async (data: Partial<CompanySettings>): Promise<any> => {
  const res = await apiClient.patch('/settings', data);
  return res.data;
};

export const triggerEmergencyPause = async (): Promise<any> => {
  const res = await apiClient.post('/settings/emergency-pause');
  return res.data;
};

export const emergencyPause = triggerEmergencyPause;

export const triggerResumeOperations = async (): Promise<any> => {
  const res = await apiClient.post('/settings/resume');
  return res.data;
};

export const resumeCompany = triggerResumeOperations;

export const fetchOrgChart = async (): Promise<OrgChartData> => {
  const res = await apiClient.get<OrgChartData>('/agents/org-chart');
  return res.data;
};

export const syncFullAgentRoster = async (): Promise<any> => {
  const res = await apiClient.post('/agents/sync-roster');
  return res.data;
};

export interface ApprovalItem {
  id: string;
  task_id: string | null;
  agent_id: string | null;
  action_type: string;
  title: string;
  description: string | null;
  preview_payload: Record<string, any> | null;
  risk_level: string;
  status: string;
  created_at: string | null;
}

export interface ModelItem {
  name: string;
  parameter_size: string | null;
  quantization: string | null;
  advertised_context: number;
  runtime_context: number;
  supports_tools: boolean;
  supports_vision: boolean;
  supports_thinking: boolean;
  supports_json: boolean;
  task_categories: string[];
  latency_ms: number | null;
  tokens_per_sec: number | null;
  benchmark_score: number | null;
  status: string;
  is_enabled: boolean;
}

export interface MemoryItem {
  id: string;
  tier: string;
  namespace: string;
  key: string;
  content: string;
  metadata: Record<string, any> | null;
  provenance: string | null;
  created_at: string | null;
}

export interface ProposalItem {
  id: string;
  brief_id: string;
  title: string;
  scope_summary: string;
  milestones: any[];
  total_cost_inr: number;
  status: string;
  approval_request_id: string | null;
  created_at: string | null;
}

export interface VoiceRecordItem {
  id: string;
  lead_id: string | null;
  phone_masked: string;
  is_test_call: boolean;
  duration: number;
  status: string;
  summary: string | null;
  created_at: string | null;
}

export const fetchPendingApprovals = async (): Promise<ApprovalItem[]> => {
  const res = await apiClient.get<ApprovalItem[]>('/approvals/pending');
  return res.data;
};

export const decideApproval = async (id: string, approved: boolean, feedback?: string): Promise<any> => {
  const res = await apiClient.post(`/approvals/${id}/decide`, { approved, founder_feedback: feedback });
  return res.data;
};

export const fetchRegisteredModels = async (): Promise<ModelItem[]> => {
  const res = await apiClient.get<ModelItem[]>('/models');
  return res.data;
};

export const probeOllamaModels = async (): Promise<any> => {
  const res = await apiClient.post('/models/probe');
  return res.data;
};

export const benchmarkModel = async (modelName: string): Promise<any> => {
  const res = await apiClient.post(`/models/${modelName}/benchmark`);
  return res.data;
};

export const fetchCompanyMemories = async (tier?: string, namespace?: string, q?: string): Promise<MemoryItem[]> => {
  const res = await apiClient.get<MemoryItem[]>('/memory', { params: { tier, namespace, q } });
  return res.data;
};

export const storeCompanyMemory = async (data: { tier: string; namespace: string; key: string; content: string }): Promise<any> => {
  const res = await apiClient.post('/memory', data);
  return res.data;
};

export const fetchProposals = async (): Promise<ProposalItem[]> => {
  const res = await apiClient.get<ProposalItem[]>('/proposals');
  return res.data;
};

export const generateProposal = async (briefId: string, hours: number, rate: number): Promise<any> => {
  const res = await apiClient.post('/proposals/generate', { brief_id: briefId, estimated_hours: hours, rate_per_hour_inr: rate });
  return res.data;
};

export const fetchVoiceRecords = async (): Promise<VoiceRecordItem[]> => {
  const res = await apiClient.get<VoiceRecordItem[]>('/voice/records');
  return res.data;
};

export const executeTestVoiceCall = async (phone: string, purpose: string): Promise<any> => {
  const res = await apiClient.post('/voice/test-call', { phone_number: phone, script_purpose: purpose });
  return res.data;
};

export const enforceLeadOptOut = async (leadId: string, reason?: string): Promise<any> => {
  const res = await apiClient.post(`/voice/opt-out/${leadId}`, {}, { params: { reason } });
  return res.data;
};

export const createWorkspace = async (projectId: string, projectName: string, techStack?: string): Promise<any> => {
  const res = await apiClient.post('/proposals/workspaces/create', { project_id: projectId, project_name: projectName, tech_stack: techStack });
  return res.data;
};

// Powerhouse Interfaces & Functions
export interface ProspectAuditResult {
  id: string;
  target_url: string;
  business_name: string;
  overall_score: number;
  performance_score: number;
  seo_score: number;
  mobile_friendly: boolean;
  ssl_active: boolean;
  issues_found: Array<{ severity: string; issue: string }>;
  proposed_solutions: Array<{ category: string; solution: string }>;
  report_html: string;
}

export const auditProspectWebsite = async (target_url: string, business_name: string): Promise<ProspectAuditResult> => {
  const res = await apiClient.post<ProspectAuditResult>('/prospecting/audit', { target_url, business_name });
  return res.data;
};

export const draftOutreachPitch = async (audit_id: string): Promise<any> => {
  const res = await apiClient.post('/prospecting/outreach/draft', { audit_id });
  return res.data;
};

export const generateFactoryCodebase = async (
  project_id: string,
  project_name: string,
  tech_stack: string = 'React + Tailwind + FastAPI',
  pages?: string[],
  features?: string[]
): Promise<any> => {
  const res = await apiClient.post('/factory/generate', {
    project_id,
    project_name,
    tech_stack,
    pages,
    features,
  });
  return res.data;
};

export interface InvoiceItem {
  id: string;
  invoice_number: string;
  client_name: string;
  total_amount: number;
  subtotal: number;
  gst_amount: number;
  status: string;
  payment_link: string | null;
  due_date: string | null;
  paid_at: string | null;
  created_at: string;
}

export const fetchInvoices = async (): Promise<InvoiceItem[]> => {
  const res = await apiClient.get<InvoiceItem[]>('/billing/invoices');
  return res.data;
};

export const createInvoice = async (data: any): Promise<any> => {
  const res = await apiClient.post('/billing/invoices', data);
  return res.data;
};

export const payInvoice = async (invoice_id: string, payment_reference_id?: string): Promise<any> => {
  const res = await apiClient.post(`/billing/invoices/${invoice_id}/pay`, {
    payment_reference_id: payment_reference_id || 'PAY-DIRECT-ONLINE',
  });
  return res.data;
};

export interface ContractItem {
  id: string;
  contract_number: string;
  client_name: string;
  title: string;
  total_value_inr: number;
  status: string;
  terms_text: string;
  founder_signed_at: string | null;
  created_at: string;
}

export const fetchContracts = async (): Promise<ContractItem[]> => {
  const res = await apiClient.get<ContractItem[]>('/billing/contracts');
  return res.data;
};

export const createContract = async (data: any): Promise<any> => {
  const res = await apiClient.post('/billing/contracts', data);
  return res.data;
};

export const founderSignContract = async (contract_id: string): Promise<any> => {
  const res = await apiClient.post(`/billing/contracts/${contract_id}/sign`);
  return res.data;
};

export interface MarketingPostItem {
  id: string;
  platform: string;
  title: string;
  content_text: string;
  hashtags: string[];
  status: string;
  created_by_agent: string;
  published_at: string | null;
  created_at: string;
}

export const fetchMarketingPosts = async (platform?: string, status?: string): Promise<MarketingPostItem[]> => {
  const res = await apiClient.get<MarketingPostItem[]>('/marketing/posts', { params: { platform, status } });
  return res.data;
};

export const generateMarketingPost = async (platform: string, topic: string, key_insight?: string): Promise<any> => {
  const res = await apiClient.post('/marketing/posts/generate', { platform, topic, key_insight });
  return res.data;
};

export const publishMarketingPost = async (post_id: string): Promise<any> => {
  const res = await apiClient.post(`/marketing/posts/${post_id}/publish`);
  return res.data;
};

export const semanticSearchMemories = async (q: string): Promise<any[]> => {
  const res = await apiClient.get<any[]>('/memory/semantic-search', { params: { q } });
  return res.data;
};

export interface AutopilotResult {
  status: string;
  business_name: string;
  project_id: string;
  lead_id: string;
  audit_score: number;
  staging_preview_url: string;
  invoice_number: string;
  total_inr: number;
  payment_link: string;
  contract_number: string;
  whatsapp_click_to_chat: string;
  pipeline_log: Array<{ stage: string; department: string; agent: string; outcome: string }>;
}

export const runCompanyAutopilot = async (
  business_name: string,
  website_url: string,
  phone?: string,
  location?: string,
  category?: string
): Promise<AutopilotResult> => {
  const res = await apiClient.post<AutopilotResult>('/nexus/autopilot/run', {
    business_name,
    website_url,
    phone,
    location,
    category,
  });
  return res.data;
};

export interface ExecutiveBriefing {
  date: string;
  executive_summary: string;
  financials: {
    total_invoiced_inr: number;
    total_collected_inr: number;
    pending_collection_inr: number;
    invoices_count: number;
    active_msa_contracts: number;
    signed_msa_contracts: number;
  };
  pipeline: {
    total_leads: number;
    new_leads: number;
    contacted_leads: number;
    converted_leads: number;
  };
  production: {
    total_projects: number;
    total_tasks: number;
    active_tasks: number;
  };
  governance: {
    pending_founder_approvals_count: number;
    pending_actions: Array<{ id: string; action_type: string; created_at: string | null }>;
  };
  strategic_priorities: string[];
  generated_by: {
    agent: string;
    role: string;
    department: string;
  };
}

export const fetchExecutiveBriefing = async (): Promise<ExecutiveBriefing> => {
  const res = await apiClient.get<ExecutiveBriefing>('/nexus/briefing');
  return res.data;
};

export interface QAAuditReport {
  project_id: string;
  status: string;
  overall_score: number;
  security_score: number;
  quality_score: number;
  certification: string;
  files_scanned_count: number;
  files_scanned: string[];
  total_lines_of_code: number;
  owasp_top_10_compliant: boolean;
  findings_count: number;
  findings: Array<{ severity: string; category: string; file: string; description: string }>;
  audited_by_departments: Array<{ department: string; name: string; agent: string }>;
  recommendations: string[];
}

export const fetchProjectQAAudit = async (projectId: string): Promise<QAAuditReport> => {
  const res = await apiClient.get<QAAuditReport>(`/factory/audit/${projectId}`);
  return res.data;
};

export const runProjectQAAudit = async (projectId: string): Promise<QAAuditReport> => {
  const res = await apiClient.post<QAAuditReport>(`/factory/audit/${projectId}`);
  return res.data;
};

export interface ClientPortalData {
  project: {
    id: string;
    name: string;
    description: string;
    status: string;
    created_at: string;
    staging_url: string;
    download_zip_url: string;
  };
  qa_certification: {
    certification: string;
    overall_score: number;
    owasp_compliant: boolean;
    findings_count: number;
  };
  invoices: Array<{
    id: string;
    invoice_number: string;
    total_amount: number;
    status: string;
    due_date: string;
    payment_link: string;
    print_url: string;
  }>;
  contracts: Array<{
    id: string;
    contract_number: string;
    title: string;
    total_value_inr: number;
    status: string;
    founder_signed: boolean;
    print_url: string;
  }>;
  change_requests: Array<{
    id: string;
    title: string;
    description: string;
    status: string;
    priority: string;
    estimated_hours: number;
    created_at: string;
  }>;
}

export const fetchClientPortalData = async (projectId: string): Promise<ClientPortalData> => {
  const res = await apiClient.get<ClientPortalData>(`/client-portal/${projectId}`);
  return res.data;
};

export const submitClientChangeRequest = async (
  projectId: string,
  data: { title: string; description: string; priority?: string }
): Promise<any> => {
  const res = await apiClient.post(`/client-portal/${projectId}/change-request`, data);
  return res.data;
};




