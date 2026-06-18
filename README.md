# Agentic QA Platform

An intelligent QA automation platform using LangGraph agents for automated test case generation from software requirements and comprehensive testing capabilities.

## Overview

The Agentic QA Platform is built with:
- **LangGraph**: Multi-agent orchestration for complex QA workflows
- **LangSmith**: Observability and monitoring of agent interactions
- **SQLite**: Lightweight database for storing requirements and test cases
- **Python 3.14**: Latest Python version for modern features and performance

## Architecture

### Clean Architecture Layers

```
src/
├── agents/                    # LLM-powered agents
│   └── requirement_agent.py  # Parses requirements and generates test cases
├── workflows/                 # LangGraph workflows
│   ├── qa_workflow.py        # Main QA workflow orchestration
│   └── file_processor.py     # Requirement file processing
├── models/                    # Data models and schemas
│   └── schemas.py            # Pydantic schemas for validation
├── database/                  # Database layer
│   ├── config.py             # Database configuration
│   ├── models.py             # SQLAlchemy ORM models
│   └── services.py           # Database service layer
├── config/                    # Configuration
│   ├── settings.py           # Application settings
│   └── logging_config.py     # Logging configuration
└── main.py                    # Application entry point

tests/                         # Test suite
├── test_requirement_agent.py
├── test_database.py
└── test_workflow.py

requirements_folder/          # Markdown requirement files
data/                         # SQLite database
logs/                         # Application logs
```

## Features

### 1. Requirement Agent
- Reads markdown requirement files from `requirements_folder/`
- Parses requirements to extract key information
- Generates comprehensive structured test cases
- Uses LLM to understand context and create realistic test scenarios

### 2. Test Case Generation
- Automatic test case creation from requirements
- Structured test cases with:
  - Unique test IDs (TC001, TC002, etc.)
  - Clear titles and descriptions
  - Preconditions
  - Step-by-step test actions
  - Expected results
  - Priority levels (low, medium, high, critical)

### 3. Database Management
- **Requirements Table**: Stores parsed requirements
- **Test Cases Table**: Stores generated test cases
- **Test Executions Table**: Logs test execution results
- Relational structure for easy querying and analysis

### 4. Workflow Orchestration
LangGraph-based workflow with stages:
1. **Parse Requirement**: Extract metadata and structure
2. **Extract Scenarios**: Identify test scenarios and acceptance criteria
3. **Generate Test Cases**: Use LLM agent to create comprehensive test cases
4. **Validate Output**: Ensure quality and completeness
5. **Save to Database**: Persist results to SQLite

### 5. Observability
- **LangSmith Integration**: Monitor agent interactions and decisions
- **Comprehensive Logging**: File and console logging with rotation
- **Execution Tracking**: Track test case status and results

## Installation

### Prerequisites
- Python 3.14
- pip or conda
- OpenAI API key
- LangSmith API key (optional, for observability)

### Setup

1. Clone the repository:
```bash
cd Agentic-QA-Platform
```

2. Create a virtual environment:
```bash
python3.14 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
# Or: pip install -e .
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

5. Initialize database:
```bash
python -c "from src.database.config import init_db; init_db()"
```

## Usage

### Basic Usage

```python
from src.main import AgenticQAPlatform

# Initialize platform
platform = AgenticQAPlatform()

# Process all requirements
results = platform.process_all_requirements()

# List generated test cases
test_cases = platform.list_generated_test_cases()
```

### Process Single Requirement

```python
platform = AgenticQAPlatform()

requirement_text = """
# Login Feature
Users should be able to log in with email and password.
...
"""

result = platform.process_single_requirement("login.md", requirement_text)
```

### Add Custom Requirements

1. Create a markdown file in `requirements_folder/`:
```bash
nano requirements_folder/my_feature.md
```

2. Write your requirement:
```markdown
# Feature Name

## Overview
Feature description...

## Functional Requirements
- Requirement 1
- Requirement 2

## Acceptance Criteria
- Criteria 1
- Criteria 2
```

3. Run the platform to generate test cases

## Configuration

Edit `.env` file to configure:

| Variable | Description | Default |
|----------|-------------|---------|
| `ENV` | Environment (development/production) | development |
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `MODEL_NAME` | LLM model to use | gpt-4 |
| `TEMPERATURE` | LLM temperature (0-1) | 0.7 |
| `LANGSMITH_API_KEY` | LangSmith API key | Optional |
| `TARGET_WEBSITE_URL` | Target website for testing | https://demo.opencart.com/ |
| `LOG_LEVEL` | Logging level | INFO |
| `REQUIREMENTS_PATH` | Path to requirements folder | ./requirements_folder |
| `DATABASE_URL` | Database connection string | sqlite:///./data/qa_platform.db |

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_requirement_agent.py -v

# Run specific test
pytest tests/test_database.py::test_create_requirement -v
```

