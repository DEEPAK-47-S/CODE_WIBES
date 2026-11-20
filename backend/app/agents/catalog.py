"""Canonical catalog of the 10 departments and 100 departmental AI employee profiles + NEXUS."""
from typing import Any, Dict, List

# 10 Canonical Departments
DEPARTMENTS_CATALOG: List[Dict[str, str]] = [
    {
        "code": "D01",
        "name": "Executive Operations & Governance",
        "slug": "d01-operations-governance",
        "description": "Company policy enforcement, compliance research, audit logging, finance tracking, and resource planning.",
    },
    {
        "code": "D02",
        "name": "Market Research & Lead Intelligence",
        "slug": "d02-lead-intelligence",
        "description": "Territory discovery, official Google Places API research, website auditing, and lead qualification.",
    },
    {
        "code": "D03",
        "name": "Sales, Customer Relations & Voice",
        "slug": "d03-sales-voice",
        "description": "Outreach campaign planning, ElevenLabs voice coordination, meeting scheduling, and opt-out suppression.",
    },
    {
        "code": "D04",
        "name": "Customer Discovery & Solution Architecture",
        "slug": "d04-discovery-solutions",
        "description": "Client requirements capture, business analysis, solution architecture, scope writing, and effort estimation.",
    },
    {
        "code": "D05",
        "name": "UI/UX & Brand Design",
        "slug": "d05-ui-ux-design",
        "description": "Design systems, brand identity, visual interfaces, responsive layouts, and accessibility guidelines.",
    },
    {
        "code": "D06",
        "name": "Software Engineering",
        "slug": "d06-software-engineering",
        "description": "Production Python FastAPI backends, async PostgreSQL architectures, React/TypeScript frontends, and integrations.",
    },
    {
        "code": "D07",
        "name": "Quality Assurance & Security",
        "slug": "d07-qa-security",
        "description": "Functional testing, contract testing, security audits, OWASP Top 10 prevention, and release verification.",
    },
    {
        "code": "D08",
        "name": "DevOps, Deployment & Reliability",
        "slug": "d08-devops-reliability",
        "description": "CI/CD automation, domain/SSL management, health monitoring, backups, and rollback orchestration.",
    },
    {
        "code": "D09",
        "name": "Marketing & Growth",
        "slug": "d09-marketing-growth",
        "description": "SEO research, content strategy, brand consistency, portfolio showcases, and growth analytics.",
    },
    {
        "code": "D10",
        "name": "Customer Success & Support",
        "slug": "d10-customer-success",
        "description": "Customer onboarding, issue triage, change request management, feedback synthesis, and retention.",
    },
]

# NEXUS Central System Agent Definition
NEXUS_PROFILE: Dict[str, Any] = {
    "code": "NEXUS-00",
    "name": "Nexus",
    "role": "Chief of Staff & Central AI Manager",
    "department_code": "CENTRAL",
    "is_head": True,
    "reports_to": "FOUNDER",
    "model_preference": "qwen3.5:4b",
    "fallback_models": ["llama3.1:latest", "phi4-mini:latest"],
    "system_instructions": (
        "You are Nexus, Chief of Staff and Central AI Manager at CODE WIBES TECHNOLOGIES. "
        "You report directly to the Founder / Owner (human). You translate business directives "
        "into structured departmental tasks, coordinate the 10 Department Heads, track dependencies "
        "and progress, and enforce the Founder approval policy. You never execute consequential external "
        "actions without explicit human approval."
    ),
    "tool_allowlist": ["task_delegate", "task_inspect", "approval_request", "memory_query"],
    "approval_mode": "FOUNDER_APPROVAL",
    "context_budget": 8192,
}

