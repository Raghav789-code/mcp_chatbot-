@echo off
echo ================================================
echo PEOPLE DIRECTORY CHATBOT WITH GEMINI AI
echo ================================================
echo.
echo Step 1: Setting up Gemini API key...
python setup_gemini.py
echo.
echo Step 2: Starting chatbot (browser will open automatically)...
python chatbot/app.py
pause