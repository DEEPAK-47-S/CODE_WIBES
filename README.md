# CODE WIBES 🚀

> **Autonomous AI-Operated Software Company Operating System**  
> *Architected for autonomous agent orchestration, departmental coordination, high-precision B2B lead acquisition, and end-to-end software delivery.*

---

## 📌 Overview

**CODE WIBES** is an enterprise-grade AI operating platform that simulates and runs an entire software agency/company with autonomous AI agents. Powered by local high-performance LLMs running via **Ollama**, an asynchronous **FastAPI + PostgreSQL** backend, and a modern **React 19 + TypeScript** dashboard, CODE WIBES manages strategic planning, software engineering, marketing, financial auditing, and automated sales client acquisition without third-party API dependencies.

---

## 🏗️ Architecture & Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React 19, Vite, TypeScript, TanStack Query, Axios, Lucide Icons |
| **Backend** | Python 3.12+, FastAPI, SQLAlchemy 2.0 (Async), Asyncpg, Pydantic v2, Alembic |
| **Database** | PostgreSQL 16+ / 19 |
| **AI Inference** | Local GPU Acceleration via Ollama (Llama 3.1, Qwen 2.5 Coder, Gemma 3, Qwen 3.5) |
| **Lead Harvester** | Google Places API (New) & Local Offline AI Crawler with Missing-Website Filter |

---

## 🤖 The AI Executive & Engineering Board

CODE WIBES operates through specialized autonomous agents assigned to dedicated company departments:

| Agent Name | Role / Title | Department | Primary Model |
|---|---|---|---|
| **Nexus** | Chief Executive Officer (CEO) | Executive Leadership | `llama3.1:latest` |
| **Forge** | CTO & Lead Full-Stack Engineer | Engineering | `qwen2.5-coder:3b` |
| **Atlas** | COO & Senior Technical Project Manager | Operations | `qwen3.5:4b` |
| **Hunter** | Head of B2B Lead Generation & Sales | Sales & Acquisition | `llama3.1:latest` |
| **Echo** | Head of Digital Marketing & Brand Strategy | Marketing | `gemma3:4b` |
| **Aura** | Principal UI/UX Architect | Design & Experience | `gemma3:4b` |
| **Sentinel**| Lead QA & Cybersecurity Auditor | Quality & Security | `qwen2.5-coder:3b` |
| **Ledger** | Head of Finance & Operations | Finance | `qwen3.5:2b` |

---

## 📁 Repository Structure

```
CODE-WIBES/
├── backend/
│   ├── alembic/                # Database schema migrations
│   │   └── versions/           # Migration revision scripts
│   ├── app/
│   │   ├── api/                # REST API routers (agents, leads, owner, projects, etc.)
│   │   ├── core/               # Pydantic configuration & environment settings
│   │   ├── database/           # Async SQLAlchemy engine & session factory
│   │   ├── models/             # ORM database entities (Lead, Agent, Project, Task, etc.)
│   │   ├── schemas/            # Request/Response Pydantic validation schemas
│   │   └── services/           # Agent runtime, Lead harvester, Company seeding
│   ├── tests/                  # Backend automated test suite
│   ├── alembic.ini             # Alembic configuration
│   ├── requirements.txt        # Python backend dependencies
│   └── update_agent_models.py  # Model mapping sync utility
├── frontend/
│   ├── public/                 # Static assets & icons
│   ├── src/
│   │   ├── api.ts              # Strongly typed Axios client & backend interfaces
│   │   ├── App.tsx             # Main Command Center UI with tabs & analytics
│   │   ├── App.css             # Cyberpunk/Dark-mode theme styling
│   │   └── main.tsx            # Vite root entry
│   ├── package.json            # Node.js dependencies & build scripts
│   ├── tsconfig.json           # TypeScript compilation config
│   └── vite.config.ts          # Vite build pipeline
├── execution/
│   ├── sandbox/                # Isolated sandbox for executing code
│   └── workspaces/             # Agent working directories
├── infrastructure/
│   └── database/               # Database initialization & deployment scripts
├── docs/                       # Architectural documentation and guides
├── .env.example                # Sample environment configuration
├── .gitignore                  # Global ignore rules
└── README.md                   # Project documentation
```

---

## ⚡ Core Capabilities

