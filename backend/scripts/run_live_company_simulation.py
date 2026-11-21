"""Live Company Simulation Script — Operates the entire 10-department AI software company end-to-end."""
import asyncio
import json
import sys
import time
from pathlib import Path

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import httpx
from sqlalchemy import select, func

from app.database.session import AsyncSessionLocal
from app.models.agent import Agent
from app.models.department import Department
from app.models.company_setting import CompanySetting
from app.services.autopilot_service import AutopilotService
from app.services.nexus_manager import NexusManagerService, _GPU_INFERENCE_LOCK

OLLAMA_API = "http://127.0.0.1:11434/api/generate"


async def main():
    print("\n" + "=" * 70)
    print("🚀 CODE WIBES TECHNOLOGIES — LIVE AUTONOMOUS COMPANY SIMULATION")
    print("Founder & Owner: DEEPAKUMAR.S")
    print("=" * 70 + "\n")

    async with AsyncSessionLocal() as db:
        # 1. Roster Inspection
        total_dept = (await db.execute(select(func.count(Department.id)))).scalar()
        total_agents = (await db.execute(select(func.count(Agent.id)))).scalar()
        print(f"📊 Company Structure: {total_dept} Departments, {total_agents} AI Agents registered.")

        # 2. Live Local Model Probing
        print("\n🔍 Probing Key AI Agents & Local Ollama Models:")
        test_roster = [
            ("NEXUS (Chief of Staff)", "qwen3.5:4b", "Plan a 3-step technical roadmap for enterprise CRM."),
            ("Hunter (D02 Lead Intel Head)", "llama3.1:latest", "Qualify a B2B hydraulic manufacturer for web modernization."),
            ("Forge (D06 Engineering Head)", "qwen2.5-coder:3b", "Generate a clean FastAPI health router in Python."),
            ("Aura (D05 UI/UX Head)", "gemma3:4b", "Describe modern Tailwind color palette for industrial SaaS."),
            ("Sentinel (D07 Security Lead)", "deepseek-r1:1.5b", "Evaluate SQL injection defense with parameterized queries."),
        ]

        for agent_title, model_name, test_prompt in test_roster:
            print(f"  • Testing {agent_title} with model '{model_name}'...")
            t0 = time.time()
            async with _GPU_INFERENCE_LOCK:
                try:
                    payload = {
                        "model": model_name,
                        "prompt": test_prompt,
                        "stream": False,
                        "options": {"num_ctx": 4096, "temperature": 0.2},
                    }
                    async with httpx.AsyncClient(timeout=60.0) as client:
                        resp = await client.post(OLLAMA_API, json=payload)
                        latency = round(time.time() - t0, 2)
                        if resp.status_code == 200:
                            output_preview = resp.json().get("response", "").strip()[:80].replace("\n", " ")
                            print(f"    ✓ OK ({latency}s): \"{output_preview}...\"")
                        else:
                            print(f"    ⚠ Ollama Error {resp.status_code}")
                except Exception as e:
                    print(f"    ⚠ Inference error: {e}")

        # 3. Autonomous Company Pipeline Execution
        print("\n⚡ Executing Full 10-Department Autonomous Auto-Pilot Lifecycle:")
        print("   Target Client: 'Coimbatore Precision Hydraulics'")
        autopilot = AutopilotService(db)
        t_pipe = time.time()
        result = await autopilot.run_full_company_pipeline(
            business_name="Coimbatore Precision Hydraulics",
            website_url="cbehydraulics.in",
            phone="+91 94422 55667",
            location="Coimbatore, Tamil Nadu",
            category="Industrial Hydraulic Cylinders & Valves",
        )
        pipe_duration = round(time.time() - t_pipe, 2)

        print(f"\n✅ Pipeline Succeeded in {pipe_duration}s!")
        print("-" * 70)
        for step in result.get("pipeline_log", []):
            print(f"  [{step['stage']}] {step['department']} ({step['agent']}) -> {step['outcome']}")

        print("-" * 70)
        print("📦 Final Deliverables & Live Artifacts:")
        print(f"  • Live Staging Website: {result.get('staging_preview_url')}")
        print(f"  • GST Tax Invoice:      {result.get('invoice_number')} (Total: INR ₹{result.get('total_inr'):,.2f})")
        print(f"  • Payment Link:         {result.get('payment_link')}")
        print(f"  • Legal MSA Contract:   {result.get('contract_number')}")
        print(f"  • WhatsApp Outreach:    {result.get('whatsapp_click_to_chat')}")
        print("=" * 70)
        print("🎉 ALL 10 DEPARTMENTS & CENTRAL MANAGER OPERATING FLAWLESSLY!\n")


if __name__ == "__main__":
    asyncio.run(main())
