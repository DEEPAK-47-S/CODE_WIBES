# CODE WIBES TECHNOLOGIES — Implementation Roadmap

**Document Reference:** `CODE_WIBES_ANTIGRAVITY_MASTER_PROMPT.md`  
**Execution Strategy:** Sequential, non-breaking, test-verified, evidence-backed implementation.

---

## Phase Overview

```
Phase 0: Repository Audit & Recovery (COMPLETE)
   │
Phase 1: Secure Company Foundation (Auth, Audit Logs, Settings)
   │
Phase 2: Org Chart & 100-Agent Profile Registry (10 Depts + NEXUS)
   │
Phase 3: Model Registry, Capability Probing & Persistent Memory
   │
Phase 4: Durable Task Engine & Founder Approval Center
   │
Phase 5: Policy-Compliant Lead CRM & Places Discovery
   │
Phase 6: ElevenLabs Voice Integration & Compliance Test Harness
   │
Phase 7: Requirement Discovery & Proposal Generator
   │
Phase 8: Website/App Factory & Isolated Workspaces
   │
Phase 9: Customer Review Portal & Change Management
   │
Phase 10: Public Company Marketing Website
   │
Phase 11: Production Monitoring, Health Probes & Hardening
```

---

## Detailed Phase Breakdown

### Phase 0 — Repository Audit & Recovery (Completed)
- [x] Baseline audit of existing backend, database, models, and frontend.
- [x] Document verified current state in `docs/CURRENT_STATE_AUDIT.md`.
- [x] Create canonical Master Prompt in `CODE_WIBES_ANTIGRAVITY_MASTER_PROMPT.md`.
- [x] Establish Risk Register in `docs/RISK_REGISTER.md`.

### Phase 1 — Secure Company Foundation
- [ ] Implement Founder Authentication and secure session tokens.
- [ ] Create append-only `audit_logs` schema tracking actor, action, timestamp, task, policy decision, input/output hash.
- [ ] Implement global Emergency Kill Switches (`Pause All Agents`, `Disable External Actions`).
- [ ] Add backend unit tests for security and authorization.

### Phase 2 — Org Chart & 100-Agent Registry
- [ ] Seed 10 canonical departments (D01 through D10) in PostgreSQL.
- [ ] Seed exactly 100 departmental AI employee profiles (10 Department Heads + 90 Specialists).
- [ ] Establish NEXUS as the central coordinating system agent.
- [ ] Structure agent profiles as configuration data (system instructions, capabilities, tool allowlists, memory namespaces, approval modes).
- [ ] Create interactive Org Chart and Agent Directory in the frontend.

### Phase 3 — Model Registry, Capability Probing & Persistent Memory
- [ ] Build Model Registry table discovering installed Ollama models dynamically via `/api/tags` and `/api/show`.
- [ ] Implement automated capability probing (tools, vision, JSON mode, context limit).
- [ ] Build 7-tier Persistent Memory in PostgreSQL (Constitution, Founder, Department, Agent, Project, Task, Customer).
- [ ] Implement Context Checkpoint & Resume engine (triggering at 65-75% context threshold).

### Phase 4 — Durable Task Engine & Founder Approvals
- [ ] Implement stateful task lifecycle (`created` -> `assigned` -> `running` -> `awaiting_approval` -> `completed` / `failed`).
- [ ] Implement Founder Approval Inbox (`BLOCKED`, `DRAFT_ONLY`, `FOUNDER_APPROVAL`, `AUTO_APPROVED`).
- [ ] Build Task Dependencies, retry limits, backoff, and idempotency guarantees.

### Phase 5 — Policy-Compliant Lead CRM & Places Discovery
- [ ] Build territory planner for districts and industry categories.
- [ ] Implement official Google Places API (New) adapter with field masking and Place ID deduplication.
- [ ] Enforce compliant Google attribution and zero bulk-scraping policies.
- [ ] Support offline AI crawler fallback with clearly marked source provenance.

### Phase 6 — ElevenLabs Voice Integration & Compliance Test Harness
- [ ] Build ElevenLabs agent integration adapter with hard-coded **disabled-by-default** safety gate.
- [ ] Implement India telecom compliance gate (TRAI / TCCCPR / DLT / A2P check).
- [ ] Enable test-only mode restricted strictly to Founder-authorized phone numbers.
- [ ] Provide separate Founder Alert Voice Channel for critical production incidents.

### Phase 7 — Requirement Discovery & Proposal Workflow
- [ ] Build structured `CustomerRequirementBrief` schema with version history.
- [ ] Create proposal generator (scope, deliverables, timeline, pricing draft, acceptance criteria).
- [ ] Enforce mandatory Founder approval gate before any proposal can be marked ready or dispatched.

### Phase 8 — Website/App Factory & Isolated Workspaces
- [ ] Create isolated project workspace directories under `execution/workspaces/<project_id>`.
- [ ] Establish Git branch-per-project workflow.
- [ ] Implement code generation for real full-stack web applications with automated unit and Playwright smoke tests.
- [ ] Staging preview environment and release gate.

### Phase 9 — Customer Review Portal & Change Management
- [ ] Client review portal for previewing staging sites and submitting feedback.
- [ ] Convert customer feedback into versioned change requests with scope checks.
- [ ] Regression test runner after revisions.

### Phase 10 — Public Company Marketing Website
- [ ] Responsive public marketing website with Midnight Navy (`#101827`) and Electric Blue (`#2563EB`) brand identity.
- [ ] Pages: Home, About, Services, Case Studies, Process, Contact, Quote Request.
- [ ] Public forms integrated with backend rate-limiting and audit capture.

### Phase 11 — Production Monitoring, Health Probes & Hardening
- [ ] Background uptime and health monitoring service.
- [ ] Rollback-capable deployment runbooks and automated database backup verification.
- [ ] Comprehensive documentation and operational manuals.
