# CODE WIBES TECHNOLOGIES — AI Agent Employee Catalog

**Total Profiles:** 101 (1 Central Manager + 10 Department Heads + 90 Specialist AI Employees).  
**Configuration Source:** `backend/app/agents/catalog.py`  
**Database Table:** `agents` (PostgreSQL)  

---

## Central Coordination Role

### NEXUS — Central AI Manager / Chief of Staff
* **Code:** `NEXUS-00`
* **Role:** Chief of Staff & Central AI Manager
* **Reports To:** Founder / Owner (Human)
* **Assigned Model:** `qwen3.5:4b`
* **Fallback Models:** `llama3.1:latest`, `phi4-mini:latest`
* **Approval Mode:** `FOUNDER_APPROVAL`
* **Tool Allowlists:** `task_delegate`, `task_inspect`, `approval_request`, `memory_query`

---

## D01 — Executive Operations & Governance
* **Head:** Vanguard (`granite4.2:3b`) — Operations Director / Department Head

| Code | Role | Agent Name | Assigned Model | Approval Mode |
|---|---|---|---|---|
| D01-01 | Operations Director / Department Head | Vanguard | `granite4.2:3b` | FOUNDER_APPROVAL |
| D01-02 | Executive Assistant Agent | Clio | `qwen3.5:2b` | DRAFT_ONLY |
| D01-03 | Policy & Approval Coordinator | Arbiter | `granite4.2:3b` | DRAFT_ONLY |
| D01-04 | Finance Analyst (Ledger) | Ledger | `qwen3.5:2b` | DRAFT_ONLY |
| D01-05 | Legal & Compliance Research Assistant | Justiciar | `granite4.2:3b` | DRAFT_ONLY |
| D01-06 | Open-Source License & Vendor Review Agent | LicenseGuard | `qwen3.5:2b` | DRAFT_ONLY |
| D01-07 | Resource & Capacity Planner | Chronos | `granite4.2:3b` | DRAFT_ONLY |
| D01-08 | KPI & Management Reporting Agent | Metricon | `qwen3.5:2b` | DRAFT_ONLY |
| D01-09 | Internal Audit & Data Governance Agent | AuditorPrime | `granite4.2:3b` | DRAFT_ONLY |
| D01-10 | Knowledge & Company Memory Manager | Mnemosyne | `qwen3.5:4b` | DRAFT_ONLY |

---

## D02 — Market Research & Lead Intelligence
* **Head:** Hunter (`llama3.1:latest`) — Head of Market Intelligence

| Code | Role | Agent Name | Assigned Model | Approval Mode |
|---|---|---|---|---|
| D02-01 | Head of Market Intelligence | Hunter | `llama3.1:latest` | FOUNDER_APPROVAL |
| D02-02 | Territory Planner | Cartographer | `qwen3.5:2b` | DRAFT_ONLY |
| D02-03 | District & Weekly Campaign Scheduler | Cadence | `qwen3.5:2b` | DRAFT_ONLY |
| D02-04 | Google Places API Research Agent | PlaceScout | `qwen3.5:2b` | DRAFT_ONLY |
| D02-05 | Business Website Research Agent | WebAudit | `qwen3.5:2b` | DRAFT_ONLY |
| D02-06 | Business Data Verification Agent | Veritas | `qwen3.5:2b` | DRAFT_ONLY |
| D02-07 | Lead Qualification & Scoring Agent | ScoreCraft | `granite4.2:3b` | DRAFT_ONLY |
| D02-08 | Deduplication & Data Quality Agent | DeDuper | `qwen3.5:2b` | DRAFT_ONLY |
| D02-09 | Industry / Competitor Research Agent | Insight | `qwen3.5:4b` | DRAFT_ONLY |
| D02-10 | Source Provenance & Consent Evidence Steward | Provenance | `granite4.2:3b` | DRAFT_ONLY |

---

## D03 — Sales, Customer Relations & Voice
* **Head:** Venture (`llama3.1:latest`) — Sales Director / Department Head

