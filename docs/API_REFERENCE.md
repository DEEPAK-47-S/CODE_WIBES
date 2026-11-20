# CODE WIBES TECHNOLOGIES — Verified API Reference

**Base URL:** `http://127.0.0.1:8000/api/v1`  
**Interactive Swagger Docs:** `http://127.0.0.1:8000/docs`  
**All endpoints verified with automated integration tests.**

---

## 1. System Health & Diagnostics

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Root company information & status |
| `GET` | `/health` | Basic application health ping |
| `GET` | `/health/database` | Database connectivity verification (`SELECT 1`) |
| `GET` | `/health/system` | Comprehensive system diagnostics: DB latency, Ollama loaded models, kill switches |

---

## 2. Organization, Departments & Agents

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/departments` | List all 10 canonical AI company departments |
| `GET` | `/api/v1/agents` | List all registered AI employee profiles |
| `GET` | `/api/v1/agents/org-chart` | Full hierarchical org chart (Founder ➔ NEXUS ➔ 10 Dept Heads ➔ 90 Specialists) |
| `POST`| `/api/v1/agents/sync-roster` | Idempotently sync 100 profiles and 10 departments in PostgreSQL |
| `POST`| `/api/v1/owner/chat/{agent_id}` | Direct interactive chat with any specific agent |

---

## 3. Governance, Kill Switches & Founder Approvals

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/settings` | Inspect global kill switches, calling gates, and budget caps |
| `PATCH`| `/api/v1/settings` | Update operational settings and safety parameters |
| `POST`| `/api/v1/settings/emergency-pause`| One-click Emergency Kill Switch to halt all company agents |
| `POST`| `/api/v1/settings/resume` | Resume company operations after an emergency pause |
| `GET` | `/api/v1/approvals/pending` | Fetch all pending requests awaiting Founder decision |
| `POST`| `/api/v1/approvals` | Submit action to Founder approval inbox |
| `POST`| `/api/v1/approvals/{id}/decide` | Founder decision: approve or reject with feedback |

---

## 4. Model Registry & Persistent Memory

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/models` | List all discovered Ollama models, contexts, and capabilities |
| `POST`| `/api/v1/models/probe` | Live probe local Ollama `/api/tags` and `/api/show` |
| `POST`| `/api/v1/models/{name}/benchmark` | Execute latency & throughput benchmark on a model |
| `GET` | `/api/v1/memory` | Search persistent 7-tier memory (constitution, founder, project, etc.) |
| `POST`| `/api/v1/memory` | Store or update a memory record in a specific tier |
| `POST`| `/api/v1/memory/checkpoints` | Create task context checkpoint (at 65-75% budget threshold) |
| `GET` | `/api/v1/memory/checkpoints/{task_id}/latest` | Fetch latest checkpoint to resume task with clean context |

---

## 5. Lead Intelligence & Voice Telephony

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/leads` | List qualified commercial leads |
| `POST`| `/api/v1/leads` | Create a lead |
| `POST`| `/api/v1/leads/google-maps-harvest` | Google Places API (New) discovery with Place ID deduplication |
| `GET` | `/api/v1/leads/export/csv` | Export leads as Excel-compatible CSV |
| `GET` | `/api/v1/leads/export/json` | Export leads as JSON |
| `GET` | `/api/v1/voice/records` | List historical voice call logs and compliance states |
| `POST`| `/api/v1/voice/test-call` | Compliant ElevenLabs test call (strictly to authorized numbers) |
| `POST`| `/api/v1/voice/opt-out/{lead_id}` | Enforce Do-Not-Contact suppression on lead |
| `POST`| `/api/v1/voice/founder-alert` | Trigger Founder Voice Alert Channel for high-severity incidents |

---

## 6. Projects, Customer Briefs & Website Factory

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/projects` | Fetch all ongoing projects |
| `POST`| `/api/v1/projects` | Create a new project |
| `GET` | `/api/v1/tasks` | List task backlog |
| `POST`| `/api/v1/tasks` | Create a task |
| `POST`| `/api/v1/proposals/briefs` | Create structured CustomerRequirementBrief |
| `GET` | `/api/v1/proposals/briefs` | List all requirement briefs |
| `POST`| `/api/v1/proposals/generate` | Compile proposal with milestones and pricing (Founder gated) |
| `GET` | `/api/v1/proposals` | List generated proposals and approval states |
| `POST`| `/api/v1/proposals/workspaces/create` | Initialize isolated project directory in `execution/workspaces/` |
| `POST`| `/api/v1/change-requests` | Submit customer review revision or out-of-scope change |
| `GET` | `/api/v1/change-requests/project/{id}` | List change requests for a project |
| `PATCH`| `/api/v1/change-requests/{id}/status` | Update change request progress and resolution notes |
| `POST`| `/api/v1/owner/command` | Natural language directive to Nexus or departmental heads |
| `POST`| `/api/v1/owner/autonomous-sprint` | Run autonomous company sprint |
