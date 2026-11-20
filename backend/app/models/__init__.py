"""Database models package — import all models here for Alembic discovery."""
from app.models.user import User
from app.models.department import Department
from app.models.agent import Agent
from app.models.project import Project
from app.models.task import Task
from app.models.activity_log import ActivityLog
from app.models.lead import Lead
from app.models.company_setting import CompanySetting
from app.models.model_registry import ModelRegistry
from app.models.memory import CompanyMemory, TaskCheckpoint
from app.models.approval import ApprovalRequest, TaskDependency
from app.models.voice_call import VoiceCallRecord
from app.models.proposal import CustomerRequirementBrief, ProposalDraft
from app.models.change_request import ChangeRequest

__all__ = [
    "User",
    "Department",
    "Agent",
    "Project",
    "Task",
    "ActivityLog",
    "Lead",
    "CompanySetting",
    "ModelRegistry",
    "CompanyMemory",
    "TaskCheckpoint",
    "ApprovalRequest",
    "TaskDependency",
    "VoiceCallRecord",
    "CustomerRequirementBrief",
    "ProposalDraft",
    "ChangeRequest",
]
