# Contributing to HTML Cleaning Toolkit

Thank you for your interest in contributing! Here's how to help:

## Development Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/alemonterocr/html-cleaning-toolkit.git
   cd html-cleaning-toolkit
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

3. **Install in development mode**

   ```bash
   pip install -e .
   pip install pytest pytest-cov
   ```

4. **Run tests**
   ```bash
   python tests/validate.py
   ```

## Code Style

- Follow [PEP 8](https://pep8.org/)
- Use type hints where possible
- Keep functions small and focused (Single Responsibility)
- Write docstrings for public functions
- All functions must be testable in isolation

## Testing Requirements

- Add tests for new features in `tests/test_<feature>.py`
- Update `tests/validate.py` if adding new modules
- Run full validation suite before submitting PR
- Aim for high code coverage

## Making Changes

1. **Create a feature branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Keep commits atomic and well-described
   - Reference issues in commit messages

3. **Test thoroughly**

   ```bash
   python tests/validate.py
   python tests/test_comprehensive.py
   ```

4. **Submit a Pull Request**
   - Describe what problem your PR solves
   - Reference any related issues
   - Include test coverage for new functionality

## Reporting Issues

- Use GitHub Issues for bug reports
- Include:
  - Python version (`python --version`)
  - Example HTML that reproduces the issue
  - Expected vs actual behavior
  - Full error traceback if applicable

## Architecture Guidelines

See `.instructions.md` for:

- Module responsibilities
- Design patterns used
- Common issues and solutions
- Code quality standards

## Questions?

Open an issue or discussion on GitHub. We're happy to help!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
