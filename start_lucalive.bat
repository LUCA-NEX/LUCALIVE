@echo off
setlocal EnableExtensions

set "ROOT=%~dp0"
if "%ROOT:~-1%"=="\" set "ROOT=%ROOT:~0,-1%"

set "BACKEND_DIR=%ROOT%\backend"
set "FRONTEND_DIR=%ROOT%\frontend"
set "FRONTEND_URL=http://127.0.0.1:5173"

if not exist "%BACKEND_DIR%" (
  echo [ERROR] Backend folder not found: "%BACKEND_DIR%"
  exit /b 1
)

if not exist "%FRONTEND_DIR%" (
  echo [ERROR] Frontend folder not found: "%FRONTEND_DIR%"
  exit /b 1
)

echo Starting backend in a new terminal...
start "LUCALIVE Backend" cmd /k "cd /d \"%BACKEND_DIR%\" && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 2 /nobreak >nul

echo Starting frontend in a new terminal...
start "LUCALIVE Frontend" cmd /k "cd /d \"%FRONTEND_DIR%\" && npm run dev"

echo Waiting for frontend at %FRONTEND_URL% ...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$url = '%FRONTEND_URL%';" ^
  "$deadline = (Get-Date).AddMinutes(2);" ^
  "while ((Get-Date) -lt $deadline) {" ^
  "  try {" ^
  "    Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 2 | Out-Null;" ^
  "    Start-Process $url;" ^
  "    exit 0" ^
  "  } catch {" ^
  "    Start-Sleep -Seconds 2" ^
  "  }" ^
  "}" ^
  "exit 1"

if errorlevel 1 (
  echo Frontend did not become ready within 2 minutes.
  echo Open %FRONTEND_URL% manually after startup finishes.
  exit /b 1
)

echo LUCALIVE opened in your default browser.
exit /b 0
