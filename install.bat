@echo off
:: Budget Tracker - Auto-Installer
:: ----------------------------------
echo.
echo [1/3] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Installing...
    start ms-windows-store://pdp/?productid=9NRWMJP3717K
    echo Please install Python from the Microsoft Store, then re-run this script.
    pause
    exit
)

echo [2/3] Installing required packages...
python -m pip install --upgrade pip --quiet
python -m pip install --prefer-binary matplotlib --quiet
if %errorlevel% neq 0 (
    echo Failed to install packages. Retrying with admin rights...
    powershell -Command "Start-Process cmd -ArgumentList '/c python -m pip install --prefer-binary matplotlib' -Verb RunAs"
)

echo [3/3] Launching Budget Tracker...
python main.py
pause