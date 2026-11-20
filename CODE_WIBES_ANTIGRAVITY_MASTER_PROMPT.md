# CODE WIBES TECHNOLOGIES — Antigravity Master Build Brief
Document purpose: This is the canonical product brief and implementation instruction for Google Antigravity. Use it as the long-term project memory and build specification. Do not reduce the product to a chatbot, static dashboard, fake CRM, or a collection of disconnected agents.

Brand: CODE WIBES TECHNOLOGIES
Tagline: Turning Ideas Into Digital Solutions.
GitHub repository: https://github.com/DEEPAK-47-S/CODE_WIBES
Reported local workspace: C:\deepak\coding\CODE-WIBES-REPO
Primary operator: Founder / Owner (human).
Initial market: Coimbatore and Tamil Nadu, India; architecture should support other Indian states and international markets later.

## 1. NON-NEGOTIABLE PRODUCT VISION
Build a real, working, AI-operated software-services company operating system for CODE WIBES TECHNOLOGIES.

The Founder is the only human owner and final authority. All department heads, managers, specialists, and operational workers are AI-agent profiles. Agents must coordinate through a central task, approval, memory, and audit system. The platform must support an end-to-end software-services workflow:
1. Plan weekly territory and industry discovery.
2. Discover and qualify potential business leads using approved data sources and compliant APIs.
3. Maintain a deduplicated CRM with source provenance and permitted data only.
4. Contact eligible prospects through a compliant, approved voice workflow using ElevenLabs and a supported telecom provider.
5. Conduct requirement discovery and capture a structured customer brief.
6. Create proposal, scope, estimated effort, draft pricing, milestones, and acceptance criteria.
7. Obtain Founder approval before sending a proposal or making a commitment.
8. Create a project workspace and delegate design, development, QA, and deployment tasks to specialist agents.
9. Generate and test real customer websites/web apps, not static screenshots or fake previews.
10. Deploy to staging, collect approval, and deploy production only when authorized.
11. Collect customer feedback, turn it into tracked change requests, implement approved revisions, and retest.
12. Monitor delivered websites and provide customer support, status reporting, and legitimate review requests.

The public company website and private AI Company HQ dashboard are two separate experiences backed by the same trusted backend. The private dashboard is the Founder’s control room.

### Product principles
- Backend is the single source of truth. Frontend must display backend/API data; never invent metrics, AI output, lead records, call records, project progress, or deployment status.
- No fake frontend data in production. Demo/seed data is allowed only in a clearly labelled Demo Mode and must never be mixed with real customer data.
- No duplicate business rules in React and FastAPI. Validate and enforce rules in the backend; frontend is a presentation/client layer.
- No agent may bypass the central workflow, permissions, Founder approval, rate limits, or audit logging.
- Every consequential operation must have an actor, timestamp, task ID, policy decision, input/output references, and audit event.
- A department head must review specialist outputs before they are passed to NEXUS or another department, according to the task risk level.
- Agents must never approve their own work or change their own permissions.
- No infinite agent-to-agent conversations. Agents communicate using bounded tasks, structured artifacts, and explicit handoffs.
- No parallel duplicate records or duplicate frontend state stores. Use database constraints, idempotency keys, and canonical API resources.
- Do not claim a feature works unless its integration, tests, and real end-to-end path have been verified.

## 2. ORGANISATION AND AUTHORITY MODEL
Authority hierarchy:
Founder / Owner (human)
↓
NEXUS — Central AI Manager / Chief of Staff
↓
10 Department Heads
↓
9 specialist AI employees in each department

Create exactly 100 departmental AI employee profiles: 10 department heads + 90 specialists. NEXUS is the separate company-wide coordinating system role, not counted in those 100 departmental profiles.

The Founder controls NEXUS. The Founder can inspect any department, employee profile, task, memory, tool permission, model assignment, approval request, budget, call, project, and audit record. Routine communication should come through NEXUS as the single central manager, while the dashboard can expose all details when the Founder opens them.

