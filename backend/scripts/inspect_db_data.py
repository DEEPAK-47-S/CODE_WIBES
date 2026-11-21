import asyncio
import sys
from pathlib import Path

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import text
from app.database.session import AsyncSessionLocal

async def main():
    async with AsyncSessionLocal() as session:
        tables = [
            "leads", "projects", "tasks", "invoices", "contracts", 
            "customer_reviews", "marketing_posts", "company_memories",
            "prospect_audits", "proposal_drafts", "customer_requirement_briefs"
        ]
        print("--- DATABASE TABLE COUNTS ---")
        for table in tables:
            try:
                res = await session.execute(text(f"SELECT count(*) FROM {table}"))
                print(f"{table}: {res.scalar()}")
            except Exception as e:
                print(f"{table}: ERROR ({e})")

        print("\n--- INVOICES ---")
        try:
            invs = await session.execute(text("SELECT invoice_number, client_name, total_amount, status FROM invoices LIMIT 10"))
            for inv in invs:
                print(dict(inv._mapping))
        except Exception as e:
            print(f"Invoices error: {e}")

        print("\n--- LEADS ---")
        try:
            leads = await session.execute(text("SELECT company_name, source, status FROM leads LIMIT 10"))
            for lead in leads:
                print(dict(lead._mapping))
        except Exception as e:
            print(f"Leads error: {e}")

        print("\n--- PROJECTS ---")
        try:
            projs = await session.execute(text("SELECT name, status FROM projects LIMIT 10"))
            for proj in projs:
                print(dict(proj._mapping))
        except Exception as e:
            print(f"Projects error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
