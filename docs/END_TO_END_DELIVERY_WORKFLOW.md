# CODE WIBES TECHNOLOGIES — End-to-End Delivery Workflow

**Brand:** CODE WIBES TECHNOLOGIES  
**Tagline:** *Turning Ideas Into Digital Solutions.*  
**Delivery Model:** Fully traceable, durable pipeline from Customer Brief to QA, Staging, and Production.

---

## 1. The 10-Stage Delivery Workflow

```mermaid
graph TD
    S1["1. Territory & Lead Discovery<br/>(Places API Deduplication & No-Website Trick)"] --> S2["2. Lead Qualification & Scoring<br/>(Evidence-based Score & Audit)"]
    S2 --> S3["3. Compliant Voice Outreach<br/>(ElevenLabs Test Mode / TRAI Compliance Gate)"]
    S3 --> S4["4. Requirement Discovery<br/>(CustomerRequirementBrief Schema)"]
    S4 --> S5["5. Proposal & Estimation<br/>(Milestones, Acceptance Criteria, Hours)"]
    S5 --> S6{"Founder Approval Gate<br/>(ApprovalRequest Inbox)"}
    S6 -- Rejected --> S5
    S6 -- Approved --> S7["7. Isolated Workspace & Factory<br/>(execution/workspaces/project_id)"]
    S7 --> S8["8. Multi-Department Engineering<br/>(UI/UX Design Tokens -> Backend APIs -> React)"]
    S8 --> S9["9. QA & Security Audit<br/>(Sentinel OWASP Top 10 + Automated Smoke Tests)"]
    S9 --> S10["10. Staging Preview & Live Release<br/>(Founder Production Release Gate)"]
```

---

## 2. Milestone and Financial Breakdown

Every generated proposal includes transparent milestones:
* **M1 (25%): Discovery & UI/UX Wireframes** — Sitemap, responsive design tokens, and user flow.
* **M2 (45%): Full-Stack Software Engineering** — FastAPI endpoints, PostgreSQL queries, and React frontend.
* **M3 (15%): QA, Accessibility & Security Audit** — Zero OWASP Top 10 defects, responsive verification.
* **M4 (15%): Staging Review & Production Deployment** — Client staging link and production release.

---

## 3. Isolated Client Workspace Isolation

Every project is allocated an isolated directory:
`execution/workspaces/<project_id>/`
- `manifest.json`: Project metadata, tech stack, and git feature branch.
- `src/`: Client source code.
- `public/`: Assets and verified staging `index.html`.
- `tests/`: Automated contract and unit tests.
