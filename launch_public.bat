@echo off
REM Script to launch the Fire Detection interface with public sharing enabled

echo ============================================
echo   Starting Fire Detection with Public Sharing
echo ============================================
echo.
echo WARNING: Public URL will be valid for 72 hours
echo A shareable link will be generated...
echo.

REM Enable public sharing
set GRADIO_SHARE=True

REM Optional: Enable authentication (uncomment and set credentials)
REM set GRADIO_AUTH=username:password

REM Launch the interface
python launch_ui.py
