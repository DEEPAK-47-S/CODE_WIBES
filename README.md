# CODE WIBES

**AI-powered Software Company Operating System**

A centralized platform for managing an AI-operated software company with agent orchestration, project management, and department coordination.

## Architecture

| Component | Technology |
|-----------|-----------|
| Frontend | React + Vite + TypeScript |
| Backend | Python + FastAPI |
| Database | PostgreSQL 19 |
| AI Orchestration | LangGraph (planned) |

## Project Structure

```
CODE-WIBES-REPO/
├── backend/           # Python FastAPI backend
│   ├── app/
│   │   ├── api/       # API route handlers
│   │   ├── core/      # Configuration, security
│   │   ├── database/  # SQLAlchemy models, session
│   │   ├── models/    # ORM models
│   │   ├── schemas/   # Pydantic schemas
│   │   ├── services/  # Business logic
│   │   ├── agents/    # AI agent definitions
│   │   └── orchestration/  # Agent orchestration
│   ├── alembic/       # Database migrations
│   ├── tests/         # Backend tests
│   └── .env           # Environment variables (not committed)
├── frontend/          # React + Vite frontend
├── execution/         # Sandboxed agent workspaces
├── infrastructure/    # Database and deployment configs
└── docs/              # Documentation
```

## Quick Start

### Prerequisites

- Python 3.12+
- Node.js 24+
- PostgreSQL 19

### Backend

```bash
cd backend
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### API Docs

Once the backend is running: http://127.0.0.1:8000/docs

## Environment Variables

Copy `.env.example` to `backend/.env` and fill in your PostgreSQL password.

## License

Private — All rights reserved.
