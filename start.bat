@echo off
REM Batch file launcher for PowerShell startup script
REM This allows double-clicking to start the application

echo Starting RAG Chatbot...
powershell -ExecutionPolicy Bypass -File "%~dp0start.ps1"
pause
