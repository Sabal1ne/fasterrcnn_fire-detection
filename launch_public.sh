#!/bin/bash

# Script to launch the Fire Detection interface with public sharing enabled

echo "🔥 Starting Fire Detection with Public Sharing"
echo "=============================================="
echo ""
echo "⚠️  Public URL will be valid for 72 hours"
echo "🌐 A shareable link will be generated..."
echo ""

# Enable public sharing
export GRADIO_SHARE=True

# Optional: Enable authentication (uncomment and set credentials)
# export GRADIO_AUTH=username:password

# Launch the interface
python launch_ui.py
