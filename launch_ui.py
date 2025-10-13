#!/usr/bin/env python3
"""
Simple launcher script for the Fire Detection Web Interface
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_interface

if __name__ == "__main__":
    print("🔥 Starting Fire Detection Web Interface...")
    print("=" * 60)
    print("The interface will open in your default web browser.")
    print("If it doesn't open automatically, go to: http://localhost:7860")
    print("Press Ctrl+C to stop the server.")
    print("=" * 60)
    
    demo = create_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
        inbrowser=True  # Automatically open in browser
    )
