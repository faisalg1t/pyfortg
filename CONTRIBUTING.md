# Contributing to PyForTG

Thank you for your interest in contributing to PyForTG! This document provides guidelines and instructions for contributing.

## Getting Started

### Prerequisites
- Python 3.9+
- pip and virtualenv
- Git

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/pyfortg/pyfortg.git
cd pyfortg

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

## Development Workflow

### Code Style
- Follow PEP 8 standards
- Use type hints for all functions
- Maximum line length: 100 characters
- Use descriptive variable and function names

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pyfortg tests/

# Run specific test file
pytest tests/test_filters.py
```

### Before Submitting a Pull Request

1. **Run linting:**
   ```bash
   black pyfortg/
   isort pyfortg/
   flake8 pyfortg/
   ```

2. **Check types:**
   ```bash
   mypy pyfortg/
   ```

3. **Run tests:**
   ```bash
   pytest
   ```

4. **Update documentation** if needed

## Pull Request Process

1. Create a new branch: `git checkout -b feature/your-feature-name`
2. Make your changes and commit with clear messages
3. Push to your fork: `git push origin feature/your-feature-name`
4. Open a Pull Request with:
   - Clear description of changes
   - Reference to related issues
   - Test coverage for new features
   - Updated documentation

## Code Structure

```
pyfortg/
├── client/          # Core Telegram client
├── handlers/        # Message, callback, command handlers
├── middleware/      # Middleware system
├── storage/         # Storage backends (Redis, PostgreSQL)
├── keyboards.py     # Keyboard builders
├── filters.py       # Filter system
├── types.py         # Type definitions
├── exceptions.py    # Custom exceptions
└── utils/           # Utility functions
```

## Reporting Issues

Please include:
- Python version
- PyForTG version
- Steps to reproduce
- Expected vs actual behavior
- Relevant code snippets
- Error traceback

## Questions?

Feel free to open an issue for questions or discussions.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