| Code | Role | Agent Name | Assigned Model | Approval Mode |
|---|---|---|---|---|
| D03-01 | Sales Director / Department Head | Venture | `llama3.1:latest` | FOUNDER_APPROVAL |
| D03-02 | Outreach Campaign Planner | Strategos | `qwen3.5:4b` | DRAFT_ONLY |
| D03-03 | Voice Agent Supervisor | Vocalis | `phi4-mini:latest` | DRAFT_ONLY |
| D03-04 | ElevenLabs Voice Conversation Agent | AriaVoice | `llama3.1:latest` | FOUNDER_APPROVAL |
| D03-05 | Lead Qualification & Call Summary Agent | Transcribe | `qwen3.5:2b` | DRAFT_ONLY |
| D03-06 | CRM Sales Coordinator | NexusCRM | `qwen3.5:2b` | DRAFT_ONLY |
| D03-07 | Follow-up Planner | Persist | `qwen3.5:2b` | DRAFT_ONLY |
| D03-08 | Objection & FAQ Research Agent | Resolve | `qwen3.5:4b` | DRAFT_ONLY |
| D03-09 | Meeting / Callback Scheduler | Calenda | `qwen3.5:2b` | DRAFT_ONLY |
| D03-10 | Consent, Suppression & Opt-out Enforcement Agent | OptOutSentry | `granite4.2:3b` | DRAFT_ONLY |

---

## D04 — Customer Discovery & Solution Architecture
* **Head:** Atlas (`qwen3.5:4b`) — Discovery & Solutions Head

| Code | Role | Agent Name | Assigned Model | Approval Mode |
|---|---|---|---|---|
| D04-01 | Discovery & Solutions Head | Atlas | `qwen3.5:4b` | FOUNDER_APPROVAL |
| D04-02 | Requirements Interviewer | Inquirer | `qwen3.5:4b` | DRAFT_ONLY |
| D04-03 | Business Analyst | AnalystPrime | `granite4.2:3b` | DRAFT_ONLY |
| D04-04 | UX Research Agent | Empathy | `gemma3:4b` | DRAFT_ONLY |
| D04-05 | Solution Architect | Synthesize | `qwen2.5-coder:3b` | DRAFT_ONLY |
| D04-06 | Scope & Acceptance Criteria Writer | ScopeGuard | `granite4.2:3b` | DRAFT_ONLY |
| D04-07 | Effort / Estimate Drafting Agent | Estimator | `qwen3.5:2b` | DRAFT_ONLY |
| D04-08 | Delivery Timeline Planner | Gantt | `granite4.2:3b` | DRAFT_ONLY |
| D04-09 | Project Risk Analyst | RiskEngine | `granite4.2:3b` | DRAFT_ONLY |
| D04-10 | Customer Brief & Documentation Agent | BriefCraft | `qwen3.5:2b` | DRAFT_ONLY |

---

## D05 — UI/UX & Brand Design
* **Head:** Aura (`gemma3:4b`) — Design Director / Department Head

| Code | Role | Agent Name | Assigned Model | Approval Mode |
|---|---|---|---|---|
| D05-01 | Design Director / Department Head | Aura | `gemma3:4b` | FOUNDER_APPROVAL |
| D05-02 | Brand Identity Designer | Palette | `gemma3:4b` | DRAFT_ONLY |
| D05-03 | Visual UI Designer | Canvas | `gemma3:4b` | DRAFT_ONLY |
| D05-04 | UX Designer | FlowState | `gemma3:4b` | DRAFT_ONLY |
| D05-05 | Wireframe & Information Architecture Agent | Blueprint | `qwen3.5:4b` | DRAFT_ONLY |
| D05-06 | Design System Agent | TokenForge | `qwen2.5-coder:3b` | DRAFT_ONLY |
| D05-07 | Responsive Design Specialist | Adaptive | `gemma3:4b` | DRAFT_ONLY |
| D05-08 | Accessibility Design Specialist | AllyAura | `gemma3:4b` | DRAFT_ONLY |
| D05-09 | Website Content Structure Agent | Structura | `qwen3.5:2b` | DRAFT_ONLY |
| D05-10 | Prototype & Design QA Reviewer | PixelCritic | `gemma3:4b` | DRAFT_ONLY |

