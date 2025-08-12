@echo off
echo Backend başlatılıyor...
cd /d "%~dp0"
python -c "import uvicorn; from test_simple import app; print('Backend başladı: http://localhost:8001'); uvicorn.run(app, host='127.0.0.1', port=8001)"
pause
