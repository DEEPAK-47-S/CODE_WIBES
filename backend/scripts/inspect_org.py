import sys
import os
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database.session import AsyncSessionLocal
from sqlalchemy import text


async def inspect_org():
    async with AsyncSessionLocal() as session:
        dept_count = (await session.execute(text("SELECT count(*) FROM departments"))).scalar()
        depts = (await session.execute(text("SELECT id, name, slug FROM departments ORDER BY name"))).fetchall()
        agent_count = (await session.execute(text("SELECT count(*) FROM agents"))).scalar()
        agents = (await session.execute(text("SELECT a.name, a.role, d.name, a.model_name FROM agents a LEFT JOIN departments d ON a.department_id = d.id ORDER BY d.name, a.name"))).fetchall()
        
        print(f"Total Departments: {dept_count}")
        for d in depts:
            dept_agents = [a for a in agents if a[2] == d[1]]
            print(f"  [{d[2]}] {d[1]} -> {len(dept_agents)} employees")
        
        central_agents = [a for a in agents if a[2] is None or 'NEXUS' in a[0].upper() or 'NEXUS' in a[1].upper()]
        print(f"\nCentral / Unassigned / Main Agents ({len(central_agents)}):")
        for a in central_agents:
            print(f"  ★ {a[0]} ({a[1]}) - Model: {a[3]}")

        print(f"\nTotal Agents in Database: {agent_count}")
        
        # Detail D04
        d04_agents = (await session.execute(text("SELECT a.name, a.role FROM agents a JOIN departments d ON a.department_id = d.id WHERE d.slug = 'd04-discovery-solutions'"))).fetchall()
        print(f"\nD04 Discovery Solutions Agents ({len(d04_agents)}):")
        for a in d04_agents:
            print(f"  - {a[0]} ({a[1]})")

if __name__ == "__main__":
    asyncio.run(inspect_org())
