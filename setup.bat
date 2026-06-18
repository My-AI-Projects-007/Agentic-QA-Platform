@echo off
REM Setup script for Agentic QA Platform (Windows)

setlocal enabledelayedexpansion

echo.
echo ========================================
echo Agentic QA Platform - Setup Script
echo ========================================
echo.

REM Check Python
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo √ Python %PYTHON_VERSION% installed

REM Create virtual environment
echo.
echo Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo √ Virtual environment created
) else (
    echo √ Virtual environment already exists
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo √ Virtual environment activated

REM Install dependencies
echo.
echo Installing dependencies...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    exit /b 1
)
echo √ Dependencies installed

REM Create directories
echo.
echo Creating directories...
if not exist "data" mkdir data
if not exist "logs" mkdir logs
if not exist "reports" mkdir reports
echo √ Directories created

REM Setup environment file
echo.
echo Setting up environment configuration...
if not exist ".env" (
    copy .env.example .env
    echo √ Created .env file (please edit with your API keys)
) else (
    echo √ .env file already exists
)

REM Initialize database
echo.
echo Initializing database...
python -c "from src.database.config import init_db; init_db()"
if errorlevel 1 (
    echo ERROR: Failed to initialize database
    exit /b 1
)
echo √ Database initialized

echo.
echo ========================================
echo √ Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file with your API keys:
echo    - OPENAI_API_KEY
echo    - LANGSMITH_API_KEY (optional)
echo.
echo 2. Add requirement files to requirements_folder\
echo.
echo 3. Run the platform:
echo    python tasks.py run
echo.
echo 4. View documentation:
echo    - README.md for full documentation
echo    - QUICKSTART.md for quick start
echo    - examples.py for code examples
echo.

pause
