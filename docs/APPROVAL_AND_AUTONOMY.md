# CODE WIBES TECHNOLOGIES — Approval and Autonomy Policy Engine

**Authority Principle:** Human Founder holds final global authority. No AI agent can grant itself autonomy, approve its own work, or initiate consequential external actions without explicit Founder approval.

---

## 1. Approval Modes

| Mode | Behavior | Execution Permitted? |
|---|---|---|
| **`BLOCKED`** | The action is completely disabled by policy. | ❌ No |
| **`DRAFT_ONLY`** | The agent can formulate a proposal, draft an email, or generate code, but cannot send or execute it. | ❌ No (Draft stored in DB) |
| **`FOUNDER_APPROVAL`** | The agent submits an explicit request to the Founder Approval Inbox. Action waits in queue. | ⏸️ Paused until Founder clicks "Approve" |
| **`AUTO_APPROVED`** | Internal, bounded, low-risk actions (e.g., local tests, classification, summarizing) explicitly permitted by Founder. | ✅ Yes (Within quota limits) |

---

## 2. Hard-Locked Actions Requiring Founder Approval

The following actions are strictly hard-locked and will **never** execute automatically:
1. **Outbound voice calls** to real customers or prospects.
2. **Sending external communications** (email, SMS, WhatsApp, social posts).
3. **Dispatching commercial proposals**, quotations, contracts, or invoices.
4. **Accepting payments** or invoking paid APIs beyond pre-approved budgets.
5. **Production deployments**, DNS modifications, or public website edits.
6. **Modifying security controls**, user roles, database schema, or approval policies.

---

## 3. Global Safety Kill Switches

In `backend/app/models/company_setting.py`:
- **`emergency_pause_all_agents`** (`POST /api/v1/settings/emergency-pause`):
  Immediately halts execution across all 100 AI employees and NEXUS.
- **`disable_external_actions`** (Default: `True`):
  Globally disallows any outbound HTTP requests, emails, calls, or deployments.
- **`allow_production_calling`** (Default: `False`):
  Strict hardware/legal lock preventing any real telephone calls until compliance registration is satisfied.

---

## 4. India Calling & TRAI / TCCCPR Compliance Gate

To comply with Indian commercial communication regulations (Telecom Regulatory Authority of India):
1. **No Cold Scraped Calling**: Simply discovering a phone number on Google Maps does not grant legal permission for promotional robo-calling.
2. **DLT & Principal Entity Registration**: Telephony calling requires registered header, template, and A2P declaration through a licensed Indian telecom provider.
3. **Test Mode Enforcement**: While in development, the calling adapter accepts only verified Founder phone numbers recorded in `founder_verified_phone`. All prospect calls are routed to simulation summaries.
4. **Immediate Opt-Out Suppression**: When an opt-out is requested, the lead is immediately placed in `do_not_contact` status across all future campaigns.
