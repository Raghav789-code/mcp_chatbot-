@echo off
echo Starting People Directory Chatbot...
echo =====================================
echo.
echo [INFO] Installing dependencies...
pip install -r chatbot_requirements.txt
echo.
echo [INFO] Starting chatbot server...
echo [INFO] Open http://localhost:8000 in your browser
echo [INFO] Press Ctrl+C to stop
echo.
python chatbot/app.py
pause