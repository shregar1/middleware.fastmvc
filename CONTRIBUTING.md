# Contributing to FastMVC Middleware

Thank you for your interest in contributing to FastMVC Middleware! This document provides guidelines and instructions for contributing.

## Development Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/hyyre/fastmvc-middleware.git
   cd fastmvc-middleware
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**

   ```bash
   pip install -e ".[dev]"
   ```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=fastmvc_middleware --cov-report=html

# Run specific test file
pytest tests/test_security.py

# Run with verbose output
pytest -v
```

## Code Quality

### Linting

```bash
# Run ruff linter
ruff check .

# Auto-fix issues
ruff check --fix .
```

### Type Checking

```bash
mypy fastmvc_middleware
```

### Formatting

We follow PEP 8 with a line length of 100 characters.

## Pull Request Process

1. **Fork the repository** and create your branch from `main`.

2. **Make your changes** following the coding standards.

3. **Add tests** for any new functionality.

4. **Update documentation** if needed.

5. **Run the test suite** to ensure all tests pass.

6. **Submit a pull request** with a clear description of the changes.

## Coding Standards

- Use type hints for all function parameters and return values
- Write docstrings for all public functions and classes
- Follow the existing code style
- Keep middleware implementations simple and focused
- Prefer composition over inheritance

## Adding New Middleware

When adding a new middleware:

1. Create a new file in `fastmvc_middleware/`
2. Extend `FastMVCMiddleware` base class
3. Add comprehensive docstrings with examples
4. Export from `__init__.py`
5. Add tests in `tests/`
6. Update README.md with documentation

### Template for New Middleware

```python
"""
My New Middleware for FastMVC.

Brief description of what this middleware does.
"""

from typing import Callable, Awaitable, Set

from starlette.requests import Request
from starlette.responses import Response

from fastmvc_middleware.base import FastMVCMiddleware


class MyNewMiddleware(FastMVCMiddleware):
    """
    Middleware that does something useful.
    
    Features:
        - Feature 1
        - Feature 2
    
    Example:
        ```python
        from fastapi import FastAPI
        from fastmvc_middleware import MyNewMiddleware
        
        app = FastAPI()
        app.add_middleware(MyNewMiddleware, option="value")
        ```
    """
    
    def __init__(
        self,
        app,
        option: str = "default",
        exclude_paths: Set[str] | None = None,
        exclude_methods: Set[str] | None = None,
    ) -> None:
        super().__init__(app, exclude_paths=exclude_paths, exclude_methods=exclude_methods)
        self.option = option
    
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        # Skip if needed
        if self.should_skip(request):
            return await call_next(request)
        
        # Your middleware logic here
        response = await call_next(request)
        
        return response
```

## Reporting Bugs

When reporting bugs, please include:

- Python version
- FastAPI/Starlette version
- FastMVC Middleware version
- Minimal code to reproduce the issue
- Expected vs actual behavior
- Full error traceback if applicable

## Feature Requests

Feature requests are welcome! Please:

- Check existing issues first
- Describe the use case
- Explain why this would be useful
- Consider submitting a PR if possible

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

