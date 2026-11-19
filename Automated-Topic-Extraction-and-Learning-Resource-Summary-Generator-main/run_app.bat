@echo off
title AI Lecture Assistant
cd /d "%~dp0"
echo ========================================================
echo   Starting AI Lecture Assistant & Study Hub...
echo ========================================================
echo.
"%~dp0..\.venv\Scripts\python.exe" "%~dp0app.py"
pause
