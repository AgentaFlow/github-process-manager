#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Startup script for Local AI RAG Chatbot
.DESCRIPTION
    This script sets up and launches the RAG chatbot application.
    It creates a virtual environment, installs dependencies, and starts the Flask server.
#>

Write-Host "🤖 Local AI RAG Chatbot - Startup Script" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Get the script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# Check if Python is installed
Write-Host "🔍 Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Found: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://www.python.org/downloads/" -ForegroundColor Red
    pause
    exit 1
}

# Check if virtual environment exists
if (-not (Test-Path ".venv")) {
    Write-Host ""
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to create virtual environment" -ForegroundColor Red
        pause
        exit 1
    }
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "🔌 Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to activate virtual environment" -ForegroundColor Red
    pause
    exit 1
}
Write-Host "✅ Virtual environment activated" -ForegroundColor Green

# Check if dependencies are installed
Write-Host ""
Write-Host "📚 Checking dependencies..." -ForegroundColor Yellow
$pipList = pip list 2>&1 | Out-String
if (-not ($pipList -match "Flask")) {
    Write-Host "📥 Installing dependencies from requirements.txt..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
        pause
        exit 1
    }
    Write-Host "✅ Dependencies installed successfully" -ForegroundColor Green
}
else {
    Write-Host "✅ Dependencies already installed" -ForegroundColor Green
}

# Check if .env file exists
Write-Host ""
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  .env file not found!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Creating .env file from template..." -ForegroundColor Yellow
    
    if (Test-Path ".env.template") {
        Copy-Item ".env.template" ".env"
        Write-Host "✅ .env file created from template" -ForegroundColor Green
        Write-Host ""
        Write-Host "⚠️  IMPORTANT: Please edit .env file and add your API keys:" -ForegroundColor Red
        Write-Host "   1. GEMINI_API_KEY (required)" -ForegroundColor Red
        Write-Host "   2. GITHUB_TOKEN (optional)" -ForegroundColor Red
        Write-Host "   3. GITHUB_REPO_URL (optional)" -ForegroundColor Red
        Write-Host ""
        Write-Host "Press any key to open .env file in notepad..." -ForegroundColor Yellow
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        notepad .env
        Write-Host ""
        Write-Host "After saving your API keys, press any key to continue..." -ForegroundColor Yellow
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    }
    else {
        Write-Host "❌ .env.template not found. Please create .env manually." -ForegroundColor Red
        pause
        exit 1
    }
}
else {
    Write-Host "✅ .env file found" -ForegroundColor Green
}

# Create necessary directories
Write-Host ""
Write-Host "📁 Creating necessary directories..." -ForegroundColor Yellow
if (-not (Test-Path "uploads")) {
    New-Item -ItemType Directory -Path "uploads" | Out-Null
}
if (-not (Test-Path "chroma_db")) {
    New-Item -ItemType Directory -Path "chroma_db" | Out-Null
}
Write-Host "✅ Directories ready" -ForegroundColor Green

# Start the application
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "🚀 Starting the chatbot application..." -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "The application will be available at:" -ForegroundColor Green
Write-Host "👉 http://localhost:5000" -ForegroundColor Green -BackgroundColor DarkBlue
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Run the Flask application
python app.py

# Cleanup message
Write-Host ""
Write-Host "👋 Chatbot stopped. Goodbye!" -ForegroundColor Cyan
