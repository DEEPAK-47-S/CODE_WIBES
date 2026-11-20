# CODE WIBES TECHNOLOGIES — Risk Register & Mitigation Strategy

**Document Reference:** `CODE_WIBES_ANTIGRAVITY_MASTER_PROMPT.md`  
**Review Cadence:** Every Phase completion.

---

## 1. Compliance & Legal Risks

| Risk ID | Description | Severity | Mitigation Strategy |
|---|---|---|---|
| **R-LEG-01** | **Unsolicited Voice Calling / TRAI Non-Compliance**<br>Making automated calls to phone numbers obtained from Google Maps violates TRAI/TCCCPR rules in India without DLT registration, sender headers, and A2P consent. | **CRITICAL** | Real calling is **hard-disabled by default** in backend. Test calling allowed only to Founder-owned verified numbers. Calling requires multi-factor Founder approval and DLT verification records. |
| **R-LEG-02** | **Google Maps / Places Terms Violation**<br>Scraping the Google Maps website or bulk exporting/storing private directory data breaches Google Maps Platform Terms of Service. | **HIGH** | Use only the official Google Places API (New). Store only exempt Place IDs long-term; fetch fresh details for views. Never run DOM web scrapers on Google Maps. Display mandatory Google attribution. |
| **R-LEG-03** | **Unreviewed Legal or Financial Advice by AI**<br>AI agents generating binding contracts, invoices, or legal opinions without human legal review. | **HIGH** | The legal agent is strictly designated as a research/checklist tool. Output is explicitly watermarked: *"Draft only — not legal advice"*. Founder approval mandatory before sending any contract/proposal. |

---

## 2. Technical & Architectural Risks

| Risk ID | Description | Severity | Mitigation Strategy |
|---|---|---|---|
| **R-TECH-01** | **VRAM & Hardware Exhaustion (RTX 4050 6GB VRAM)**<br>Attempting to load multiple models or run 100 agents concurrently will crash Ollama or cause CUDA Out-of-Memory (OOM). | **HIGH** | Sequential task scheduler: **maximum 1 active local inference job at a time**. Strict concurrency cap. Agents are configurations, not persistent resident processes. Conservative context default (4K-8K). |
| **R-TECH-02** | **Context Window Overflow & Task Amnesia**<br>Models losing task context or failing mid-execution when conversation tokens reach limits. | **HIGH** | Implement persistent PostgreSQL memory. Checkpoint task state at 65-75% context threshold. Resume with clean context containing structured checkpoint summary. |
| **R-TECH-03** | **Prompt Injection & Autonomous Runaway**<br>Agent entering recursive calling loops, spending excessive compute, or executing unapproved external mutations. | **HIGH** | Strict loop breaker (max 3 retries, timeout per task). Explicit tool allowlists. Emergency Kill Switch (`Pause All Agents`). Consequential actions gated by Founder Approval. |
| **R-TECH-04** | **Secret Exfiltration / Credential Leaks**<br>API keys or database passwords appearing in AI model prompts, client responses, or Git commits. | **CRITICAL** | Server-side environment variables only (`backend/.env` in `.gitignore`). Secret redaction filter applied to all LLM prompt constructors and API serialization. |

---

## 3. Operational & Delivery Risks

| Risk ID | Description | Severity | Mitigation Strategy |
|---|---|---|---|
| **R-OPS-01** | **Fabricated / Hallucinated Business Metrics**<br>Agents inventing leads, fake testimonials, or false completion percentages. | **HIGH** | Enforce single source of truth: PostgreSQL database. Frontend only displays verified backend records. Missing data is explicitly marked as "Missing", never hallucinated. |
| **R-OPS-02** | **Project Workspace Collision**<br>Multiple agents editing the same files simultaneously or cross-contaminating client projects. | **MEDIUM** | Project-isolated directories (`execution/workspaces/<project_id>`) and Git branch-per-feature workflows. Automated QA test gating prior to merge. |
