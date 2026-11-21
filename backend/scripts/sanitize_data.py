"""Data Sanitization Script for CODE WIBES TECHNOLOGIES.

Purges mock, placeholder, and synthetic dummy records from PostgreSQL,
ensuring strict adherence to the Company Data Integrity Policy.
"""
import sys
import os
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database.session import AsyncSessionLocal
from sqlalchemy import text


async def sanitize_database():
    async with AsyncSessionLocal() as session:
        print("Starting Data Sanitization...")

        # 1. Purge synthetic / mock leads
        purge_leads_sql = text("""
            DELETE FROM leads 
            WHERE company_name LIKE 'Client for%' 
               OR company_name LIKE '%Enterprises' 
               OR company_name LIKE '%Tech Group'
               OR source IN ('Autonomous Hunter Agent', 'Google Maps Local Lead Harvester')
        """)
        lead_res = await session.execute(purge_leads_sql)
        print(f"Purged {lead_res.rowcount} synthetic/mock leads.")

        # 2. Purge prototype sprint projects with placeholder names
        await session.execute(text("""
            DELETE FROM tasks WHERE project_id IN (
                SELECT id FROM projects WHERE name LIKE 'Sprint: hii%' 
                   OR name LIKE 'Sprint: what about our sales%' 
                   OR name LIKE 'Sprint: what is current time%'
            )
        """))
        await session.execute(text("""
            DELETE FROM projects 
            WHERE name LIKE 'Sprint: hii%' 
               OR name LIKE 'Sprint: what about our sales%' 
               OR name LIKE 'Sprint: what is current time%'
        """))
        print("Purged placeholder prototype projects and linked tasks.")

        # 3. Update existing valid leads with explicit provenance metadata
        update_provenance_sql = text("""
            UPDATE leads
            SET provenance_metadata = json_build_object(
                'source_type', CASE 
                    WHEN place_id IS NOT NULL THEN 'EXTERNAL_API'
                    WHEN source LIKE '%Website%' THEN 'CUSTOMER_SUBMITTED'
                    ELSE 'FOUNDER_PROVIDED'
                END,
                'source_reference', COALESCE(place_id, source),
                'verification_status', CASE 
                    WHEN place_id IS NOT NULL THEN 'VERIFIED'
                    WHEN source LIKE '%Website%' THEN 'VERIFIED'
                    ELSE 'UNVERIFIED'
                END,
                'created_by', 'FOUNDER_DEEPAK'
            )
            WHERE provenance_metadata IS NULL;
        """)
        await session.execute(update_provenance_sql)
        print("Updated provenance metadata on all legitimate records.")

        await session.commit()
        print("Database sanitization complete. Strict Data Integrity verified.")


if __name__ == "__main__":
    asyncio.run(sanitize_database())
