import asyncio
from sqlalchemy import select
from app.database.session import AsyncSessionLocal
from app.models.agent import Agent

AGENT_MODELS = {
    "Nexus": ("llama3.1:latest", "Chief Executive Officer (CEO)"),
    "Forge": ("qwen2.5-coder:3b", "Chief Technology Officer & Lead Full-Stack Engineer"),
    "Hunter": ("llama3.1:latest", "Head of B2B Lead Generation & Sales"),
    "Echo": ("gemma3:4b", "Head of Digital Marketing & Brand Strategy"),
    "Atlas": ("qwen3.5:4b", "Senior Technical Project Manager (COO)"),
    "Sentinel": ("qwen2.5-coder:3b", "Lead QA & Cybersecurity Auditor"),
    "Aura": ("gemma3:4b", "Principal UI/UX Architect"),
    "Ledger": ("qwen3.5:2b", "Head of Finance & Operations"),
}

async def update_agents():
    async with AsyncSessionLocal() as db:
        res = await db.execute(select(Agent))
        agents = res.scalars().all()
        for a in agents:
            if a.name in AGENT_MODELS:
                model, role = AGENT_MODELS[a.name]
                a.model_name = model
                a.role = role
                print(f"Updated {a.name} -> Model: {model}, Role: {role}")
        await db.commit()
        print("All agents updated in PostgreSQL successfully!")

if __name__ == "__main__":
    asyncio.run(update_agents())
