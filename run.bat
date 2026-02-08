@echo off
echo Starting RAG Chatbot...
echo.

cd /d "%~dp0"

call .venv\Scripts\activate.bat

echo Python environment activated
echo.

python app.py

pause