# Specification of 10 Profiles per Department (1 Head + 9 Specialists)
DEPARTMENT_ROLES: Dict[str, List[Dict[str, Any]]] = {
    "D01": [
        {"role": "Operations Director / Department Head", "name": "Vanguard", "is_head": True, "model": "granite4.2:3b"},
        {"role": "Executive Assistant Agent", "name": "Clio", "is_head": False, "model": "qwen3.5:2b"},
        {"role": "Policy & Approval Coordinator", "name": "Arbiter", "is_head": False, "model": "granite4.2:3b"},
        {"role": "Finance Analyst (Ledger)", "name": "Ledger", "is_head": False, "model": "qwen3.5:2b"},
        {"role": "Legal & Compliance Research Assistant", "name": "Justiciar", "is_head": False, "model": "granite4.2:3b"},
        {"role": "Open-Source License & Vendor Review Agent", "name": "LicenseGuard", "is_head": False, "model": "qwen3.5:2b"},
        {"role": "Resource & Capacity Planner", "name": "Chronos", "is_head": False, "model": "granite4.2:3b"},
        {"role": "KPI & Management Reporting Agent", "name": "Metricon", "is_head": False, "model": "qwen3.5:2b"},
        {"role": "Internal Audit & Data Governance Agent", "name": "AuditorPrime", "is_head": False, "model": "granite4.2:3b"},
        {"role": "Knowledge & Company Memory Manager", "name": "Mnemosyne", "is_head": False, "model": "qwen3.5:4b"},
    ],
    "D02": [
        {"role": "Head of Market Intelligence (Hunter)", "name": "Hunter", "is_head": True, "model": "llama3.1:latest"},
        {"role": "Territory Planner", "name": "Cartographer", "is_head": False, "model": "qwen3.5:2b"},
        {"role": "District & Weekly Campaign Scheduler", "name": "Cadence", "is_head": False, "model": "qwen3.5:2b"},
        {"role": "Google Places API Research Agent", "name": "PlaceScout", "is_head": False, "model": "qwen3.5:2b"},
        {"role": "Business Website Research Agent", "name": "WebAudit", "is_head": False, "model": "qwen3.5:2b"},
        {"role": "Business Data Verification Agent", "name": "Veritas", "is_head": False, "model": "qwen3.5:2b"},
        {"role": "Lead Qualification & Scoring Agent", "name": "ScoreCraft", "is_head": False, "model": "granite4.2:3b"},
        {"role": "Deduplication & Data Quality Agent", "name": "DeDuper", "is_head": False, "model": "qwen3.5:2b"},
        {"role": "Industry / Competitor Research Agent", "name": "Insight", "is_head": False, "model": "qwen3.5:4b"},
        {"role": "Source Provenance & Consent Evidence Steward", "name": "Provenance", "is_head": False, "model": "granite4.2:3b"},
    ],
    "D03": [
        {"role": "Sales Director / Department Head", "name": "Venture", "is_head": True, "model": "llama3.1:latest"},
        {"role": "Outreach Campaign Planner", "name": "Strategos", "is_head": False, "model": "qwen3.5:4b"},
        {"role": "Voice Agent Supervisor", "name": "Vocalis", "is_head": False, "model": "phi4-mini:latest"},
        {"role": "ElevenLabs Voice Conversation Agent", "name": "AriaVoice", "is_head": False, "model": "llama3.1:latest"},
        {"role": "Lead Qualification & Call Summary Agent", "name": "Transcribe", "is_head": False, "model": "qwen3.5:2b"},
        {"role": "CRM Sales Coordinator", "name": "NexusCRM", "is_head": False, "model": "qwen3.5:2b"},
        {"role": "Follow-up Planner", "name": "Persist", "is_head": False, "model": "qwen3.5:2b"},
        {"role": "Objection & FAQ Research Agent", "name": "Resolve", "is_head": False, "model": "qwen3.5:4b"},
        {"role": "Meeting / Callback Scheduler", "name": "Calenda", "is_head": False, "model": "qwen3.5:2b"},
        {"role": "Consent, Suppression & Opt-out Enforcement Agent", "name": "OptOutSentry", "is_head": False, "model": "granite4.2:3b"},
    ],
    "D04": [
        {"role": "Discovery & Solutions Head (Atlas)", "name": "Atlas", "is_head": True, "model": "qwen3.5:4b"},
        {"role": "Requirements Interviewer", "name": "Inquirer", "is_head": False, "model": "qwen3.5:4b"},
        {"role": "Business Analyst", "name": "AnalystPrime", "is_head": False, "model": "granite4.2:3b"},
        {"role": "UX Research Agent", "name": "Empathy", "is_head": False, "model": "gemma3:4b"},
        {"role": "Solution Architect", "name": "Synthesize", "is_head": False, "model": "qwen2.5-coder:3b"},
        {"role": "Scope & Acceptance Criteria Writer", "name": "ScopeGuard", "is_head": False, "model": "granite4.2:3b"},
        {"role": "Effort / Estimate Drafting Agent", "name": "Estimator", "is_head": False, "model": "qwen3.5:2b"},
        {"role": "Delivery Timeline Planner", "name": "Gantt", "is_head": False, "model": "granite4.2:3b"},
        {"role": "Project Risk Analyst", "name": "RiskEngine", "is_head": False, "model": "granite4.2:3b"},
        {"role": "Customer Brief & Documentation Agent", "name": "BriefCraft", "is_head": False, "model": "qwen3.5:2b"},
    ],
    "D05": [
        {"role": "Design Director / Department Head (Aura)", "name": "Aura", "is_head": True, "model": "gemma3:4b"},
        {"role": "Brand Identity Designer", "name": "Palette", "is_head": False, "model": "gemma3:4b"},
        {"role": "Visual UI Designer", "name": "Canvas", "is_head": False, "model": "gemma3:4b"},
        {"role": "UX Designer", "name": "FlowState", "is_head": False, "model": "gemma3:4b"},
        {"role": "Wireframe & Information Architecture Agent", "name": "Blueprint", "is_head": False, "model": "qwen3.5:4b"},
        {"role": "Design System Agent", "name": "TokenForge", "is_head": False, "model": "qwen2.5-coder:3b"},
        {"role": "Responsive Design Specialist", "name": "Adaptive", "is_head": False, "model": "gemma3:4b"},
        {"role": "Accessibility Design Specialist", "name": "AllyAura", "is_head": False, "model": "gemma3:4b"},
        {"role": "Website Content Structure Agent", "name": "Structura", "is_head": False, "model": "qwen3.5:2b"},
        {"role": "Prototype & Design QA Reviewer", "name": "PixelCritic", "is_head": False, "model": "gemma3:4b"},
    ],
    "D06": [
        {"role": "Engineering Director / Department Head (Forge)", "name": "Forge", "is_head": True, "model": "qwen2.5-coder:3b"},
        {"role": "Frontend Engineer Agent", "name": "ReactEngine", "is_head": False, "model": "qwen2.5-coder:3b"},
        {"role": "Backend Engineer Agent", "name": "FastAPIEngine", "is_head": False, "model": "qwen2.5-coder:3b"},
        {"role": "API Integration Engineer", "name": "Connector", "is_head": False, "model": "qwen2.5-coder:3b"},
        {"role": "Database Engineer", "name": "SchemaMaster", "is_head": False, "model": "qwen2.5-coder:3b"},
        {"role": "Third-Party Integration Engineer", "name": "BridgeForge", "is_head": False, "model": "qwen2.5-coder:3b"},
        {"role": "Workflow Automation Engineer", "name": "PipelineDev", "is_head": False, "model": "qwen2.5-coder:3b"},
        {"role": "Coding / Debugging Specialist", "name": "BugHunter", "is_head": False, "model": "qwen2.5-coder:3b"},
        {"role": "Refactoring & Code Review Agent", "name": "CleanCode", "is_head": False, "model": "qwen2.5-coder:3b"},
        {"role": "Technical Documentation Agent", "name": "DocuTech", "is_head": False, "model": "qwen3.5:2b"},
    ],
    "D07": [
        {"role": "QA & Security Head (Sentinel)", "name": "Sentinel", "is_head": True, "model": "qwen2.5-coder:3b"},
        {"role": "Test Strategy Planner", "name": "TestStrategist", "is_head": False, "model": "phi4-mini:latest"},
        {"role": "Frontend Functional QA Agent", "name": "UIAssert", "is_head": False, "model": "qwen2.5-coder:3b"},
        {"role": "Backend Functional QA Agent", "name": "APIAssert", "is_head": False, "model": "qwen2.5-coder:3b"},
        {"role": "API & Contract Testing Agent", "name": "ContractCheck", "is_head": False, "model": "qwen2.5-coder:3b"},
        {"role": "Integration & Regression QA Agent", "name": "RegressionWatch", "is_head": False, "model": "qwen2.5-coder:3b"},
        {"role": "Performance Testing Agent", "name": "LoadScan", "is_head": False, "model": "qwen3.5:2b"},
        {"role": "Accessibility Testing Agent", "name": "A11yAuditor", "is_head": False, "model": "qwen3.5:2b"},
        {"role": "Security Review Agent", "name": "OWASPShield", "is_head": False, "model": "qwen2.5-coder:3b"},
        {"role": "Release Acceptance Reviewer", "name": "GateKeeper", "is_head": False, "model": "granite4.2:3b"},
    ],
    "D08": [
        {"role": "DevOps Director / Department Head", "name": "Helm", "is_head": True, "model": "phi4-mini:latest"},
        {"role": "CI/CD Pipeline Agent", "name": "BuildLine", "is_head": False, "model": "qwen2.5-coder:3b"},
        {"role": "Container & Environment Agent", "name": "DockerSmith", "is_head": False, "model": "qwen2.5-coder:3b"},
        {"role": "Hosting & Platform Agent", "name": "CloudDeploy", "is_head": False, "model": "qwen2.5-coder:3b"},
        {"role": "Domain, DNS & SSL Agent", "name": "CertManager", "is_head": False, "model": "qwen3.5:2b"},
        {"role": "Backup & Restore Agent", "name": "DataVault", "is_head": False, "model": "qwen3.5:2b"},
        {"role": "Uptime & Health Monitoring Agent", "name": "PingSentinel", "is_head": False, "model": "qwen3.5:2b"},
        {"role": "Logs & Observability Agent", "name": "LogStream", "is_head": False, "model": "qwen3.5:2b"},
        {"role": "Incident Triage Agent", "name": "AlertDispatch", "is_head": False, "model": "phi4-mini:latest"},
        {"role": "Release & Rollback Coordinator", "name": "RollbackZero", "is_head": False, "model": "granite4.2:3b"},
    ],
    "D09": [
        {"role": "Growth Director / Department Head (Echo)", "name": "Echo", "is_head": True, "model": "gemma3:4b"},
        {"role": "SEO Research Agent", "name": "RankCraft", "is_head": False, "model": "qwen3.5:2b"},
        {"role": "Content Strategy Agent", "name": "StoryArc", "is_head": False, "model": "gemma3:4b"},
        {"role": "Social Content Drafting Agent", "name": "ViralVox", "is_head": False, "model": "gemma3:4b"},
        {"role": "Case Study & Portfolio Agent", "name": "Showcase", "is_head": False, "model": "qwen3.5:4b"},
        {"role": "Brand Consistency Reviewer", "name": "ToneAudit", "is_head": False, "model": "gemma3:4b"},
        {"role": "Website Analytics Agent", "name": "TrafficPulse", "is_head": False, "model": "qwen3.5:2b"},
        {"role": "Email / Newsletter Drafting Agent", "name": "LetterForge", "is_head": False, "model": "gemma3:4b"},
        {"role": "Campaign Research Agent", "name": "AdTarget", "is_head": False, "model": "qwen3.5:4b"},
        {"role": "Growth Experiment Analyst", "name": "A/BMatrix", "is_head": False, "model": "granite4.2:3b"},
    ],
    "D10": [
        {"role": "Customer Success Head", "name": "Beacon", "is_head": True, "model": "granite4.2:3b"},
        {"role": "Customer Onboarding Agent", "name": "WelcomeFlow", "is_head": False, "model": "qwen3.5:2b"},
        {"role": "Client Account Coordinator", "name": "Liaison", "is_head": False, "model": "qwen3.5:2b"},
        {"role": "Support Request Triage Agent", "name": "HelpDesk", "is_head": False, "model": "qwen3.5:2b"},
        {"role": "Technical Issue Diagnosis Agent", "name": "Diagnostix", "is_head": False, "model": "qwen2.5-coder:3b"},
        {"role": "Feedback Analysis Agent", "name": "Sentiment", "is_head": False, "model": "qwen3.5:4b"},
        {"role": "Change Request Manager", "name": "ScopeGuard2", "is_head": False, "model": "granite4.2:3b"},
        {"role": "Customer Knowledge Base Agent", "name": "WikiMaster", "is_head": False, "model": "qwen3.5:2b"},
        {"role": "Review Request & Reputation Agent", "name": "Repute", "is_head": False, "model": "qwen3.5:2b"},
        {"role": "Retention & Project Handover Agent", "name": "Handover", "is_head": False, "model": "granite4.2:3b"},
    ],
}


