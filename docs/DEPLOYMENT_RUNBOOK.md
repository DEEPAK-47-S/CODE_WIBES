# CODE WIBES TECHNOLOGIES — Deployment & Operations Runbook

**Environment:** Windows 11 Workstation / Linux Cloud Server  
**Production Ports:** Backend `8000`, Frontend `5173`, Ollama `11434`, PostgreSQL `5432`

---

## 1. Local Development Startup

### A. Start Database & Ollama
1. Verify PostgreSQL service is running on port `5432`.
2. Ensure Ollama service is active:
   ```powershell
   ollama serve
   ```

### B. Start Backend API
```powershell
cd backend
.\.venv\Scripts\activate
# Run database migrations
alembic upgrade head
# Start FastAPI server
uvicorn app.main:app --reload --port 8000
```
Verify diagnostics: `http://127.0.0.1:8000/health/system`

### C. Start Frontend Dashboard
```powershell
cd frontend
npm run dev
```
Open Dashboard: `http://localhost:5173`

---

## 2. Automated Test Execution

Run the complete test suite across all 11 phases:
```powershell
cd backend
.\.venv\Scripts\python -m pytest tests/ -v
```
All 26 unit and integration tests must pass before committing or deploying.

---

## 3. Database Backups & Rollbacks

### Creating a Snapshot Backup
```powershell
pg_dump -U code_wibes -d code_wibes -F c -b -v -f "infrastructure/database/backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').dump"
```

### Rollback / Schema Reversion
If an emergency rollback is required:
```powershell
cd backend
# Rollback one migration
alembic downgrade -1
# Or rollback to a specific revision
alembic downgrade <revision_id>
```

---

## 4. Emergency Kill Switch Runbook

If an agent behaves abnormally, enters a loop, or an unapproved external action is detected:
1. **Via UI**: Click the red **Emergency Pause** button in the Command Center header.
2. **Via API**:
   ```bash
   curl -X POST http://127.0.0.1:8000/api/v1/settings/emergency-pause
   ```
3. **To Resume**:
   ```bash
   curl -X POST http://127.0.0.1:8000/api/v1/settings/resume
   ```
