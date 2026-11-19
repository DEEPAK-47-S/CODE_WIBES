"""API v1 Owner Executive Command Center & Autonomous Multi-Agent Cascade."""
import uuid
from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.session import get_db
from app.models.agent import Agent
from app.models.task import Task
from app.schemas.schemas import OwnerCommandRequest, OwnerCommandResponse
from app.services.agent_runtime import AgentRuntimeService

router = APIRouter(prefix="/owner", tags=["owner"])


class AgentChatRequest(BaseModel):
    message: str


class AgentChatResponse(BaseModel):
    agent_id: str
    agent_name: str
    role: str
    model: str
    message: str
    reply: str


class AutonomousSprintRequest(BaseModel):
    objective: str


@router.post("/command", response_model=OwnerCommandResponse)
async def execute_owner_command(
    req: OwnerCommandRequest,
    db: AsyncSession = Depends(get_db),
):
    """Deepak (Human Owner) issues a directive to a specific AI employee."""
    target_name = req.target_agent or "Nexus"
    result = await db.execute(select(Agent).where(Agent.name.ilike(f"%{target_name}%")))
    agent = result.scalar_one_or_none()

    if not agent:
        agent_res = await db.execute(select(Agent).limit(1))
        agent = agent_res.scalar_one_or_none()

    if not agent:
        raise HTTPException(status_code=404, detail="No AI agent found.")

    runtime = AgentRuntimeService(db)
    prompt = (
        f"DIRECTIVE FROM HUMAN OWNER DEEPAK: '{req.command}'.\n"
        f"Analyze this directive, establish an actionable execution plan, "
        f"and provide your immediate professional output."
    )
    exec_res = await runtime.execute_agent_task(agent_id=agent.id, prompt=prompt)

    # Spawn task in DB
    new_task = Task(
        title=f"Directive: {req.command[:60]}",
        description=f"Direct command executed by {agent.name}.",
        status="in_progress",
        priority="critical",
        assigned_agent_id=agent.id,
    )
    db.add(new_task)
    await db.commit()

    return OwnerCommandResponse(
        command=req.command,
        executing_agent=agent.name,
        department=agent.role,
        plan_summary=f"Processed by {agent.name} using local Ollama.",
        delegated_tasks=[f"Task #{new_task.title}", "Verification Active"],
        agent_reasoning=exec_res["response"],
        status="EXECUTING",
    )


@router.post("/autonomous-sprint")
async def run_autonomous_sprint(
    req: AutonomousSprintRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Launch an autonomous company-wide sprint:
    CEO Nexus plans -> Hunter finds clients -> Forge codes -> Sentinel audits.
    """
    runtime = AgentRuntimeService(db)
    result = await runtime.run_autonomous_company_sprint(req.objective)
    return result


@router.post("/chat/{agent_id}", response_model=AgentChatResponse)
async def chat_with_agent(
    agent_id: uuid.UUID,
    req: AgentChatRequest,
    db: AsyncSession = Depends(get_db),
):
    """Live 1-on-1 conversation between Deepak (Owner) and any specific AI Employee."""
    result = await db.execute(select(Agent).where(Agent.id == agent_id))
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    runtime = AgentRuntimeService(db)
    exec_res = await runtime.execute_agent_task(agent_id=agent.id, prompt=req.message)

    return AgentChatResponse(
        agent_id=str(agent.id),
        agent_name=agent.name,
        role=agent.role,
        model=exec_res["model"],
        message=req.message,
        reply=exec_res["response"],
    )
