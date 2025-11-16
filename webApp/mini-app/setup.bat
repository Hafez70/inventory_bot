@echo off
REM Development Setup Script for Telegram Mini App

echo.
echo 🚀 Setting up Telegram Mini App Development Environment
echo ==================================================
echo.

REM Check if Node.js is installed
echo 📦 Checking Node.js installation...
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Node.js is not installed. Please install Node.js 18+ first.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('node -v') do set NODE_VERSION=%%i
echo ✅ Node.js %NODE_VERSION% is installed
echo.

REM Check if npm is installed
echo 📦 Checking npm installation...
where npm >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ npm is not installed. Please install npm first.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('npm -v') do set NPM_VERSION=%%i
echo ✅ npm %NPM_VERSION% is installed
echo.

REM Install dependencies
echo 📥 Installing dependencies...
call npm install

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully
echo.

REM Check if API is running
echo 🔌 Checking if API is running...
curl -s http://localhost:8001/health >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ API is running at http://localhost:8001
) else (
    echo ⚠️  API is not running at http://localhost:8001
    echo    Please start your FastAPI backend first
)
echo.

REM Success message
echo ==================================================
echo ✅ Setup complete!
echo.
echo To start development:
echo   npm start
echo.
echo To build for production:
echo   npm run build
echo.
echo For testing in Telegram:
echo   1. Install ngrok: https://ngrok.com/download
echo   2. Run: ngrok http 4200
echo   3. Configure bot menu button with ngrok URL
echo.
echo See QUICKSTART.md for detailed instructions
echo ==================================================
echo.
pause

