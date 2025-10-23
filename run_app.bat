@echo off
REM Sign Language Detection Application Launcher (Windows)
REM This script helps you run the application with proper setup

echo ==========================================
echo Sign Language Detection Application
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed!
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo [OK] Python found
python --version

REM Check if virtual environment exists
if not exist "venv\" (
    echo.
    echo No virtual environment found. Creating one...
    python -m venv venv
    echo [OK] Virtual environment created
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
python -c "import cv2" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Dependencies not installed. Installing...
    pip install -r requirements.txt
    echo [OK] Dependencies installed
) else (
    echo [OK] Dependencies already installed
)

REM Check for model file
echo.
echo Checking for model file...
set MODEL_FOUND=0
if exist "model.h5" (
    echo [OK] Model found: model.h5
    set MODEL_FOUND=1
)
if exist "model.keras" (
    echo [OK] Model found: model.keras
    set MODEL_FOUND=1
)
if exist "asl_model.h5" (
    echo [OK] Model found: asl_model.h5
    set MODEL_FOUND=1
)

if %MODEL_FOUND%==0 (
    echo [WARNING] No model file found!
    echo Please place your trained model (.h5 or .keras) in this directory
    echo Or update MODEL_PATH in config.py
    echo.
    set /p CONTINUE="Continue anyway? (y/n): "
    if /i not "%CONTINUE%"=="y" exit /b 1
)

REM Run the application
echo.
echo ==========================================
echo Starting application...
echo ==========================================
echo.

python sign_language_app.py

REM Deactivate virtual environment
call venv\Scripts\deactivate.bat

pause