def build_full_agent_roster() -> List[Dict[str, Any]]:
    """Build the exact 100 departmental AI profiles list + NEXUS central manager."""
    roster = []

    # 1. Add NEXUS central coordinator
    roster.append(NEXUS_PROFILE)

    # 2. Add 10 profiles for each of the 10 departments = 100 profiles
    for dept_code, roles in DEPARTMENT_ROLES.items():
        dept_head_name = roles[0]["name"]
        for idx, r in enumerate(roles, start=1):
            code = f"{dept_code}-{idx:02d}"
            reports_to = "NEXUS" if r["is_head"] else dept_head_name
            profile = {
                "code": code,
                "name": r["name"],
                "role": r["role"],
                "department_code": dept_code,
                "is_head": r["is_head"],
                "reports_to": reports_to,
                "model_preference": r["model"],
                "fallback_models": ["qwen3.5:2b", "phi4-mini:latest"],
                "system_instructions": (
                    f"You are {r['name']}, {r['role']} in department {dept_code} at CODE WIBES TECHNOLOGIES. "
                    f"You report to {reports_to}. Deliver production-quality, verified results. "
                    f"Never hallucinate facts or metrics; execute tasks within your authorized tool scope."
                ),
                "tool_allowlist": ["inspect_task", "submit_artifact", "request_review"],
                "approval_mode": "FOUNDER_APPROVAL" if r["is_head"] else "DRAFT_ONLY",
                "context_budget": 8192,
            }
            roster.append(profile)

    return roster
