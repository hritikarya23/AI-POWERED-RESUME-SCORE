@echo off
title AI-Powered Resume Scorer
echo ============================================================
echo      Starting AI-Powered Resume Scorer Web Server...
echo ============================================================
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    echo Opening browser at http://127.0.0.1:8000 ...
    start http://127.0.0.1:8000
    echo Server running at http://127.0.0.1:8000 (Press Ctrl+C to stop)
    .venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
) else (
    echo [ERROR] Virtual environment (.venv) not found.
    pause
)
pause
