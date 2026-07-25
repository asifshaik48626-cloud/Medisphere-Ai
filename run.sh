#!/bin/bash

# MediSphere AI - Local Startup Helper Script

echo "===================================================="
echo "🏥 Welcome to MediSphere AI Local Runner"
echo "===================================================="
echo "Please select an option:"
echo "1) Seed Local Database (SQLite)"
echo "2) Start FastAPI Monolith Backend"
echo "3) Launch React Frontend Dev Server"
echo "4) Spin Up Container Stack (Docker Compose)"
echo "5) Exit"
echo "===================================================="
read -p "Select option [1-5]: " opt

case $opt in
  1)
    echo "🌱 Seeding database catalogs and credentials..."
    cd backend
    PYTHONPATH=. .venv/bin/python -m app.seed
    ;;
  2)
    echo "🚀 Starting FastAPI Backend Monolith..."
    cd backend
    source .venv/bin/activate
    uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
    ;;
  3)
    echo "⚡ Launching React Frontend Server..."
    cd frontend
    npm run dev
    ;;
  4)
    echo "🐳 Starting all services with Docker Compose..."
    docker-compose up --build
    ;;
  5)
    echo "Goodbye!"
    exit 0
    ;;
  *)
    echo "Invalid option."
    exit 1
    ;;
esac