### Central manager: NEXUS
NEXUS responsibilities:
- Understand Founder instructions and convert them into goals, projects, and tasks.
- Identify the relevant department and assign work to the correct department head.
- Delegate specialist work through explicit tasks with acceptance criteria.
- Track dependencies, blockers, progress, budgets, retries, and deadlines.
- Check department-head reviews and resolve conflicting outputs.
- Present concise decision-ready summaries to the Founder.
- Request approval before any action covered by an approval policy.
- Never assume that silence means approval.
- Never modify the Founder’s global policy or approval settings.
- Never send an external communication or initiate a real call unless the applicable approval and compliance gates pass.

### The 10 departments and their 10 profiles each
Every department list below includes its Head as role 1.
D01 — Executive Operations & Governance
1. Operations Director / Department Head
2. Executive Assistant Agent
3. Policy & Approval Coordinator
4. Finance Analyst (draft/reporting only)
5. Legal & Compliance Research Assistant (not a lawyer; no legal advice)
6. Open-Source License & Vendor Review Agent
7. Resource & Capacity Planner
8. KPI & Management Reporting Agent
9. Internal Audit & Data Governance Agent
10. Knowledge & Company Memory Manager

D02 — Market Research & Lead Intelligence
1. Head of Market Intelligence
2. Territory Planner
3. District & Weekly Campaign Scheduler
4. Google Places API Research Agent
5. Business Website Research Agent
6. Business Data Verification Agent
7. Lead Qualification & Scoring Agent
8. Deduplication & Data Quality Agent
9. Industry / Competitor Research Agent
10. Source Provenance & Consent Evidence Steward

D03 — Sales, Customer Relations & Voice
1. Sales Director / Department Head
2. Outreach Campaign Planner
3. Voice Agent Supervisor
4. ElevenLabs Voice Conversation Agent
5. Lead Qualification & Call Summary Agent
6. CRM Sales Coordinator
7. Follow-up Planner
8. Objection & FAQ Research Agent
9. Meeting / Callback Scheduler
10. Consent, Suppression & Opt-out Enforcement Agent

D04 — Customer Discovery & Solution Architecture
1. Discovery & Solutions Head
2. Requirements Interviewer
3. Business Analyst
4. UX Research Agent
5. Solution Architect
6. Scope & Acceptance Criteria Writer
7. Effort / Estimate Drafting Agent
8. Delivery Timeline Planner
9. Project Risk Analyst
10. Customer Brief & Documentation Agent

D05 — UI/UX & Brand Design
1. Design Director / Department Head
2. Brand Identity Designer
3. Visual UI Designer
4. UX Designer
5. Wireframe & Information Architecture Agent
6. Design System Agent
7. Responsive Design Specialist
8. Accessibility Design Specialist
9. Website Content Structure Agent
10. Prototype & Design QA Reviewer

D06 — Software Engineering
1. Engineering Director / Department Head
2. Frontend Engineer Agent
3. Backend Engineer Agent
4. API Integration Engineer
5. Database Engineer
6. Third-Party Integration Engineer
7. Workflow Automation Engineer
8. Coding / Debugging Specialist
9. Refactoring & Code Review Agent
10. Technical Documentation Agent

D07 — Quality Assurance & Security
1. QA & Security Head
2. Test Strategy Planner
3. Frontend Functional QA Agent
4. Backend Functional QA Agent
5. API & Contract Testing Agent
6. Integration & Regression QA Agent
7. Performance Testing Agent
8. Accessibility Testing Agent
9. Security Review Agent
10. Release Acceptance Reviewer

D08 — DevOps, Deployment & Reliability
1. DevOps Director / Department Head
2. CI/CD Pipeline Agent
3. Container & Environment Agent
4. Hosting & Platform Agent
5. Domain, DNS & SSL Agent
6. Backup & Restore Agent
7. Uptime & Health Monitoring Agent
8. Logs & Observability Agent
9. Incident Triage Agent
10. Release & Rollback Coordinator

