"""Pydantic schemas for CODE WIBES."""
import uuid
from datetime import datetime
from typing import Any, Optional, List
from pydantic import BaseModel, ConfigDict, Field


# Base Schema
class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# Department Schemas
class DepartmentBase(BaseSchema):
    name: str
    slug: str
    description: Optional[str] = None
    is_active: bool = True


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentRead(DepartmentBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


# Agent Schemas
class AgentBase(BaseSchema):
    name: str
    role: str
    description: Optional[str] = None
    department_id: Optional[uuid.UUID] = None
    status: str = "active"
    provider: str = "local"
    model_name: Optional[str] = None
    capabilities: Optional[dict[str, Any]] = None
    is_active: bool = True


class AgentCreate(AgentBase):
    pass


class AgentRead(AgentBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


# Project Schemas
class ProjectBase(BaseSchema):
    name: str
    description: Optional[str] = None
    status: str = "in_progress"
    priority: str = "medium"
    progress: int = Field(default=0, ge=0, le=100)
    start_date: Optional[datetime] = None
    target_date: Optional[datetime] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectRead(ProjectBase):
    id: uuid.UUID
    owner_id: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime


# Task Schemas
class TaskBase(BaseSchema):
    title: str
    description: Optional[str] = None
    status: str = "pending"
    priority: str = "medium"
    project_id: Optional[uuid.UUID] = None
    assigned_agent_id: Optional[uuid.UUID] = None
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: uuid.UUID
    assigned_user_id: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime


# Lead / CRM Schemas
class LeadBase(BaseSchema):
    company_name: str
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    industry: str = "Technology"
    status: str = "new"
    estimated_value: float = 0.0
    source: str = "AI Lead Scraping"
    notes: Optional[str] = None


class LeadCreate(LeadBase):
    pass


class LeadRead(LeadBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


# Owner Command Schemas
class OwnerCommandRequest(BaseModel):
    command: str
    target_agent: Optional[str] = None  # None = CEO by default


class OwnerCommandResponse(BaseModel):
    command: str
    executing_agent: str
    department: str
    plan_summary: str
    delegated_tasks: List[str]
    agent_reasoning: str
    status: str


# Analytics / Stats Schema
class OverviewStats(BaseSchema):
    total_projects: int
    active_projects: int
    completed_projects: int
    total_tasks: int
    pending_tasks: int
    completed_tasks: int
    active_agents: int
    total_agents: int
    departments_count: int
    total_leads: int
    pipeline_value: float
