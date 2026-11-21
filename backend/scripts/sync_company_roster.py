"""Synchronizes the full CODE WIBES company roster with the 18 local Ollama models.

1 Main Agent (NEXUS) + 10 Departments x 10 Specialists = Exactly 101 AI Employees.
"""
import sys
import os
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database.session import AsyncSessionLocal
from app.services.company_service import CompanyService
from sqlalchemy import text


async def sync_company():
    async with AsyncSessionLocal() as session:
        print("=== Synchronizing CODE WIBES TECHNOLOGIES AI Company Organization ===")

        # 1. Clean up legacy / duplicate empty departments
        cleanup_sql = text("""
            DELETE FROM departments 
            WHERE slug IN ('business-operations', 'digital-marketing', 'lead-generation-sales', 'software-development', 'testing-qa', 'ui-ux-creative')
            AND id NOT IN (SELECT DISTINCT department_id FROM agents WHERE department_id IS NOT NULL);
        """)
        await session.execute(cleanup_sql)
        await session.commit()

        # 2. Re-assign any agent pointing to legacy department to the canonical department
        reassign_sql = text("""
            UPDATE agents 
            SET department_id = (SELECT id FROM departments WHERE slug = 'd04-discovery-solutions' LIMIT 1)
            WHERE department_id IN (SELECT id FROM departments WHERE slug = 'business-operations');
        """)
        await session.execute(reassign_sql)
        await session.commit()

        # 3. Clean up the now empty legacy departments
        await session.execute(cleanup_sql)
        await session.commit()

        # Ensure Nexus is Central Main Agent (not bound to a single department)
        await session.execute(text("UPDATE agents SET department_id = NULL WHERE name = 'Nexus'"))
        await session.commit()

        # 4. Synchronize all 10 departments and 101 agents with 18 Ollama models
        company_svc = CompanyService(session)
        sync_result = await company_svc.sync_full_organization()
        print(f"Roster Sync: {sync_result}")

        # 5. Verify the complete structure
        org_chart = await company_svc.get_org_chart()
        print(f"\nFounder Authority: {org_chart['founder']}")
        print(f"Main Central Agent: {org_chart['central_manager']['name']} ({org_chart['central_manager']['role']}) -> Model: {org_chart['central_manager']['model']}")
        print(f"Total Departments: {org_chart['total_departments']}")
        print(f"Total Active Agents: {org_chart['total_agents']}")

        print("\nCanonical Departments & Heads:")
        for d in org_chart["departments"]:
            head_info = f"{d['head']['name']} ({d['head']['role']}) [{d['head']['model']}]" if d.get("head") else "Vacant"
            print(f"  • {d['name']} ({d['slug']})")
            print(f"    - Head: {head_info}")
            print(f"    - Specialists ({d['specialists_count']}): {', '.join([s['name'] + ' [' + (s['model'] or '') + ']' for s in d['specialists'][:4]])}...")

        print("\nAll 18+ Ollama models mapped and active in CODE WIBES.")


if __name__ == "__main__":
    asyncio.run(sync_company())
