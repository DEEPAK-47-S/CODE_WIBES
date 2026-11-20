"""Database models package — import all models here for Alembic discovery."""
from app.models.user import User
from app.models.department import Department
from app.models.agent import Agent
from app.models.project import Project
from app.models.task import Task
from app.models.activity_log import ActivityLog
from app.models.lead import Lead
from app.models.company_setting import CompanySetting

__all__ = [
    "User",
    "Department",
    "Agent",
    "Project",
    "Task",
    "ActivityLog",
    "Lead",
    "CompanySetting",
]
