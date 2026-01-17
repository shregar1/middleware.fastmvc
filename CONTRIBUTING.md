# Contributing to FastMVC Middleware

Thank you for your interest in contributing to FastMVC Middleware! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Code Style](#code-style)
- [Pull Request Process](#pull-request-process)
- [Writing Middleware](#writing-middleware)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone. Please:

- Be respectful and considerate in discussions
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards other community members

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/fastmvc-middleware.git
   cd fastmvc-middleware
   ```
3. **Add the upstream remote**:
   ```bash
   git remote add upstream https://github.com/hyyre/fastmvc-middleware.git
   ```

## Development Setup

### Prerequisites

- Python 3.10 or higher
- pip or uv package manager
- Git

### Installation

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

   Or using Make:
   ```bash
   make install-dev
   ```

3. Verify the setup:
   ```bash
   make test
   make lint
   ```

### Using Make

We provide a Makefile for common development tasks:

| Command | Description |
|---------|-------------|
| `make install` | Install package in editable mode |
| `make install-dev` | Install with dev dependencies |
| `make test` | Run tests with coverage |
| `make lint` | Run linter (ruff) |
| `make type-check` | Run type checker (mypy) |
| `make format` | Format code |
| `make clean` | Clean build artifacts |
| `make all` | Run lint, type-check, and test |

## Making Changes

### Branching Strategy

1. Create a new branch from `main`:
   ```bash
   git checkout main
   git pull upstream main
   git checkout -b feature/your-feature-name
   ```

2. Branch naming conventions:
   - `feature/` - New features
   - `fix/` - Bug fixes
   - `docs/` - Documentation changes
   - `refactor/` - Code refactoring
   - `test/` - Test additions or improvements

### Commit Messages

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(security): add Content-Security-Policy report-only mode
fix(rate-limit): handle missing client IP correctly
docs(readme): add metrics middleware documentation
test(cache): add tests for conditional requests
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_security.py

# Run specific test
pytest tests/test_security.py::TestSecurityHeaders::test_hsts_header

# Run tests in parallel
pytest -n auto

# Run with verbose output
pytest -v
```

### Writing Tests

1. **Test Location**: Place tests in the `tests/` directory
2. **Test Naming**: Use descriptive names: `test_<what>_<expected_behavior>`
3. **Test Structure**: Use the Arrange-Act-Assert pattern

Example:
```python
import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from fastMiddleware import SecurityHeadersMiddleware

class TestSecurityHeaders:
    """Tests for SecurityHeadersMiddleware."""
    
    @pytest.fixture
    def app(self) -> FastAPI:
        """Create test application."""
        app = FastAPI()
        app.add_middleware(SecurityHeadersMiddleware, enable_hsts=True)
        
        @app.get("/")
        async def root():
            return {"ok": True}
        
        return app
    
    @pytest.fixture
    def client(self, app: FastAPI) -> TestClient:
        """Create test client."""
        return TestClient(app)
    
    def test_hsts_header_present(self, client: TestClient):
        """Test that HSTS header is present when enabled."""
        # Arrange is done in fixtures
        
        # Act
        response = client.get("/")
        
        # Assert
        assert response.status_code == 200
        assert "Strict-Transport-Security" in response.headers
```

### Test Coverage

- Aim for 80%+ code coverage
- Cover both success and error paths
- Test edge cases and boundary conditions
- Test middleware interaction with other middlewares

## Code Style

### Python Style

We use:
- [Ruff](https://github.com/astral-sh/ruff) for linting and formatting
- [mypy](https://mypy.readthedocs.io/) for type checking

Run before committing:
```bash
make lint
make type-check
make format
```

### Style Guidelines

1. **Type Hints**: Use type hints for all function parameters and return values
   ```python
   def process_request(
       self,
       request: Request,
       call_next: Callable[[Request], Awaitable[Response]],
   ) -> Response:
   ```

2. **Docstrings**: Use Google-style docstrings
   ```python
   def dispatch(self, request: Request, call_next) -> Response:
       """Process the request through the middleware.
       
       Args:
           request: The incoming HTTP request.
           call_next: The next middleware/route handler.
       
       Returns:
           The HTTP response with modifications.
       
       Raises:
           ValueError: If the request is malformed.
       """
   ```

3. **Class Structure**: Follow consistent ordering
   ```python
   class MyMiddleware(FastMVCMiddleware):
       # 1. Class docstring
       # 2. __init__
       # 3. Public methods
       # 4. Private methods (prefixed with _)
   ```

## Pull Request Process

### Before Submitting

1. Update documentation if needed
2. Add tests for new functionality
3. Ensure all tests pass
4. Run linter and type checker
5. Update CHANGELOG.md

### Submitting

1. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Open a Pull Request against `main`

3. Fill out the PR template:
   - Description of changes
   - Link to related issues
   - Checklist of completed items

4. Wait for review and address feedback

### PR Review

- PRs require at least one approval
- CI must pass (tests, linting, type checking)
- Maintain conversation in the PR for context

## Writing Middleware

### Middleware Structure

All middleware should extend `FastMVCMiddleware`:

```python
from dataclasses import dataclass
from typing import Callable, Awaitable, Set

from starlette.requests import Request
from starlette.responses import Response

from fastMiddleware.base import FastMVCMiddleware


@dataclass
class MyMiddlewareConfig:
    """Configuration for MyMiddleware.
    
    Attributes:
        option1: Description of option1.
        option2: Description of option2.
    """
    option1: str = "default"
    option2: int = 100


class MyMiddleware(FastMVCMiddleware):
    """Brief description of what this middleware does.
    
    Example:
        ```python
        app.add_middleware(MyMiddleware, option1="value")
        ```
    
    Attributes:
        config: The middleware configuration.
    """
    
    def __init__(
        self,
        app,
        config: MyMiddlewareConfig | None = None,
        option1: str | None = None,
        option2: int | None = None,
        exclude_paths: Set[str] | None = None,
        exclude_methods: Set[str] | None = None,
    ) -> None:
        """Initialize the middleware.
        
        Args:
            app: The ASGI application.
            config: Optional configuration object.
            option1: Optional override for option1.
            option2: Optional override for option2.
            exclude_paths: Paths to skip processing.
            exclude_methods: HTTP methods to skip.
        """
        super().__init__(app, exclude_paths=exclude_paths, exclude_methods=exclude_methods)
        self.config = config or MyMiddlewareConfig()
        
        # Apply overrides
        if option1 is not None:
            self.config.option1 = option1
        if option2 is not None:
            self.config.option2 = option2
    
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        """Process the request.
        
        Args:
            request: The incoming request.
            call_next: The next handler.
        
        Returns:
            The modified response.
        """
        # Skip if excluded
        if self.should_skip(request):
            return await call_next(request)
        
        # Pre-processing
        # ...
        
        # Call next handler
        response = await call_next(request)
        
        # Post-processing
        # ...
        
        return response
```

### Middleware Checklist

When creating a new middleware:

- [ ] Extend `FastMVCMiddleware`
- [ ] Create a dataclass config (if needed)
- [ ] Support both config object and individual parameters
- [ ] Implement `dispatch` method
- [ ] Use `should_skip()` for path/method exclusion
- [ ] Add comprehensive docstrings
- [ ] Export from `src/__init__.py`
- [ ] Add tests in `tests/`
- [ ] Document in README.md
- [ ] Update CHANGELOG.md

### Testing Middleware

```python
class TestMyMiddleware:
    """Tests for MyMiddleware."""
    
    @pytest.fixture
    def app(self) -> FastAPI:
        """Create test application."""
        app = FastAPI()
        app.add_middleware(MyMiddleware, option1="test")
        
        @app.get("/")
        async def root():
            return {"ok": True}
        
        return app
    
    @pytest.fixture
    def client(self, app: FastAPI) -> TestClient:
        return TestClient(app)
    
    def test_basic_functionality(self, client: TestClient):
        """Test that middleware works correctly."""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_with_config_object(self):
        """Test using config object."""
        config = MyMiddlewareConfig(option1="custom", option2=200)
        app = FastAPI()
        app.add_middleware(MyMiddleware, config=config)
        # ...
    
    def test_excluded_path_skipped(self, client: TestClient):
        """Test that excluded paths are skipped."""
        # ...
```

## Questions?

If you have questions about contributing:

1. Check existing issues and discussions
2. Open a new discussion for general questions
3. Open an issue for bugs or feature requests

Thank you for contributing! 🎉
