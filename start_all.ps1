# PowerShell script to start both frontend and backend
Write-Host "🚀 Starting UniqueAI Frontend and Backend..." -ForegroundColor Green

# Start Backend
Write-Host "📡 Starting Backend..." -ForegroundColor Yellow
$backendJob = Start-Job -ScriptBlock {
    Set-Location "C:\Users\NUR\Desktop\UniqeAi-feature-backend-correction (2)\UniqeAi-feature-backend-correction\backend"
    $env:PYTHONPATH = "."
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
}

# Wait a bit for backend to initialize
Start-Sleep -Seconds 3

# Start Frontend  
Write-Host "🎨 Starting Frontend..." -ForegroundColor Cyan
$frontendJob = Start-Job -ScriptBlock {
    Set-Location "C:\Users\NUR\Desktop\UniqeAi-feature-backend-correction (2)\UniqeAi-feature-backend-correction\frontend"
    npm run dev
}

Write-Host "✅ Both services are starting..." -ForegroundColor Green
Write-Host "🌐 Frontend will be available at: http://localhost:5173" -ForegroundColor Magenta
Write-Host "🔗 Backend API will be available at: http://localhost:8000" -ForegroundColor Magenta
Write-Host "📚 API Documentation: http://localhost:8000/docs" -ForegroundColor Magenta
Write-Host "" 
Write-Host "Press Ctrl+C to stop both services"

# Wait for user input to stop
try {
    while ($true) {
        Start-Sleep -Seconds 1
    }
} catch {
    Write-Host "🛑 Stopping services..." -ForegroundColor Red
    Stop-Job $backendJob, $frontendJob
    Remove-Job $backendJob, $frontendJob
}