D09 — Marketing & Growth
1. Growth Director / Department Head
2. SEO Research Agent
3. Content Strategy Agent
4. Social Content Drafting Agent
5. Case Study & Portfolio Agent
6. Brand Consistency Reviewer
7. Website Analytics Agent
8. Email / Newsletter Drafting Agent
9. Campaign Research Agent
10. Growth Experiment Analyst

D10 — Customer Success & Support
1. Customer Success Head
2. Customer Onboarding Agent
3. Client Account Coordinator
4. Support Request Triage Agent
5. Technical Issue Diagnosis Agent
6. Feedback Analysis Agent
7. Change Request Manager
8. Customer Knowledge Base Agent
9. Review Request & Reputation Agent (no fake or manipulated reviews)
10. Retention & Project Handover Agent

### Required profile fields for every AI employee
Each profile must have:
- stable agent_id, display name, role, department, and reports_to;
- role-specific system instructions and clear responsibilities;
- allowed model preferences and fallback models;
- verified capabilities required (tools, vision, audio, structured output, context budget);
- tool allowlist and denied tools;
- database/resource permissions, limited to least privilege;
- input schema and required output schema;
- memory namespace and retention rules;
- maximum context budget and checkpoint strategy;
- timeout, retry limit, concurrency limit, and cost/token budget;
- approval mode by action type;
- department-head reviewer and quality rubric;
- active/paused/disabled status;
- version number, created/updated timestamps, and full change history.

Create role definitions as configuration/data, not 100 hard-coded independent code paths. Profiles may reuse model instances and common agent runtime code. Do not run all 100 agents simultaneously. Agents should become active only when assigned a task.

## 3. APPROVALS, PERMISSIONS, SAFETY AND AUTONOMY
Build an explicit Founder-controlled policy engine. The default mode for all external or consequential actions is Approval Required.

### Approval modes
- BLOCKED: action is disabled.
- DRAFT_ONLY: agent can prepare the action but cannot execute it.
- FOUNDER_APPROVAL: agent requests approval; no execution until Founder approves.
- AUTO_APPROVED: permitted only after the Founder explicitly enables that exact action/category and any defined limits.

Actions that must never execute without explicit Founder approval:
- outbound calls to real prospects or customers;
- sending emails, SMS, WhatsApp, social messages, or other external communications;
- sending proposals, quotations, prices, commitments, contracts, legal notices, or invoices;
- accepting money, making purchases, using paid APIs beyond an approved budget, or changing billing;
- production deployment, DNS/domain changes, destructive migrations, data deletion, or public website changes;
- public advertising, publishing customer case studies, using customer logos, or posting content;
- sharing or exporting customer data;
- changing security controls, API permissions, user roles, secrets, or approval rules.

## 4. MODEL REGISTRY — EXISTING OLLAMA MODELS
Hardware and scheduler constraints:
Windows 11, HP Victus, Ryzen 7 7445HS, NVIDIA RTX 4050 Laptop GPU 6GB VRAM, 16GB RAM.
- Start with one local inference job at a time.
- Use a scheduler to queue agents and reuse model workers. Cap concurrent loaded models and concurrent generations.
- Initial context settings conservative (4K–8K).

## 5. PERSISTENT MEMORY & CONTEXT CONTINUATION
Context length is not permanent memory. Build persistent memory outside the model context in PostgreSQL across 7 layers:
1. Company Constitution
2. Founder Preferences
3. Department Memory
4. Agent Memory
5. Project Memory
6. Task Memory
7. Customer Memory
Checkpoint and resume tasks when context budget threshold (65-75%) is reached.

## 6. END-TO-END DELIVERY WORKFLOW
1. Territory & Lead Discovery (Google Places API with compliance, deduplication, no web scraping).
2. Lead Qualification (evidence-based).
3. Sales Calling & ElevenLabs (disabled by default, strict TRAI/TCCCPR India compliance, test mode only).
4. Customer Discovery & Requirements.
5. Proposal & Founder Approval.
6. Website/App Factory (isolated workspaces, Git branch/worktree, real apps, staging preview, release approval).
7. Feedback, Revisions & Monitoring.
