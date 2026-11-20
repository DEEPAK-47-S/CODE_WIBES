"""Service layer for CODE WIBES company operations."""
import uuid
from typing import List, Optional
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.department import Department
from app.models.agent import Agent
from app.models.project import Project
from app.models.task import Task
from app.models.lead import Lead
from app.models.activity_log import ActivityLog
from app.schemas.schemas import (
    DepartmentCreate,
    AgentCreate,
    ProjectCreate,
    TaskCreate,
    LeadCreate,
    OverviewStats,
)


class CompanyService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def seed_initial_company(self) -> None:
        """Seed complete company: 6 departments, full AI agent roster, initial CRM leads, and software projects."""
        dept_check = await self.db.execute(select(func.count(Department.id)))
        if dept_check.scalar_one() > 0:
            # Check if leads exist
            lead_check = await self.db.execute(select(func.count(Lead.id)))
            if lead_check.scalar_one() == 0:
                await self._seed_leads()
            return

        # 1. Company Departments
        departments_data = [
            {
                "name": "Software Development",
                "slug": "software-development",
                "description": "Full-stack web applications, REST APIs, database design, and cloud software engineering.",
            },
            {
                "name": "Lead Generation & Sales",
                "slug": "lead-generation-sales",
                "description": "B2B client acquisition, prospect scraping, automated outreach pipelines, and deal closing.",
            },
            {
                "name": "Digital Marketing",
                "slug": "digital-marketing",
                "description": "Growth marketing, SEO, social media authority, conversion ad campaigns, and brand storytelling.",
            },
            {
                "name": "UI/UX & Creative",
                "slug": "ui-ux-creative",
                "description": "SaaS design systems, mobile/web wireframes, Figma prototypes, and branding assets.",
            },
            {
                "name": "Testing & Quality Assurance",
                "slug": "testing-qa",
                "description": "Automated regression testing, API security audits, load testing, and zero-defect QA.",
            },
            {
                "name": "Business Operations & Management",
                "slug": "business-operations",
                "description": "Executive strategy, human-owner reporting, resource tracking, sprint velocity, and delivery.",
            },
        ]

        created_depts = {}
        for d in departments_data:
            dept = Department(**d)
            self.db.add(dept)
            created_depts[d["slug"]] = dept

        await self.db.flush()

        # 2. Complete AI Agent Employees for Every Department
        agents_data = [
            {
                "name": "Nexus",
                "role": "Chief Executive Officer (CEO)",
                "description": "Master AI executive. Receives directives from Human Owner, formulates company strategy, and delegates to all department agents.",
                "department_id": created_depts["business-operations"].id,
                "status": "active",
                "provider": "local",
                "model_name": "qwen3.5:4b",
                "capabilities": {"executive_planning": True, "task_delegation": True, "owner_reporting": True},
            },
            {
                "name": "Hunter",
                "role": "Lead Generation & B2B Sales Specialist",
                "description": "Identifies high-value enterprise leads, drafts custom cold pitches, enriches prospect data, and fills the client CRM pipeline.",
                "department_id": created_depts["lead-generation-sales"].id,
                "status": "active",
                "provider": "local",
                "model_name": "qwen3.5:4b",
                "capabilities": {"prospecting": True, "lead_enrichment": True, "sales_pitches": True},
            },
            {
                "name": "Echo",
                "role": "Head of Digital Marketing",
                "description": "Creates viral social media campaigns, SEO keyword architectures, blog copy, and conversion funnels.",
                "department_id": created_depts["digital-marketing"].id,
                "status": "active",
                "provider": "local",
                "model_name": "qwen3.5:4b",
                "capabilities": {"seo": True, "content_strategy": True, "campaign_management": True},
            },
            {
                "name": "Forge",
                "role": "Lead Full-Stack Software Engineer",
                "description": "Writes production-grade Python FastAPI backends, React TypeScript frontends, PostgreSQL migrations, and microservices.",
                "department_id": created_depts["software-development"].id,
                "status": "active",
                "provider": "local",
                "model_name": "qwen3.5:4b",
                "capabilities": {"code_generation": True, "architecture": True, "database_design": True},
            },
            {
                "name": "Aura",
                "role": "Principal UI/UX Designer",
                "description": "Crafts modern, accessible SaaS UI designs, responsive layouts, color systems, and interactive component libraries.",
                "department_id": created_depts["ui-ux-creative"].id,
                "status": "active",
                "provider": "local",
                "model_name": "qwen3.5:4b",
                "capabilities": {"wireframing": True, "design_systems": True, "user_journeys": True},
            },
            {
                "name": "Atlas",
                "role": "Senior Technical Project Manager",
                "description": "Organizes projects into sprints, creates backlog tasks, enforces timeline milestones, and eliminates delivery bottlenecks.",
                "department_id": created_depts["business-operations"].id,
                "status": "active",
                "provider": "local",
                "model_name": "qwen3.5:4b",
                "capabilities": {"sprint_planning": True, "dependency_management": True},
            },
            {
                "name": "Sentinel",
                "role": "Lead QA & Security Auditor",
                "description": "Verifies test coverage, audits code against SQL injection/XSS, executes automated integration tests, and signs off releases.",
                "department_id": created_depts["testing-qa"].id,
                "status": "active",
                "provider": "local",
                "model_name": "qwen3.5:4b",
                "capabilities": {"security_auditing": True, "test_automation": True, "vulnerability_scan": True},
            },
            {
                "name": "Ledger",
                "role": "Operations & Finance Coordinator",
                "description": "Monitors API compute budgets, tracks company billables, calculates gross margins, and reports company health to Owner.",
                "department_id": created_depts["business-operations"].id,
                "status": "active",
                "provider": "local",
                "model_name": "qwen3.5:4b",
                "capabilities": {"budgeting": True, "analytics": True, "invoicing": True},
            },
        ]

        for a in agents_data:
            agent = Agent(**a)
            self.db.add(agent)

        # 3. Initial Software Projects
        p1 = Project(
            name="CODE WIBES Autonomous Company Platform",
            description="Core multi-agent operating system coordinating all 8 departments under human owner leadership.",
            status="in_progress",
            priority="critical",
            progress=65,
        )
        p2 = Project(
            name="Enterprise AI Client Acquisition Portal",
            description="Automated inbound lead capture and AI demo scheduling platform for external software clients.",
            status="in_progress",
            priority="high",
            progress=30,
        )
        self.db.add_all([p1, p2])
        await self.db.flush()

        # 4. Tasks
        tasks_data = [
            Task(
                title="Orchestrate Lead Hunter Agent with B2B Scraper",
                description="Equip Hunter Agent with target industry search parameters for Software and Healthcare clients.",
                status="in_progress",
                priority="high",
                project_id=p2.id,
            ),
            Task(
                title="Launch Owner Executive Command Console",
                description="Enable Deepak (Owner) to direct CEO Nexus with real-time natural language commands.",
                status="completed",
                priority="critical",
                project_id=p1.id,
            ),
            Task(
                title="Draft 30-Day LinkedIn & Twitter AI Growth Campaign",
                description="Assigned to Echo (Marketing Agent) to establish CODE WIBES authority in AI Software engineering.",
                status="pending",
                priority="medium",
                project_id=p2.id,
            ),
        ]
        self.db.add_all(tasks_data)

        # 5. Seed CRM Leads
        await self._seed_leads()

        log = ActivityLog(
            actor_type="system",
            action="COMPANY_ACTIVATED",
            resource_type="company",
            details={"message": "All 8 AI Department Agents activated for Human Owner Deepak."},
        )
        self.db.add(log)
        await self.db.commit()

    async def _seed_leads(self) -> None:
        """Leads are generated dynamically by Hunter Agent and Google Maps Harvester."""
        pass
        await self.db.commit()

    # Department operations
    async def get_departments(self, active_only: bool = True) -> List[Department]:
        query = select(Department)
        if active_only:
            query = query.where(Department.is_active.is_(True))
        result = await self.db.execute(query.order_by(Department.slug))
        return list(result.scalars().all())

    async def sync_full_organization(self) -> dict:
        """Synchronize the 10 canonical departments and exactly 100 AI role profiles + NEXUS."""
        from app.agents.catalog import DEPARTMENTS_CATALOG, build_full_agent_roster

        # 1. Sync 10 Canonical Departments
        dept_map = {}
        for d_info in DEPARTMENTS_CATALOG:
            res = await self.db.execute(
                select(Department).where(
                    (Department.slug == d_info["slug"]) | (Department.name == d_info["name"])
                )
            )
            dept = res.scalar_one_or_none()
            if not dept:
                dept = Department(
                    name=d_info["name"],
                    slug=d_info["slug"],
                    description=d_info["description"],
                )
                self.db.add(dept)
                await self.db.flush()
            else:
                dept.name = d_info["name"]
                dept.slug = d_info["slug"]
                dept.description = d_info["description"]
            dept_map[d_info["code"]] = dept

        # 2. Sync Full Agent Roster (100 departmental profiles + NEXUS)
        roster = build_full_agent_roster()
        synced_count = 0
        for p in roster:
            dept = dept_map.get(p.get("department_code"))
            dept_id = dept.id if dept else None

            res = await self.db.execute(select(Agent).where(Agent.name == p["name"]))
            agent = res.scalar_one_or_none()
            if not agent:
                agent = Agent(
                    name=p["name"],
                    role=p["role"],
                    description=p["system_instructions"][:200],
                    department_id=dept_id,
                    status="active",
                    provider="local",
                    model_name=p["model_preference"],
                    capabilities=p,
                    is_active=True,
                )
                self.db.add(agent)
            else:
                agent.role = p["role"]
                agent.model_name = p["model_preference"]
                if dept_id:
                    agent.department_id = dept_id
                agent.capabilities = p
                agent.is_active = True
                agent.status = "active"
            synced_count += 1

        await self.db.commit()
        return {
            "departments_count": len(DEPARTMENTS_CATALOG),
            "agents_synced": synced_count,
            "status": "success",
        }

    async def get_org_chart(self) -> dict:
        """Return the hierarchical org chart: Founder -> NEXUS -> 10 Dept Heads -> Specialists."""
        depts = await self.get_departments()
        agents = await self.get_agents()

        nexus = next((a for a in agents if a.name.lower() == "nexus"), None)

        departments_tree = []
        for d in depts:
            dept_agents = [a for a in agents if a.department_id == d.id]
            head = next((a for a in dept_agents if (a.capabilities or {}).get("is_head", False)), None)
            specialists = [a for a in dept_agents if a != head]
            departments_tree.append({
                "department_id": str(d.id),
                "name": d.name,
                "slug": d.slug,
                "head": {
                    "id": str(head.id),
                    "name": head.name,
                    "role": head.role,
                    "model": head.model_name,
                } if head else None,
                "specialists_count": len(specialists),
                "specialists": [
                    {
                        "id": str(s.id),
                        "name": s.name,
                        "role": s.role,
                        "model": s.model_name,
                        "code": (s.capabilities or {}).get("code"),
                    }
                    for s in specialists
                ],
            })

        return {
            "founder": "Founder / Owner (Human Final Authority)",
            "central_manager": {
                "id": str(nexus.id) if nexus else None,
                "name": "Nexus",
                "role": "Chief of Staff & Central AI Manager",
                "model": nexus.model_name if nexus else "qwen3.5:4b",
            } if nexus else None,
            "total_departments": len(departments_tree),
            "total_agents": len(agents),
            "departments": departments_tree,
        }

    # Agent operations
    async def get_agents(self) -> List[Agent]:
        result = await self.db.execute(select(Agent).order_by(Agent.name))
        return list(result.scalars().all())

    async def create_agent(self, data: AgentCreate) -> Agent:
        agent = Agent(**data.model_dump())
        self.db.add(agent)
        await self.db.commit()
        await self.db.refresh(agent)
        return agent

    # Project operations
    async def get_projects(self) -> List[Project]:
        result = await self.db.execute(select(Project).order_by(Project.created_at.desc()))
        return list(result.scalars().all())

    async def create_project(self, data: ProjectCreate) -> Project:
        project = Project(**data.model_dump())
        self.db.add(project)
        await self.db.commit()
        await self.db.refresh(project)
        return project

    # Task operations
    async def get_tasks(self, project_id: Optional[uuid.UUID] = None) -> List[Task]:
        query = select(Task)
        if project_id:
            query = query.where(Task.project_id == project_id)
        query = query.order_by(Task.created_at.desc())
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def create_task(self, data: TaskCreate) -> Task:
        task = Task(**data.model_dump())
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    # Lead operations
    async def get_leads(self) -> List[Lead]:
        result = await self.db.execute(select(Lead).order_by(Lead.created_at.desc()))
        return list(result.scalars().all())

    async def create_lead(self, data: LeadCreate) -> Lead:
        lead = Lead(**data.model_dump())
        self.db.add(lead)
        await self.db.commit()
        await self.db.refresh(lead)
        return lead

    # Overview statistics
    async def get_overview_stats(self) -> OverviewStats:
        total_projects = (await self.db.execute(select(func.count(Project.id)))).scalar_one()
        active_projects = (await self.db.execute(select(func.count(Project.id)).where(Project.status == "in_progress"))).scalar_one()
        completed_projects = (await self.db.execute(select(func.count(Project.id)).where(Project.status == "completed"))).scalar_one()

        total_tasks = (await self.db.execute(select(func.count(Task.id)))).scalar_one()
        pending_tasks = (await self.db.execute(select(func.count(Task.id)).where(Task.status.in_(["pending", "in_progress"])))).scalar_one()
        completed_tasks = (await self.db.execute(select(func.count(Task.id)).where(Task.status == "completed"))).scalar_one()

        total_agents = (await self.db.execute(select(func.count(Agent.id)))).scalar_one()
        active_agents = (await self.db.execute(select(func.count(Agent.id)).where(Agent.status == "active"))).scalar_one()

        dept_count = (await self.db.execute(select(func.count(Department.id)))).scalar_one()

        total_leads = (await self.db.execute(select(func.count(Lead.id)))).scalar_one()
        pipeline_sum = (await self.db.execute(select(func.coalesce(func.sum(Lead.estimated_value), 0.0)))).scalar_one()

        return OverviewStats(
            total_projects=total_projects,
            active_projects=active_projects,
            completed_projects=completed_projects,
            total_tasks=total_tasks,
            pending_tasks=pending_tasks,
            completed_tasks=completed_tasks,
            active_agents=active_agents,
            total_agents=total_agents,
            departments_count=dept_count,
            total_leads=total_leads,
            pipeline_value=float(pipeline_sum),
        )
