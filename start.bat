@echo off
REM NODO x402 Protocol - Quick Start Script (Windows)

echo ==========================================
echo   NODO x402 Protocol - Starting Server
echo ==========================================
echo.

REM Check if .env exists
if not exist .env (
    echo [WARNING] No .env file found!
    echo Creating from template...
    copy env.example.txt .env
    echo [OK] Created .env file
    echo [WARNING] Please edit .env and add your API keys!
    echo.
    echo Required variables:
    echo   - NODO_WALLET_ADDRESS
    echo   - OPENROUTER_API_KEY
    echo   - ANTHROPIC_API_KEY
    echo   - OPENAI_API_KEY
    echo.
    echo Then run: start.bat
    pause
    exit /b 1
)

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed
    pause
    exit /b 1
)

echo [OK] Python found
for /f "tokens=*" %%i in ('python --version') do echo %%i

REM Check if venv exists
if not exist venv (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
)

REM Activate venv
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo [INFO] Installing dependencies...
pip install -q -r requirements.txt

echo.
echo ==========================================
echo   Starting FastAPI Server
echo ==========================================
echo.
echo Server will be available at:
echo   * http://localhost:8000
echo   * API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop
echo.

REM Start server
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

