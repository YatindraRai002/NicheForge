@echo off
echo Starting NicheForge Stack...

start "NicheForge Backend" cmd /k "python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"
start "NicheForge Frontend" cmd /k "cd frontend && npm run dev"

echo Backend running on http://localhost:8000
echo Frontend running on http://localhost:3000
