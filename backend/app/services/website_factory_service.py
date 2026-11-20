"""Website & App Factory Service generating isolated client workspaces and verified builds."""
from pathlib import Path
import json
import uuid
from typing import Any, Dict, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.services.audit_service import AuditService

BASE_WORKSPACE_DIR = Path(__file__).resolve().parents[3] / "execution" / "workspaces"


class WebsiteFactoryService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.audit = AuditService(db)

    async def create_isolated_project_workspace(
        self,
        project_id: uuid.UUID,
        project_name: str,
        tech_stack: str = "React + FastAPI + PostgreSQL",
    ) -> Dict[str, Any]:
        """Create a dedicated, isolated project workspace directory for agent code generation."""
        workspace_dir = BASE_WORKSPACE_DIR / str(project_id)
        workspace_dir.mkdir(parents=True, exist_ok=True)

        # Structure: src, public, docs, tests
        (workspace_dir / "src").mkdir(exist_ok=True)
        (workspace_dir / "public").mkdir(exist_ok=True)
        (workspace_dir / "tests").mkdir(exist_ok=True)

        # Generate workspace manifest
        manifest = {
            "project_id": str(project_id),
            "project_name": project_name,
            "tech_stack": tech_stack,
            "staging_preview_url": f"http://127.0.0.1:8000/staging/{project_id}",
            "git_branch": f"feature/project-{str(project_id)[:8]}",
            "status": "initialized",
        }
        with open(workspace_dir / "manifest.json", "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        # Generate verified index.html
        index_html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{project_name} — Built by CODE WIBES</title>
  <style>
    body {{ font-family: system-ui, sans-serif; background: #101827; color: #F3F4F6; margin: 0; padding: 40px; }}
    .container {{ max-width: 900px; margin: 0 auto; background: #1F2937; padding: 32px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.4); }}
    h1 {{ color: #60A5FA; }}
    .badge {{ background: #2563EB; color: white; padding: 4px 12px; border-radius: 9999px; font-size: 14px; font-weight: 600; }}
  </style>
</head>
<body>
  <div class="container">
    <span class="badge">CODE WIBES Verified Staging Build</span>
    <h1>{project_name}</h1>
    <p>Architecture: <strong>{tech_stack}</strong></p>
    <p>Engineered autonomously by Forge (CTO) & Sentinel (QA Auditor).</p>
  </div>
</body>
</html>"""
        with open(workspace_dir / "public" / "index.html", "w", encoding="utf-8") as f:
            f.write(index_html_content)

        await self.audit.log_event(
            actor_type="agent",
            action="workspace_created",
            resource_type="project_workspace",
            resource_id=project_id,
            details={"path": str(workspace_dir), "project_name": project_name},
            risk_level="MEDIUM",
        )

        return {
            "status": "workspace_ready",
            "project_id": str(project_id),
            "workspace_path": str(workspace_dir),
            "staging_preview_url": manifest["staging_preview_url"],
            "git_branch": manifest["git_branch"],
        }
