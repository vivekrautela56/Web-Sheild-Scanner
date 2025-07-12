@echo off
REM WebShield Scanner Startup Script for Windows

REM Check if virtual environment exists
IF NOT EXIST venv (
    echo Creating virtual environment...
    python -m venv venv
    
    echo Installing dependencies...
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
) ELSE (
    call venv\Scripts\activate.bat
)

REM Check if results directory exists
IF NOT EXIST results (
    echo Creating results directory...
    mkdir results
)

REM Start the application
echo Starting WebShield Scanner...
python app.py

pause