---

## D06 — Software Engineering
* **Head:** Forge (`qwen2.5-coder:3b`) — Engineering Director / Department Head

| Code | Role | Agent Name | Assigned Model | Approval Mode |
|---|---|---|---|---|
| D06-01 | Engineering Director / Department Head | Forge | `qwen2.5-coder:3b` | FOUNDER_APPROVAL |
| D06-02 | Frontend Engineer Agent | ReactEngine | `qwen2.5-coder:3b` | DRAFT_ONLY |
| D06-03 | Backend Engineer Agent | FastAPIEngine | `qwen2.5-coder:3b` | DRAFT_ONLY |
| D06-04 | API Integration Engineer | Connector | `qwen2.5-coder:3b` | DRAFT_ONLY |
| D06-05 | Database Engineer | SchemaMaster | `qwen2.5-coder:3b` | DRAFT_ONLY |
| D06-06 | Third-Party Integration Engineer | BridgeForge | `qwen2.5-coder:3b` | DRAFT_ONLY |
| D06-07 | Workflow Automation Engineer | PipelineDev | `qwen2.5-coder:3b` | DRAFT_ONLY |
| D06-08 | Coding / Debugging Specialist | BugHunter | `qwen2.5-coder:3b` | DRAFT_ONLY |
| D06-09 | Refactoring & Code Review Agent | CleanCode | `qwen2.5-coder:3b` | DRAFT_ONLY |
| D06-10 | Technical Documentation Agent | DocuTech | `qwen3.5:2b` | DRAFT_ONLY |

---

## D07 — Quality Assurance & Security
* **Head:** Sentinel (`qwen2.5-coder:3b`) — QA & Security Head

| Code | Role | Agent Name | Assigned Model | Approval Mode |
|---|---|---|---|---|
| D07-01 | QA & Security Head | Sentinel | `qwen2.5-coder:3b` | FOUNDER_APPROVAL |
| D07-02 | Test Strategy Planner | TestStrategist | `phi4-mini:latest` | DRAFT_ONLY |
| D07-03 | Frontend Functional QA Agent | UIAssert | `qwen2.5-coder:3b` | DRAFT_ONLY |
| D07-04 | Backend Functional QA Agent | APIAssert | `qwen2.5-coder:3b` | DRAFT_ONLY |
| D07-05 | API & Contract Testing Agent | ContractCheck | `qwen2.5-coder:3b` | DRAFT_ONLY |
| D07-06 | Integration & Regression QA Agent | RegressionWatch | `qwen2.5-coder:3b` | DRAFT_ONLY |
| D07-07 | Performance Testing Agent | LoadScan | `qwen3.5:2b` | DRAFT_ONLY |
| D07-08 | Accessibility Testing Agent | A11yAuditor | `qwen3.5:2b` | DRAFT_ONLY |
| D07-09 | Security Review Agent | OWASPShield | `qwen2.5-coder:3b` | DRAFT_ONLY |
| D07-10 | Release Acceptance Reviewer | GateKeeper | `granite4.2:3b` | DRAFT_ONLY |

---

## D08 — DevOps, Deployment & Reliability
* **Head:** Helm (`phi4-mini:latest`) — DevOps Director / Department Head

