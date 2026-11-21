"""Website & App Factory Service generating isolated client workspaces, multi-file codebases, and live builds."""
from pathlib import Path
import json
import uuid
import zipfile
from typing import Any, Dict, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.services.audit_service import AuditService

BASE_WORKSPACE_DIR = Path(__file__).resolve().parents[3] / "execution" / "workspaces"


class WebsiteFactoryService:
    """Manages multi-file client project generation, live previews, and deployment packaging."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.audit = AuditService(db)

    async def create_isolated_project_workspace(
        self,
        project_id: uuid.UUID,
        project_name: str,
        tech_stack: str = "React + Tailwind + FastAPI",
        pages: Optional[List[str]] = None,
        features: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Creates complete multi-file project codebase with runnable staging preview."""
        workspace_dir = BASE_WORKSPACE_DIR / str(project_id)
        src_dir = workspace_dir / "src"
        components_dir = src_dir / "components"
        public_dir = workspace_dir / "public"
        
        components_dir.mkdir(parents=True, exist_ok=True)
        public_dir.mkdir(parents=True, exist_ok=True)

        pages = pages or ["Home", "Services", "Portfolio", "Contact"]
        features = features or ["Interactive Hero", "Service Catalog", "Contact Form", "Mobile Navigation"]

        # 1. Package.json
        pkg_json = {
            "name": f"client-{str(project_id)[:8]}",
            "version": "1.0.0",
            "private": True,
            "scripts": {"dev": "vite", "build": "vite build", "preview": "vite preview"},
            "dependencies": {
                "react": "^18.3.1",
                "react-dom": "^18.3.1",
                "lucide-react": "^0.395.0",
                "tailwindcss": "^3.4.4",
            },
        }
        with open(workspace_dir / "package.json", "w", encoding="utf-8") as f:
            json.dump(pkg_json, f, indent=2)

        # 2. Components
        navbar_code = f"""// src/components/Navbar.jsx
import React, {{{{ useState }}}} from 'react';

export default function Navbar() {{{{
  const [open, setOpen] = useState(false);
  return (
    <nav className="bg-slate-900 border-b border-slate-800 text-white px-6 py-4 flex justify-between items-center sticky top-0 z-50">
      <div className="font-bold text-xl tracking-tight text-blue-400">{project_name}</div>
      <div className="hidden md:flex space-x-6">
        {" ".join([f'<a href="#{p.lower().replace(" ", "-")}" className="hover:text-blue-400 transition">{p}</a>' for p in pages])}
      </div>
      <button className="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-lg font-medium text-sm transition">
        Get Started
      </button>
    </nav>
  );
}}}}
"""
        with open(components_dir / "Navbar.jsx", "w", encoding="utf-8") as f:
            f.write(navbar_code)

        hero_code = f"""// src/components/Hero.jsx
import React from 'react';

export default function Hero() {{{{
  return (
    <section className="bg-gradient-to-b from-slate-900 to-slate-800 text-white py-20 px-6 text-center">
      <div className="max-w-4xl mx-auto">
        <span className="bg-blue-900/60 text-blue-300 border border-blue-700/50 px-3 py-1 rounded-full text-xs font-semibold tracking-wide uppercase">
          Autonomous Digital Delivery
        </span>
        <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight mt-6 mb-6">
          Empowering <span className="text-blue-400">{project_name}</span> with Next-Gen Technology
        </h1>
        <p className="text-lg md:text-xl text-slate-300 mb-8 max-w-2xl mx-auto leading-relaxed">
          Crafted by CODE WIBES TECHNOLOGIES. High-performance, mobile-first, and built for conversion.
        </p>
        <div className="flex justify-center gap-4">
          <a href="#contact" className="bg-blue-600 hover:bg-blue-500 px-6 py-3 rounded-lg font-semibold transition">
            Book Consultation
          </a>
          <a href="#services" className="bg-slate-800 hover:bg-slate-700 border border-slate-700 px-6 py-3 rounded-lg font-semibold transition">
            Explore Features
          </a>
        </div>
      </div>
    </section>
  );
}}}}
"""
        with open(components_dir / "Hero.jsx", "w", encoding="utf-8") as f:
            f.write(hero_code)

        # 3. Main App.jsx
        app_code = f"""// src/App.jsx
import React from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';

export default function App() {{{{
  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col font-sans">
      <Navbar />
      <Hero />
      <footer className="mt-auto py-8 text-center text-slate-500 text-sm border-t border-slate-800">
        © 2026 {project_name}. Powered by CODE WIBES.
      </footer>
    </div>
  );
}}}}
"""
        with open(src_dir / "App.jsx", "w", encoding="utf-8") as f:
            f.write(app_code)

        # 4. Verified Standalone Staging index.html (Runs instantly in iframe)
        preview_html = f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{project_name} — CODE WIBES Staging Preview</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col font-sans">
  <!-- Top Staging Badge -->
  <div class="bg-blue-600 text-white text-xs py-1.5 px-4 text-center font-semibold flex justify-between items-center">
    <span>🚀 LIVE STAGING PREVIEW — Built by CODE WIBES TECHNOLOGIES</span>
    <span class="bg-blue-800 px-2 py-0.5 rounded text-[10px]">Verified Build</span>
  </div>

  <!-- Navbar -->
  <header class="border-b border-slate-800 bg-slate-900/90 backdrop-blur sticky top-0 z-50 px-6 py-4 flex justify-between items-center">
    <div class="font-extrabold text-xl tracking-tight text-blue-400 flex items-center gap-2">
      <i class="fa-solid fa-cube"></i> {project_name}
    </div>
    <nav class="hidden md:flex gap-6 text-sm font-medium text-slate-300">
      {"".join([f'<a href="#{p.lower().replace(" ", "-")}" class="hover:text-blue-400 transition">{p}</a>' for p in pages])}
    </nav>
    <a href="#contact" class="bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold px-4 py-2 rounded-lg transition shadow-md shadow-blue-600/20">
      Contact Us
    </a>
  </header>

  <!-- Hero Section -->
  <main class="flex-1">
    <section class="py-20 px-6 text-center max-w-4xl mx-auto">
      <span class="inline-block bg-blue-950 border border-blue-800 text-blue-300 text-xs px-3 py-1 rounded-full font-semibold uppercase tracking-wider mb-6">
        Next-Generation Web Platform
      </span>
      <h1 class="text-4xl md:text-6xl font-extrabold text-white leading-tight mb-6">
        Accelerating Success for <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-400">{project_name}</span>
      </h1>
      <p class="text-slate-400 text-lg mb-8 max-w-2xl mx-auto">
        Fully responsive, search-optimized, and engineered with modern cloud architecture.
      </p>
      <div class="flex flex-wrap justify-center gap-4">
        <a href="#contact" class="bg-blue-600 hover:bg-blue-500 text-white px-6 py-3 rounded-lg font-semibold text-sm transition">
          Get Started Today
        </a>
        <a href="#services" class="bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 px-6 py-3 rounded-lg font-semibold text-sm transition">
          View Solutions
        </a>
      </div>
    </section>

    <!-- Features Section -->
    <section id="services" class="py-16 bg-slate-900/50 border-y border-slate-800/80 px-6">
      <div class="max-w-5xl mx-auto">
        <h2 class="text-2xl md:text-3xl font-bold text-center mb-12">Core Capabilities</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {"".join([f'''
          <div class="bg-slate-900 border border-slate-800 p-6 rounded-xl hover:border-blue-500/50 transition">
            <div class="w-10 h-10 bg-blue-900/50 text-blue-400 rounded-lg flex items-center justify-center mb-4">
              <i class="fa-solid fa-check-circle"></i>
            </div>
            <h3 class="font-bold text-base text-white mb-2">{f}</h3>
            <p class="text-xs text-slate-400">High-performance modern implementation tailored for {project_name}.</p>
          </div>
          ''' for f in features])}
        </div>
      </div>
    </section>

    <!-- Contact Form Section -->
    <section id="contact" class="py-16 px-6 max-w-xl mx-auto text-center">
      <h2 class="text-2xl font-bold mb-4">Inquire or Request Quote</h2>
      <p class="text-slate-400 text-sm mb-6">Leave a message and our team will get back to you within 24 hours.</p>
      <form class="space-y-4 text-left" onsubmit="event.preventDefault(); alert('Demo Form Submitted!');">
        <div>
          <label class="block text-xs font-semibold text-slate-300 mb-1">Your Name</label>
          <input type="text" required placeholder="John Doe" class="w-full bg-slate-900 border border-slate-800 rounded-lg px-4 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500">
        </div>
        <div>
          <label class="block text-xs font-semibold text-slate-300 mb-1">Email or Phone</label>
          <input type="text" required placeholder="contact@example.com" class="w-full bg-slate-900 border border-slate-800 rounded-lg px-4 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500">
        </div>
        <button type="submit" class="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 rounded-lg text-sm transition">
          Submit Inquiry
        </button>
      </form>
    </section>
  </main>

  <footer class="border-t border-slate-800 py-6 text-center text-xs text-slate-500">
    © 2026 {project_name}. Developed autonomously by CODE WIBES TECHNOLOGIES.
  </footer>
