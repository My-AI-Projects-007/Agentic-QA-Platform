#!/bin/bash
# Setup script for Agentic QA Platform

set -e

echo "========================================"
echo "Agentic QA Platform - Setup Script"
echo "========================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version installed"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Create directories
echo ""
echo "Creating directories..."
mkdir -p data logs reports
echo "✓ Directories created"

# Setup environment file
echo ""
echo "Setting up environment configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ Created .env file (please edit with your API keys)"
else
    echo "✓ .env file already exists"
fi

# Initialize database
echo ""
echo "Initializing database..."
python -c "from src.database.config import init_db; init_db()"
echo "✓ Database initialized"

echo ""
echo "========================================"
echo "✓ Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys:"
echo "   - OPENAI_API_KEY"
echo "   - LANGSMITH_API_KEY (optional)"
echo ""
echo "2. Add requirement files to requirements_folder/"
echo ""
echo "3. Run the platform:"
echo "   python tasks.py run"
echo ""
echo "4. View documentation:"
echo "   - README.md for full documentation"
echo "   - QUICKSTART.md for quick start"
echo "   - examples.py for code examples"
echo ""
