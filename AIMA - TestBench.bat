@echo off
title AIMA - TestBench
color E
echo [AIMA - TestBench] Starting up...

:: Check Python installation
echo [STEP 1/2] Installing Python...
IF NOT EXIST "%LocalAppData%\Programs\Python\Python312\python.exe" (
    echo Installing Python 3.12.3 64-bit...
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe -OutFile python-3.12.3-amd64.exe"
    python-3.12.3-amd64.exe /quiet InstallAllUsers=0 PrependPath=1
    del python-3.12.3-amd64.exe
) ELSE (
    echo Python already installed
)
python --version

:: Install Python dependencies
echo [STEP 2/2] Installing Python dependencies...
pip install -r ./utils/requirements.txt
start /b python main.py

echo [AIMA - TestBench] Done!

@pause