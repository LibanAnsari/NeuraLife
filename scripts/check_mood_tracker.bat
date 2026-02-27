@echo off
echo ================================================
echo   MOOD TRACKER - QUICK DIAGNOSTIC
echo ================================================
echo.

echo Checking if backend is running...
curl -s http://localhost:8000/docs > nul 2>&1
if %ERRORLEVEL% == 0 (
    echo [OK] Backend is running on http://localhost:8000
) else (
    echo [ERROR] Backend is NOT running!
    echo.
    echo ACTION REQUIRED: Start the backend first
    echo Run: start_backend.bat
    echo.
    pause
    exit /b 1
)

echo.
echo Running Python diagnostic...
cd /d "%~dp0backend"
python check_mood_endpoint.py

echo.
echo ================================================
echo   DIAGNOSTIC COMPLETE
echo ================================================
echo.
echo If you saw errors above, check MOOD_TRACKER_FIX.md
echo for detailed troubleshooting steps.
echo.
pause
