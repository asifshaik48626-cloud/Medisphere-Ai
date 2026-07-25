# MediSphere AI - Backend Monolith API

This directory contains the FastAPI-based backend monolith services.

## 🛠 Prerequisites

- Python 3.11+
- SQLite (Local development default) or PostgreSQL (Production)
- Virtual Environment tool (`venv`)

## 🚀 Getting Started

1. **Configure Environment Variables**:
   Copy `.env.example` from the root directory to `.env` and fill in the parameters:
   ```bash
   cp ../.env.example ../.env
   ```

2. **Set Up Python Virtual Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Initialize and Seed Database**:
   Seeding populates default exercise options, remedies, and test accounts (`patient@medisphere.com` / `doctor@medisphere.com` with password `password123`):
   ```bash
   PYTHONPATH=. .venv/bin/python -m app.seed
   ```

4. **Run DB Migrations (Alembic)**:
   ```bash
   PYTHONPATH=. .venv/bin/alembic upgrade head
   ```

5. **Start Dev Server**:
   ```bash
   .venv/bin/uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```
   Open `http://localhost:8000/docs` to view Swagger API interactive documentation.

## 🧪 Running Verification Tests

Run our diagnostic suite checking database setups, model constraints, and Safety Engine triage gates:
```bash
PYTHONPATH=. .venv/bin/python ../scratch/test_db_and_safety.py
```
