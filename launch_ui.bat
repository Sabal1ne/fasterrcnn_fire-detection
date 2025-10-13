@echo off
REM Fire Detection Web Interface Launcher for Windows

echo ========================================
echo 🔥 Fire Detection System - Web Interface
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org/
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Check if Gradio is installed
python -c "import gradio" 2>nul
if errorlevel 1 (
    echo ⚠️  Warning: Gradio is not installed
    echo Installing required dependencies...
    pip install gradio>=3.50.0
    echo.
)

REM Check if PyTorch is installed
python -c "import torch" 2>nul
if errorlevel 1 (
    echo ⚠️  Warning: PyTorch is not installed
    echo Please install PyTorch from https://pytorch.org/
    echo Or run: pip install -r requirements.txt
    pause
    exit /b 1
)

echo ✅ All dependencies found
echo.
echo Starting web interface...
echo The interface will open at: http://localhost:7860
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Launch the interface
python launch_ui.py

pause