</body>
</html>"""
        with open(public_dir / "index.html", "w", encoding="utf-8") as f:
            f.write(preview_html)

        manifest = {
            "project_id": str(project_id),
            "project_name": project_name,
            "tech_stack": tech_stack,
            "pages": pages,
            "features": features,
            "staging_preview_url": f"http://127.0.0.1:8000/staging/{project_id}",
            "git_branch": f"feature/project-{str(project_id)[:8]}",
            "files_generated": [
                "package.json",
                "src/App.jsx",
                "src/components/Navbar.jsx",
                "src/components/Hero.jsx",
                "public/index.html",
            ],
            "status": "ready",
        }
        with open(workspace_dir / "manifest.json", "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        return {
            "status": "codebase_ready",
            "project_id": str(project_id),
            "workspace_path": str(workspace_dir),
            "staging_preview_url": manifest["staging_preview_url"],
            "git_branch": manifest["git_branch"],
            "files_generated": manifest["files_generated"],
        }

    async def get_staging_html(self, project_id: uuid.UUID) -> str:
        """Returns the runnable HTML staging preview for direct iframe rendering."""
        index_file = BASE_WORKSPACE_DIR / str(project_id) / "public" / "index.html"
        if index_file.exists():
            return index_file.read_text(encoding="utf-8")
        return f"<h1>Staging preview not generated for project {project_id}</h1>"

    async def export_project_zip(self, project_id: uuid.UUID) -> Path:
        """Packages the workspace files into a deployable zip archive."""
        workspace_dir = BASE_WORKSPACE_DIR / str(project_id)
        if not workspace_dir.exists():
            raise ValueError(f"Workspace for project {project_id} does not exist.")

        zip_path = workspace_dir / f"project-{str(project_id)[:8]}.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file_path in workspace_dir.rglob("*"):
                if file_path.is_file() and file_path != zip_path:
                    arcname = file_path.relative_to(workspace_dir)
                    zipf.write(file_path, arcname)
        return zip_path
