@echo off
echo Backend başlatılıyor...
cd /d "%~dp0"
set PYTHONPATH=%CD%
set AI_MODEL_TYPE=mock
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
pause
