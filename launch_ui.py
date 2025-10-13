#!/usr/bin/env python3
"""
Simple launcher script for the Fire Detection Web Interface
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_interface, GRADIO_SHARE, GRADIO_SERVER_NAME, GRADIO_SERVER_PORT, GRADIO_AUTH

if __name__ == "__main__":
    print("🔥 Starting Fire Detection Web Interface...")
    print("=" * 60)
    
    # Parse authentication if provided
    auth = None
    if GRADIO_AUTH:
        auth_parts = GRADIO_AUTH.split(':')
        if len(auth_parts) == 2:
            auth = (auth_parts[0], auth_parts[1])
            print("🔒 Authentication enabled")
    
    if GRADIO_SHARE:
        print("🌐 Public sharing enabled - generating public URL...")
        print("⚠️  Public URL will be valid for 72 hours")
    else:
        print("📍 Local mode - interface will be accessible only on this machine")
        print(f"If it doesn't open automatically, go to: http://localhost:{GRADIO_SERVER_PORT}")
    
    print("Press Ctrl+C to stop the server.")
    print("=" * 60)
    
    demo = create_interface()
    demo.launch(
        server_name=GRADIO_SERVER_NAME,
        server_port=GRADIO_SERVER_PORT,
        share=GRADIO_SHARE,
        show_error=True,
        inbrowser=True,  # Automatically open in browser
        auth=auth
    )
