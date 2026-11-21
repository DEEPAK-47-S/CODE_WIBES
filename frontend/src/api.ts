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


