# CODE WIBES TECHNOLOGIES — Persistent 7-Tier Memory & Checkpoint System

**Key Principle:** *Context length is not permanent memory.* Model context windows are transient and bounded. Permanent company, agent, and project knowledge resides authoritatively in PostgreSQL outside the model context.

---

## 1. The 7 Memory Tiers

```
Tier 1: Constitution (Company brand, immutable rules, authority hierarchy)
  │
Tier 2: Founder Preferences (Operating directives, risk tolerances, confirmed approvals)
  │
Tier 3: Department SOPs (Standard operating procedures, allowed tools, quality rubrics)
  │
Tier 4: Agent Memory (Role-specific instructions, successful task patterns)
  │
Tier 5: Project Memory (Customer brief, architectural decisions, milestones, tests)
  │
Tier 6: Task Memory (Input arguments, execution artifacts, error traces, run logs)
  │
Tier 7: Customer Memory (Tenant-isolated requirements, approved assets, opt-out status)
```

---

## 2. Context Checkpoint & Continuation Engine

When an agent executes a multi-step task, token consumption is monitored:
1. **Trigger Threshold:** Evaluated by `MemoryService.should_trigger_checkpoint()`. When tokens hit **65% to 75%** of the context budget (e.g. ~5,700 tokens of an 8,192 budget).
2. **Checkpoint Generation:**
   - Goal statement
   - Completed work summary
   - Key architectural decisions made
   - Verified facts
   - Open questions
   - Exact next steps
   - Associated file paths and commit hashes
3. **Continuation Run:**
   - The current context session is concluded safely.
   - A fresh model context is initialized, seeded only with the latest checkpoint summary and relevant retrieved memories.
   - The task resumes seamlessly with the original `task_id` and audit trail intact.
   - **Zero data loss, zero infinite loops, zero model reinstalls.**
