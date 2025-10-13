#!/bin/bash

# Fire Detection Web Interface Launcher
# Simple script to start the Gradio web interface

echo "🔥 Fire Detection System - Web Interface"
echo "=========================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.7+ from https://www.python.org/"
    exit 1
fi

# Check if Gradio is installed
if ! python3 -c "import gradio" 2>/dev/null; then
    echo "⚠️  Warning: Gradio is not installed"
    echo "Installing required dependencies..."
    pip install gradio>=3.50.0
    echo ""
fi

# Check if PyTorch is installed
if ! python3 -c "import torch" 2>/dev/null; then
    echo "⚠️  Warning: PyTorch is not installed"
    echo "Please install PyTorch from https://pytorch.org/"
    echo "Or run: pip install -r requirements.txt"
    exit 1
fi

echo "✅ All dependencies found"
echo ""
echo "Starting web interface..."
echo "The interface will open at: http://localhost:7860"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

# Launch the interface
python3 launch_ui.py