## Database Schema

### Requirements Table
```sql
CREATE TABLE requirements (
    id INTEGER PRIMARY KEY,
    filename VARCHAR(255) UNIQUE,
    title VARCHAR(255),
    content TEXT,
    created_at DATETIME,
    updated_at DATETIME
);
```

### Test Cases Table
```sql
CREATE TABLE test_cases (
    id INTEGER PRIMARY KEY,
    requirement_id INTEGER,
    test_id VARCHAR(50) UNIQUE,
    title VARCHAR(255),
    description TEXT,
    preconditions TEXT,  -- JSON
    steps TEXT,          -- JSON
    expected_result TEXT,
    status VARCHAR(20),  -- draft, ready, executed, passed, failed
    priority VARCHAR(20),  -- low, medium, high, critical
    created_at DATETIME,
    updated_at DATETIME
);
```

### Test Executions Table
```sql
CREATE TABLE test_executions (
    id INTEGER PRIMARY KEY,
    test_case_id INTEGER,
    executed_at DATETIME,
    status VARCHAR(20),  -- passed, failed, skipped
    duration_seconds INTEGER,
    error_message TEXT,
    logs TEXT
);
```

## Future Enhancements

The platform is designed for extensibility. Planned additions:

### 1. Playwright Agent
- Browser automation for test execution
- Web UI interaction and validation
- Screenshot and video capture
- Cross-browser testing support

### 2. Defect Triage Agent
- Automatic defect classification
- Root cause analysis
- Severity and priority assignment
- Duplicate detection

### 3. Jira Integration Agent
- Automatic defect logging
- Bi-directional synchronization
- Issue tracking and management
- Sprint planning integration

### 4. API Testing Agent
- REST API endpoint testing
- Request/response validation
- Performance testing
- Load testing capabilities

### 5. Visual Testing Agent
- UI element detection
- Visual regression testing
- Layout validation
- Accessibility checks

## Project Structure Details

### Agents Module (`src/agents/`)
- **RequirementAgent**: Main agent for requirement processing
  - Parses requirements using LLM
  - Generates structured test cases
  - Extracts scenarios and criteria

### Workflows Module (`src/workflows/`)
- **QAWorkflow**: LangGraph-based workflow orchestration
- **RequirementFileProcessor**: Handles file I/O operations

### Models Module (`src/models/`)
- **schemas.py**: Pydantic models for validation and type checking

### Database Module (`src/database/`)
- **config.py**: SQLAlchemy engine and session setup
- **models.py**: ORM model definitions
- **services.py**: Service layer for database operations

### Config Module (`src/config/`)
- **settings.py**: Application configuration management
- **logging_config.py**: Logging setup and utilities

## Logging

The platform uses Python's logging module with:
- **Console Handler**: Real-time log output
- **File Handler**: Persistent logs in `logs/app.log`
- **Rotation**: Automatic log file rotation (10MB max)
- **Configurable Level**: Set via `LOG_LEVEL` environment variable

Example log output:
```
2024-01-15 10:30:45 - agentic_qa_platform - INFO - QA Workflow initialized
2024-01-15 10:30:46 - agentic_qa_platform - INFO - Processing requirement: user_registration.md
2024-01-15 10:30:50 - agentic_qa_platform - INFO - Generated 8 test cases
```

## API Integration Example

```python
from src.main import AgenticQAPlatform
from src.config.settings import settings

# Initialize
platform = AgenticQAPlatform()

# Process requirement
result = platform.process_single_requirement(
    filename="login_feature.md",
    content="# Login Feature\nUsers can log in with email and password..."
)

# Access results
print(f"Status: {result['status']}")
print(f"Test cases generated: {result['test_cases_generated']}")
print(f"Test cases: {result['test_cases']}")
```

## Contributing

Contributions are welcome! Please:
1. Create a feature branch
2. Add tests for new functionality
3. Ensure all tests pass
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues, questions, or feature requests, please use the GitHub issue tracker.

## Acknowledgments

- LangChain and LangGraph teams
- OpenAI for the powerful language models
- The open-source community

## Roadmap

- [ ] Web UI dashboard for test case management
- [ ] REST API for integration with external tools
- [ ] Support for multiple LLM providers (Claude, Gemini, etc.)
- [ ] Advanced test scheduling and reporting
- [ ] Integration with CI/CD pipelines
- [ ] Mobile app testing capabilities
- [ ] Performance and load testing
- [ ] Accessibility testing support
