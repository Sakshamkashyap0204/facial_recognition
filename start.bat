@echo off
echo ============================================================
echo Criminal Record Detection System - Quick Start
echo ============================================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo.
echo Checking MongoDB...
mongod --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: MongoDB not found or not in PATH
    echo Please ensure MongoDB is installed and running
    echo.
)

echo.
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Running system test...
python test_system.py
if errorlevel 1 (
    echo.
    echo WARNING: Some tests failed
    echo System may not work correctly
    echo.
    pause
)

echo.
echo ============================================================
echo Starting Criminal Record Detection System
echo ============================================================
echo.
echo The system will:
echo 1. Import criminal dataset
echo 2. Seed criminal data
echo 3. Start Flask application
echo.
echo Open browser: http://127.0.0.1:5000
echo.
echo Press CTRL+C to stop the server
echo.
pause

python quickstart.py
