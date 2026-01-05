@echo off
echo Iniciando Backend API (FastAPI)...
cd /d %~dp0\backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause

