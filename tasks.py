"""
Makefile-style commands for common operations
"""
import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd, description=None):
    """Run a shell command"""
    if description:
        print(f"\n{'='*60}")
        print(f"{description}")
        print(f"{'='*60}\n")
    
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Command failed with exit code {e.returncode}")
        sys.exit(1)


def setup():
    """Initial setup"""
    print("Setting up project...")
    
    # Create directories
    Path("logs").mkdir(exist_ok=True)
    Path("data").mkdir(exist_ok=True)
    Path("requirements_folder").mkdir(exist_ok=True)
    
    # Copy env file
    if not Path(".env").exists() and Path(".env.example").exists():
        run_command("cp .env.example .env")
    
    print("Setup complete!")


def install():
    """Install dependencies"""
    run_command("pip install -r requirements.txt", "Installing dependencies...")


def test():
    """Run tests"""
    run_command("pytest -v --cov=src --cov-report=html", "Running tests...")


def run():
    """Run the application"""
    run_command("python -m src.main", "Running application...")


def lint():
    """Run linters"""
    run_command("black src/ tests/", "Formatting with Black...")
    run_command("isort src/ tests/", "Sorting imports with isort...")
    run_command("flake8 src/ tests/ --max-line-length=100", "Linting with flake8...")


def format_code():
    """Format code"""
    run_command("black src/ tests/", "Formatting code...")
    run_command("isort src/ tests/", "Sorting imports...")


def clean():
    """Clean generated files"""
    print("Cleaning up...")
    run_command("find . -type d -name __pycache__ -exec rm -rf {} +", "Removing cache...")
    run_command("find . -type f -name '*.pyc' -delete", "Removing .pyc files...")
    run_command("rm -rf .pytest_cache .mypy_cache htmlcov .coverage", "Removing test artifacts...")
    print("Clean complete!")


def help_text():
    """Show help"""
    print("""
    Available commands:
    
    python tasks.py setup      - Initial project setup
    python tasks.py install    - Install dependencies
    python tasks.py test       - Run tests with coverage
    python tasks.py run        - Run the application
    python tasks.py lint       - Run all linters
    python tasks.py format     - Format code
    python tasks.py clean      - Clean generated files
    python tasks.py examples   - Run example scripts
    python tasks.py help       - Show this help message
    """)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        help_text()
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "setup":
        setup()
    elif command == "install":
        install()
    elif command == "test":
        test()
    elif command == "run":
        run()
    elif command == "lint":
        lint()
    elif command == "format":
        format_code()
    elif command == "clean":
        clean()
    elif command == "examples":
        run_command("python examples.py", "Running examples...")
    elif command == "help":
        help_text()
    else:
        print(f"Unknown command: {command}")
        help_text()
        sys.exit(1)
