# Contributing to Flaco AI

Thank you for your interest in contributing to Flaco! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/yourusername/flaco.ai/issues)
2. If not, create a new issue with:
   - Clear, descriptive title
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, Ollama version)
   - Relevant logs or screenshots

### Suggesting Features

1. Check existing feature requests
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Potential implementation approach (optional)

### Pull Requests

1. Fork the repository
2. Create a feature branch from `main`
3. Make your changes
4. Add/update tests if applicable
5. Update documentation
6. Ensure all tests pass
7. Submit a pull request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/flaco.ai.git
cd flaco.ai

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks (if available)
pre-commit install
```

## Code Style

- Follow PEP 8 for Python code
- Use type hints where appropriate
- Write docstrings for public APIs
- Keep functions focused and small
- Add comments for complex logic

## Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=flaco --cov-report=html
```

## Commit Messages

Follow conventional commits:

```
feat: Add support for new Ollama models
fix: Resolve permission handling bug
docs: Update installation instructions
refactor: Simplify tool execution logic
test: Add tests for security validator
```

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