1. **Owner Command Center**:
   - Issue strategic directives directly to the CEO (Nexus) or any departmental head.
   - Natural language delegation decomposed into actionable tasks.

2. **Autonomous Sprints**:
   - High-speed autonomous execution loop: Objective ➔ CEO Strategic Roadmap ➔ Lead acquisition targets ➔ Engineering code generation.

3. **B2B Lead Acquisition & Harvester (Botsol Spec)**:
   - Scrapes and compiles structured B2B leads by industry/keyword and location.
   - **"No Website" Qualifier**: Identifies high-value agency targets lacking websites for web development outreach.
   - Instant export to **CSV (Excel compatible)** and **JSON**.

4. **Project & Task Management**:
   - Real-time tracking of projects, priorities, completion percentages, and agent task assignments.

5. **Local AI Model Routing**:
   - Zero API subscription fees. Connects directly to local Ollama runtime on your GPU.

---

## 🚀 Quick Start Guide

### Prerequisites

- **Python 3.12+**
- **Node.js 20+** (npm or pnpm)
- **PostgreSQL 16+** (Running locally or in Docker)
- **Ollama** installed with required models

---

### 1. Database Setup

Create a PostgreSQL database and user:

```sql
CREATE USER code_wibes WITH PASSWORD 'your_secure_password';
CREATE DATABASE code_wibes OWNER code_wibes;
```

---

### 2. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv .venv
# Windows:
.\.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp ../.env.example .env
# Edit .env with your PostgreSQL credentials

# Run database migrations
alembic upgrade head

# Start FastAPI development server
uvicorn app.main:app --reload --port 8000
```

FastAPI Interactive Docs will be live at: **http://127.0.0.1:8000/docs**

---

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start Vite development server
npm run dev
```

Dashboard will be live at: **http://localhost:5173**

---

### 4. Local AI Setup (Ollama)

Ensure Ollama is running and download the models:

```bash
ollama serve

# Pull models for your team
ollama pull llama3.1:latest
ollama pull qwen2.5-coder:3b
ollama pull qwen3.5:4b
ollama pull qwen3.5:2b
ollama pull gemma3:4b
```

---

## 🔑 Environment Configuration

Create a `.env` file in the `backend/` directory based on `.env.example`:

```env
APP_NAME="CODE WIBES"
APP_ENV="development"

# PostgreSQL Configuration
PGHOST="127.0.0.1"
PGPORT=5432
PGDATABASE="code_wibes"
PGUSER="code_wibes"
PGPASSWORD="your_password_here"

# Optional: Google Places API Key (If omitted, local agent crawler is used)
GOOGLE_MAPS_API_KEY=""
```

---

## 📡 API Reference Summary

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check endpoint |
| `GET` | `/health/database` | PostgreSQL connection health verification |
| `GET` | `/api/v1/departments` | List all company departments |
| `GET` | `/api/v1/agents` | List all autonomous agents and their model status |
| `GET` | `/api/v1/projects` | Fetch all ongoing and completed projects |
| `POST`| `/api/v1/projects` | Create a new project |
| `GET` | `/api/v1/tasks` | Fetch task backlog |
| `POST`| `/api/v1/tasks` | Create and assign a task |
| `GET` | `/api/v1/leads` | List acquired commercial leads |
| `POST`| `/api/v1/leads/google-maps-harvest` | Trigger Google Maps lead harvesting |
| `GET` | `/api/v1/leads/export/csv` | Download leads as CSV |
| `GET` | `/api/v1/leads/export/json` | Download leads as JSON |
| `POST`| `/api/v1/owner/command` | Issue owner directive to agent |
| `POST`| `/api/v1/owner/autonomous-sprint` | Run autonomous company sprint |
| `POST`| `/api/v1/owner/chat/{agent_id}` | Direct interactive chat with an agent |

---

## 🛡️ Security & Clean Code

- **Security First**: Secrets and environment variables are excluded via `.gitignore`. Parameterized SQL queries prevent SQL injection.
- **Async Architecture**: Non-blocking asynchronous I/O across database queries and local LLM requests.
- **Fail-Safe Fallbacks**: Lead harvester falls back to offline agent extraction when Google Maps API key is not supplied.

---

## 📜 License

Private & Proprietary — **CODE WIBES**. All rights reserved.
