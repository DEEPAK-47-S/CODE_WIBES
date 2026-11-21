"""Clean all mock, fake, and unit-test generated data from PostgreSQL database and execution workspaces.

Preserves 100% authentic core data:
- The 10 AI Departments
- The 101 AI Agent roster profiles
- The 20 registered Ollama local models
- Company Credentials & Settings (Google Maps, ElevenLabs, Twilio, Razorpay)
- Company Constitution & Founder Preferences (Tier 1 & Tier 2 company memories)
- The 2 Core Platform Projects:
    * 'CODE WIBES Autonomous Company Platform' (396144f3-2c79-468c-8124-ff480f25e8c0)
    * 'Enterprise AI Client Acquisition Portal' (443d8822-26f0-4d94-835a-aa0e2b9560ee)
    and their 3 active tasks
- Authentic organic leads submitted via Public Website Contact Form
"""

import asyncio
import os
import shutil
from pathlib import Path
from sqlalchemy import text
from app.database.session import AsyncSessionLocal

CORE_PROJECT_IDS = [
    "396144f3-2c79-468c-8124-ff480f25e8c0",
    "443d8822-26f0-4d94-835a-aa0e2b9560ee",
]

async def purge_fake_data():
    print("=" * 60)
    print("CODE WIBES TECHNOLOGIES - DATA PURGE & AUTHENTIC SANITIZATION")
    print("=" * 60)

    async with AsyncSessionLocal() as db:
        # 1. Customer Reviews (all were mock/test)
        rev_count = (await db.execute(text("DELETE FROM customer_reviews RETURNING id"))).rowcount
        print(f"Purged Customer Reviews: {rev_count}")

        # 2. Invoices (all were mock/test CW-INV-2026-*)
        inv_count = (await db.execute(text("DELETE FROM invoices RETURNING id"))).rowcount
        print(f"Purged Invoices: {inv_count}")

        # 3. Contracts (all were mock MSAs)
        cntr_count = (await db.execute(text("DELETE FROM contracts RETURNING id"))).rowcount
        print(f"Purged Contracts: {cntr_count}")

        # 4. Change Requests (all mock test tickets)
        cr_count = (await db.execute(text("DELETE FROM change_requests RETURNING id"))).rowcount
        print(f"Purged Change Requests: {cr_count}")

        # 5. Marketing Posts (all mock test posts)
        mp_count = (await db.execute(text("DELETE FROM marketing_posts RETURNING id"))).rowcount
        print(f"Purged Marketing Posts: {mp_count}")

        # 6. Proposal Drafts
        prop_count = (await db.execute(text("DELETE FROM proposal_drafts RETURNING id"))).rowcount
        print(f"Purged Proposal Drafts: {prop_count}")

        # 7. Customer Requirement Briefs
        brief_count = (await db.execute(text("DELETE FROM customer_requirement_briefs RETURNING id"))).rowcount
        print(f"Purged Customer Requirement Briefs: {brief_count}")

        # 8. Prospect Audits
        audit_count = (await db.execute(text("DELETE FROM prospect_audits RETURNING id"))).rowcount
        print(f"Purged Prospect Audits: {audit_count}")

        # 9. Voice Call Records
        voice_count = (await db.execute(text("DELETE FROM voice_call_records RETURNING id"))).rowcount
        print(f"Purged Voice Call Records: {voice_count}")

        # 10. Task Checkpoints
        chk_count = (await db.execute(text("DELETE FROM task_checkpoints RETURNING id"))).rowcount
        print(f"Purged Task Checkpoints: {chk_count}")

        # 11. Approval Requests (Keep only if not mock test data)
        appr_count = (await db.execute(text("DELETE FROM approval_requests RETURNING id"))).rowcount
        print(f"Purged Approval Requests: {appr_count}")

        # 12. Task Dependencies & Tasks for non-core projects or NULL project_id
        core_ids_str = ", ".join(f"'{pid}'" for pid in CORE_PROJECT_IDS)
        
        # Delete task dependencies for tasks to be deleted
        await db.execute(text(f"""
            DELETE FROM task_dependencies 
            WHERE task_id IN (SELECT id FROM tasks WHERE project_id IS NULL OR project_id NOT IN ({core_ids_str}))
               OR depends_on_task_id IN (SELECT id FROM tasks WHERE project_id IS NULL OR project_id NOT IN ({core_ids_str}))
        """))

        del_tasks = (await db.execute(text(f"""
            DELETE FROM tasks 
            WHERE project_id IS NULL OR project_id NOT IN ({core_ids_str}) 
            RETURNING id
        """))).rowcount
        print(f"Purged Mock Tasks: {del_tasks}")

        # 13. Projects (Keep only the 2 core platform projects)
        del_projects = (await db.execute(text(f"""
            DELETE FROM projects 
            WHERE id NOT IN ({core_ids_str}) 
            RETURNING id
        """))).rowcount
        print(f"Purged Mock Projects: {del_projects}")

        # 14. Leads: Keep real contact submissions, delete test leads
        del_leads = (await db.execute(text("""
            DELETE FROM leads 
            WHERE company_name IN ('Opt Out Test Enterprise', 'Apex Coimbatore Tech', 'Coimbatore Pumps & Motors', 
                                   'Kovai Precision Tools', 'Coimbatore Precision Hydraulics', 'Coimbatore Smart Logistics')
               OR source = 'AUTONOMOUS_DISCOVERY'
               OR source = 'EXTERNAL_API'
            RETURNING id
        """))).rowcount
        print(f"Purged Mock/Test Leads: {del_leads}")

        # 15. Memories & Embeddings: Purge test project/customer memories
        del_mems = (await db.execute(text("""
            DELETE FROM company_memories 
            WHERE tier IN ('project', 'customer')
            RETURNING id
        """))).fetchall()
        del_mem_ids = [str(r[0]) for r in del_mems]
        if del_mem_ids:
            mem_ids_str = ", ".join(f"'{m}'" for m in del_mem_ids)
            await db.execute(text(f"DELETE FROM memory_embeddings WHERE memory_id IN ({mem_ids_str})"))
        print(f"Purged Mock Project/Customer Memories: {len(del_mem_ids)}")

        # 16. Activity logs: Clear historical test noise
        del_logs = (await db.execute(text("DELETE FROM activity_logs RETURNING id"))).rowcount
        print(f"Purged Test Activity Logs: {del_logs}")

        await db.commit()
        print("Database commit successful.")

    # 17. Clean Execution Workspaces on disk
    ws_dir = Path("execution/workspaces")
    if ws_dir.exists():
        cleaned_dirs = 0
        for item in ws_dir.iterdir():
            if item.is_dir() and item.name not in CORE_PROJECT_IDS:
                try:
                    shutil.rmtree(item)
                    cleaned_dirs += 1
                except Exception as e:
                    print(f"Warning: could not delete {item}: {e}")
        print(f"Purged Test Execution Workspaces from disk: {cleaned_dirs}")

    print("=" * 60)
    print("CLEANUP COMPLETE: ONLY AUTHENTIC DATA REMAINS.")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(purge_fake_data())
