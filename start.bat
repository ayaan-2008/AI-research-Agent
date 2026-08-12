@echo off
title Research Agent
echo ============================================
echo   Research Agent - Starting...
echo ============================================
echo.
cd /d "%~dp0"
venv\Scripts\streamlit.exe run streamlit_app.py
pause
