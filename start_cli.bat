@echo off
title Research Agent - CLI
echo ============================================
echo   Research Agent - CLI Mode
echo ============================================
echo.
cd /d "%~dp0"
venv\Scripts\python.exe app.py
pause
