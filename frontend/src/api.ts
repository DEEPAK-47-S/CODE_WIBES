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
  ceo_plan: string;
  code_generated: string;
  lead_acquired: string;
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
  leads_added: Partial<Lead>[];
}

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
  count: number = 5
): Promise<GoogleMapsHarvestResponse> => {
  const res = await apiClient.post<GoogleMapsHarvestResponse>('/leads/google-maps-harvest', {
    query,
    location,
    count,
  });
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