| Code | Role | Agent Name | Assigned Model | Approval Mode |
|---|---|---|---|---|
| D08-01 | DevOps Director / Department Head | Helm | `phi4-mini:latest` | FOUNDER_APPROVAL |
| D08-02 | CI/CD Pipeline Agent | BuildLine | `qwen2.5-coder:3b` | DRAFT_ONLY |
| D08-03 | Container & Environment Agent | DockerSmith | `qwen2.5-coder:3b` | DRAFT_ONLY |
| D08-04 | Hosting & Platform Agent | CloudDeploy | `qwen2.5-coder:3b` | DRAFT_ONLY |
| D08-05 | Domain, DNS & SSL Agent | CertManager | `qwen3.5:2b` | DRAFT_ONLY |
| D08-06 | Backup & Restore Agent | DataVault | `qwen3.5:2b` | DRAFT_ONLY |
| D08-07 | Uptime & Health Monitoring Agent | PingSentinel | `qwen3.5:2b` | DRAFT_ONLY |
| D08-08 | Logs & Observability Agent | LogStream | `qwen3.5:2b` | DRAFT_ONLY |
| D08-09 | Incident Triage Agent | AlertDispatch | `phi4-mini:latest` | DRAFT_ONLY |
| D08-10 | Release & Rollback Coordinator | RollbackZero | `granite4.2:3b` | DRAFT_ONLY |

---

## D09 — Marketing & Growth
* **Head:** Echo (`gemma3:4b`) — Growth Director / Department Head

| Code | Role | Agent Name | Assigned Model | Approval Mode |
|---|---|---|---|---|
| D09-01 | Growth Director / Department Head | Echo | `gemma3:4b` | FOUNDER_APPROVAL |
| D09-02 | SEO Research Agent | RankCraft | `qwen3.5:2b` | DRAFT_ONLY |
| D09-03 | Content Strategy Agent | StoryArc | `gemma3:4b` | DRAFT_ONLY |
| D09-04 | Social Content Drafting Agent | ViralVox | `gemma3:4b` | DRAFT_ONLY |
| D09-05 | Case Study & Portfolio Agent | Showcase | `qwen3.5:4b` | DRAFT_ONLY |
| D09-06 | Brand Consistency Reviewer | ToneAudit | `gemma3:4b` | DRAFT_ONLY |
| D09-07 | Website Analytics Agent | TrafficPulse | `qwen3.5:2b` | DRAFT_ONLY |
| D09-08 | Email / Newsletter Drafting Agent | LetterForge | `gemma3:4b` | DRAFT_ONLY |
| D09-09 | Campaign Research Agent | AdTarget | `qwen3.5:4b` | DRAFT_ONLY |
| D09-10 | Growth Experiment Analyst | A/BMatrix | `granite4.2:3b` | DRAFT_ONLY |

---

## D10 — Customer Success & Support
* **Head:** Beacon (`granite4.2:3b`) — Customer Success Head

| Code | Role | Agent Name | Assigned Model | Approval Mode |
|---|---|---|---|---|
| D10-01 | Customer Success Head | Beacon | `granite4.2:3b` | FOUNDER_APPROVAL |
| D10-02 | Customer Onboarding Agent | WelcomeFlow | `qwen3.5:2b` | DRAFT_ONLY |
| D10-03 | Client Account Coordinator | Liaison | `qwen3.5:2b` | DRAFT_ONLY |
| D10-04 | Support Request Triage Agent | HelpDesk | `qwen3.5:2b` | DRAFT_ONLY |
| D10-05 | Technical Issue Diagnosis Agent | Diagnostix | `qwen2.5-coder:3b` | DRAFT_ONLY |
| D10-06 | Feedback Analysis Agent | Sentiment | `qwen3.5:4b` | DRAFT_ONLY |
| D10-07 | Change Request Manager | ScopeGuard2 | `granite4.2:3b` | DRAFT_ONLY |
| D10-08 | Customer Knowledge Base Agent | WikiMaster | `qwen3.5:2b` | DRAFT_ONLY |
| D10-09 | Review Request & Reputation Agent | Repute | `qwen3.5:2b` | DRAFT_ONLY |
| D10-10 | Retention & Project Handover Agent | Handover | `granite4.2:3b` | DRAFT_ONLY |
