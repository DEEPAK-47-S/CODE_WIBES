"""D06 Cloud Infrastructure & DevOps Service: Generates production Docker, Nginx, and CI/CD pipelines."""
import json
from pathlib import Path
import uuid
from typing import Any, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.website_factory_service import BASE_WORKSPACE_DIR
from app.services.memory_service import MemoryService


class DevOpsService:
    """Atlas (D06 DevOps Lead) generates containerization, Nginx, and CI/CD deployment files."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.memory = MemoryService(db)

    async def generate_production_devops_bundle(
        self,
        project_id: uuid.UUID,
        project_name: str,
        domain: str = "app.codewibes.com",
    ) -> Dict[str, Any]:
        """Generates Dockerfile, nginx.conf, docker-compose.yml, and GitHub Actions CI/CD."""
        workspace_dir = BASE_WORKSPACE_DIR / str(project_id)
        if not workspace_dir.exists():
            workspace_dir.mkdir(parents=True, exist_ok=True)

        docker_dir = workspace_dir / "docker"
        ci_dir = workspace_dir / ".github" / "workflows"
        docker_dir.mkdir(parents=True, exist_ok=True)
        ci_dir.mkdir(parents=True, exist_ok=True)

        # 1. Multi-stage Production Dockerfile
        dockerfile_content = """# Stage 1: Build Environment
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --silent
COPY . .
RUN npm run build || mkdir -p dist && cp -r public/* dist/

# Stage 2: Production Nginx Server
FROM nginx:1.25-alpine
WORKDIR /usr/share/nginx/html
RUN rm -rf ./*
COPY --from=builder /app/dist .
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
"""
        with open(workspace_dir / "Dockerfile", "w", encoding="utf-8") as f:
            f.write(dockerfile_content)

        # 2. Hardened Nginx Configuration
        nginx_content = f"""server {{
    listen 80;
    server_name {domain} localhost;
    root /usr/share/nginx/html;
    index index.html;

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Permissions-Policy "camera=(), microphone=(), geolocation=()" always;

    # Gzip Compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/json application/javascript application/xml+rss;

    # Single Page App Routing
    location / {{
        try_files $uri $uri/ /index.html;
    }}

    # Cache static assets
    location ~* \\.(?:ico|css|js|gif|jpe?g|png|woff2?|eot|ttf|svg)$ {{
        expires 6M;
        access_log off;
        add_header Cache-Control "public, max-age=15552000, immutable";
    }}
}}
"""
        with open(docker_dir / "nginx.conf", "w", encoding="utf-8") as f:
            f.write(nginx_content)

        # 3. Docker Compose Orchestration
        compose_content = f"""version: '3.8'

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: {project_name.lower().replace(' ', '-')}-web
    ports:
      - "8080:80"
    restart: unless-stopped
    environment:
      - NODE_ENV=production
"""
        with open(workspace_dir / "docker-compose.yml", "w", encoding="utf-8") as f:
            f.write(compose_content)

        # 4. GitHub Actions CI/CD Pipeline
        ci_cd_content = f"""name: Build and Deploy {project_name}

on:
  push:
    branches: [ main, production ]
  pull_request:
    branches: [ main ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node.js 20
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - name: Install Dependencies
        run: npm ci
      - name: Code Quality & Lint
        run: npm run lint --if-present
      - name: Build Application
        run: npm run build
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      - name: Build Docker Container
        run: docker build -t {project_name.lower().replace(' ', '-')}:latest .
"""
        with open(ci_dir / "deploy.yml", "w", encoding="utf-8") as f:
            f.write(ci_cd_content)

        files_generated = [
            "Dockerfile",
            "docker/nginx.conf",
            "docker-compose.yml",
            ".github/workflows/deploy.yml",
        ]

        # Update manifest.json if exists
        manifest_file = workspace_dir / "manifest.json"
        if manifest_file.exists():
            try:
                manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
                manifest.setdefault("files_generated", []).extend(files_generated)
                manifest["devops_ready"] = True
                with open(manifest_file, "w", encoding="utf-8") as f:
                    json.dump(manifest, f, indent=2)
            except Exception:
                pass

        # Record in memory
        await self.memory.store_memory(
            tier="project",
            namespace=f"project:{str(project_id)[:8]}",
            key="devops_deployment_bundle",
            content=f"Atlas (D06 DevOps Lead) generated Dockerfile, Nginx config, docker-compose, and GitHub Actions CI/CD.",
            provenance="D06_DEVOPS_ATLAS",
        )

        return {
            "status": "devops_bundle_generated",
            "project_id": str(project_id),
            "files_generated": files_generated,
            "architecture": "Docker Multi-Stage + Nginx Alpine + GitHub Actions CI/CD",
        }
