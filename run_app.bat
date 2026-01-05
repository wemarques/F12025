@echo off
echo Verificando dependencias...
python check_dependencies.py
if errorlevel 1 (
    echo.
    echo ERRO: Falha ao verificar dependencias. Instale manualmente com:
    echo pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo Iniciando Backend API (FastAPI)...
start cmd /k "cd /d %~dp0\backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
timeout /t 3 /nobreak > nul
echo Iniciando Frontend (Streamlit)...
start cmd /k "cd /d %~dp0 && python -m streamlit run streamlit_app/app.py"
echo.
echo Aplicacao iniciada!
echo Backend API: http://localhost:8000
echo Frontend Streamlit: http://localhost:8501
pause

