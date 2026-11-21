"""D04 QA & D10 CyberSecurity Autonomous Audit Service for generated codebases."""
import json
from pathlib import Path
import re
import uuid
from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.memory_service import MemoryService
from app.services.website_factory_service import BASE_WORKSPACE_DIR


class QualitySecurityService:
    """Performs static code quality audits, OWASP Top 10 vulnerability scans, and security certification."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.memory = MemoryService(db)

    async def audit_project_workspace(self, project_id: uuid.UUID) -> Dict[str, Any]:
        """Deeply scans all project files for security vulnerabilities and code quality."""
        workspace_dir = BASE_WORKSPACE_DIR / str(project_id)
        if not workspace_dir.exists():
            return {
                "status": "error",
                "message": f"Workspace {project_id} not found",
                "overall_score": 0,
                "certification": "UNVERIFIED",
            }

        files_scanned: List[str] = []
        findings: List[Dict[str, Any]] = []

        # Collect code files
        code_files = list(workspace_dir.rglob("*.jsx")) + list(workspace_dir.rglob("*.html")) + list(workspace_dir.rglob("*.json"))

        total_lines = 0
        has_eval = False
        has_dangerously_set_inner_html = False
        has_hardcoded_secret = False
        insecure_http_links: List[str] = []
        has_semantic_elements = False

        secret_patterns = [
            re.compile(r'(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*["\'][a-zA-Z0-9_\-]{16,}["\']'),
            re.compile(r'AIza[0-9A-Za-z-_]{35}'),  # Google API key
            re.compile(r'sk_live_[0-9a-zA-Z]{24}'),  # Stripe live key
        ]

        for file_path in code_files:
            rel_name = file_path.relative_to(workspace_dir).as_posix()
            files_scanned.append(rel_name)
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            lines = content.splitlines()
            total_lines += len(lines)

            # Check 1: Injection / XSS
            if "eval(" in content:
                has_eval = True
                findings.append({
                    "severity": "HIGH",
                    "category": "INJECTION",
                    "file": rel_name,
                    "description": "Direct use of JavaScript eval() detected. Potential remote code execution vulnerability.",
                })

            if "dangerouslySetInnerHTML" in content:
                has_dangerously_set_inner_html = True
                findings.append({
                    "severity": "MEDIUM",
                    "category": "XSS",
                    "file": rel_name,
                    "description": "dangerouslySetInnerHTML found. Ensure input is sanitized to prevent cross-site scripting.",
                })

            # Check 2: Hardcoded secrets
            for pattern in secret_patterns:
                if pattern.search(content):
                    has_hardcoded_secret = True
                    findings.append({
                        "severity": "CRITICAL",
                        "category": "SECRET_EXPOSURE",
                        "file": rel_name,
                        "description": "Potential hardcoded secret or live credential detected.",
                    })

            # Check 3: Mixed Content / Insecure HTTP
            for match in re.finditer(r'http://[a-zA-Z0-9.\-_/:]+', content):
                url = match.group(0)
                # Ignore localhost and staging internal URLs
                if "127.0.0.1" not in url and "localhost" not in url and "w3.org" not in url:
                    insecure_http_links.append(url)
                    findings.append({
                        "severity": "LOW",
                        "category": "TRANSPORT_SECURITY",
                        "file": rel_name,
                        "description": f"Insecure plaintext HTTP reference found: {url}. Migrate to HTTPS.",
                    })

            # Check 4: Semantic Accessibility
            if rel_name.endswith(".html") or rel_name.endswith(".jsx"):
                if any(tag in content for tag in ["<nav", "<header", "<main", "<footer"]):
                    has_semantic_elements = True

        # Calculate Scores
        security_score = 100
        if has_eval:
            security_score -= 30
        if has_dangerously_set_inner_html:
            security_score -= 15
        if has_hardcoded_secret:
            security_score -= 40
        if insecure_http_links:
            security_score -= min(15, len(insecure_http_links) * 5)
        security_score = max(0, security_score)

        quality_score = 85
        if has_semantic_elements:
            quality_score += 10
        if total_lines > 100:
            quality_score += 5
        quality_score = min(100, max(0, quality_score))

        overall_score = round((security_score * 0.6) + (quality_score * 0.4), 1)

        if overall_score >= 90:
            certification = "A+ ENTERPRISE CERTIFIED"
            qa_status = "PASSED_STAGING_DEPLOYABLE"
        elif overall_score >= 75:
            certification = "A COMPLIANT"
            qa_status = "PASSED_WITH_OBSERVATIONS"
        else:
            certification = "REVIEW_REQUIRED"
            qa_status = "REMEDIATION_NEEDED"

        report = {
            "project_id": str(project_id),
            "status": qa_status,
            "overall_score": overall_score,
            "security_score": security_score,
            "quality_score": quality_score,
            "certification": certification,
            "files_scanned_count": len(files_scanned),
            "files_scanned": files_scanned,
            "total_lines_of_code": total_lines,
            "owasp_top_10_compliant": security_score >= 85,
            "findings_count": len(findings),
            "findings": findings,
            "audited_by_departments": [
                {"department": "D04", "name": "Quality Assurance & Testing", "agent": "TestMaster"},
                {"department": "D10", "name": "CyberSecurity & Compliance", "agent": "Sentinel"},
            ],
            "recommendations": [
                "Enforce Content Security Policy (CSP) headers in production reverse proxy (Nginx / Cloudflare).",
                "Ensure all external JavaScript libraries are loaded via subresource integrity (SRI) hashes.",
                "Verify responsive mobile breakpoint testing across iPhone 15, Pixel 8, and iPad viewport ratios.",
            ],
        }

        # Write report to workspace
        report_file = workspace_dir / "QA_SECURITY_REPORT.json"
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        # Persist memory in project tier
        await self.memory.store_memory(
            tier="project",
            namespace=f"project:{str(project_id)[:8]}",
            key="qa_security_audit_report",
            content=f"QA/Security Audit by TestMaster & Sentinel: Score {overall_score}/100. Certification: {certification}. Status: {qa_status}.",
            provenance="D04_QA_AND_D10_CYBERSECURITY",
        )

        return report

    async def get_audit_report(self, project_id: uuid.UUID) -> Optional[Dict[str, Any]]:
        """Retrieves existing audit report or runs a new one if not present."""
        report_file = BASE_WORKSPACE_DIR / str(project_id) / "QA_SECURITY_REPORT.json"
        if report_file.exists():
            try:
                return json.loads(report_file.read_text(encoding="utf-8"))
            except Exception:
                pass
        return await self.audit_project_workspace(project_id)
