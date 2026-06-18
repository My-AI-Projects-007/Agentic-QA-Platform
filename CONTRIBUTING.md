# Contributing to Agentic QA Platform

Thank you for your interest in contributing to the Agentic QA Platform!

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/Agentic-QA-Platform.git`
3. Create a virtual environment: `python3.14 -m venv venv`
4. Activate it: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Install dev dependencies: `pip install -e ".[dev]"`

## Development Workflow

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Format code: `python tasks.py format`
4. Run tests: `python tasks.py test`
5. Commit with clear messages: `git commit -m "Add feature: description"`
6. Push to your fork: `git push origin feature/your-feature`
7. Create a Pull Request

## Code Standards

- Follow PEP 8 style guide
- Use type hints in function signatures
- Write docstrings for all public functions
- Maintain or improve test coverage
- Use black for code formatting
- Use isort for import sorting

## Testing Requirements

- Write tests for new features
- Ensure all tests pass: `pytest`
- Maintain minimum 80% code coverage
- Use descriptive test names

## Commit Messages

- Use clear, descriptive messages
- Format: `[type]: description`
- Types: feat, fix, docs, style, refactor, test, chore
- Example: `feat: add Playwright automation agent`

## Pull Request Process

1. Update documentation as needed
2. Add tests for new functionality
3. Ensure CI/CD checks pass
4. Request review from maintainers
5. Address review comments

## Areas for Contribution

### High Priority
- Playwright agent implementation
- Defect triage agent
- Jira integration agent

### Medium Priority
- Web UI dashboard
- REST API endpoints
- Multi-LLM provider support

### Low Priority
- Performance optimizations
- Documentation improvements
- Example scripts

## Reporting Issues

Use GitHub Issues for:
- Bug reports
- Feature requests
- Documentation issues
- Questions and discussions

Include:
- Clear description of the issue
- Steps to reproduce (if applicable)
- Expected vs actual behavior
- Environment details (Python version, OS, etc.)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to open an issue or contact the maintainers.

Thank you for contributing! 🚀
