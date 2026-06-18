"""
Quick start guide
"""

# QUICK START GUIDE

## 1. Installation

```bash
# Clone or navigate to project
cd Agentic-QA-Platform

# Create virtual environment
python3.14 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup
python tasks.py setup
```

## 2. Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your API keys:
# - OPENAI_API_KEY=your_key_here
# - LANGSMITH_API_KEY=your_key_here (optional)
```

## 3. Add Requirements

Create markdown files in `requirements_folder/`:

```markdown
# Feature Name

## Overview
Brief description of the feature...

## Functional Requirements
- Requirement 1
- Requirement 2

## Acceptance Criteria
- Criteria 1
- Criteria 2
```

## 4. Run the Platform

```bash
# Process all requirements
python tasks.py run

# Or run examples
python tasks.py examples

# Or in Python code:
from src.main import AgenticQAPlatform

platform = AgenticQAPlatform()
results = platform.process_all_requirements()
test_cases = platform.list_generated_test_cases()
```

## 5. View Results

- Generated test cases are stored in SQLite database: `data/qa_platform.db`
- Logs are in: `logs/app.log`
- See test cases by querying the database or using the platform API

## 6. Run Tests

```bash
# Run all tests
python tasks.py test

# Run specific test
pytest tests/test_database.py -v

# With coverage
pytest --cov=src
```

## 7. Development

```bash
# Format code
python tasks.py format

# Run linters
python tasks.py lint

# Clean artifacts
python tasks.py clean
```

## Next Steps

1. Add your requirements to `requirements_folder/`
2. Set up environment variables in `.env`
3. Run the platform
4. View generated test cases in the database
5. (Future) Connect Playwright agent for test execution
6. (Future) Integrate with Jira for defect management

## Troubleshooting

### Import errors
- Ensure you're in the virtual environment
- Install dependencies: `pip install -r requirements.txt`

### API key errors
- Set OPENAI_API_KEY in `.env`
- Ensure key has valid access to GPT-4

### Database errors
- Delete `data/qa_platform.db` to reset
- Run `python -c "from src.database.config import init_db; init_db()"`

### File not found errors
- Ensure you're running from project root directory
- Check file paths in `.env`

## Resources

- [Full README](README.md)
- [Roadmap](ROADMAP.md)
- [Contributing](CONTRIBUTING.md)
- [Examples](examples.py)

## Support

For issues or questions, check:
1. README.md for detailed documentation
2. examples.py for usage examples
3. tests/ for test examples
4. GitHub Issues for known issues
