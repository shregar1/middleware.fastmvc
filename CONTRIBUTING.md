# Contributing to FastMVC Middleware

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and constructive in all interactions. We're building this together.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- Make (optional but recommended)

### Development Setup

1. **Fork and clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/fastmvc-middleware.git
cd fastmvc-middleware

```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

```

3. **Install development dependencies**

```bash
make install-dev

# Or manually:
pip install -e ".[dev]"
pre-commit install

```

4. **Verify setup**

```bash
make test-fast
make lint

```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name

# or
git checkout -b fix/issue-description

```

### 2. Make Changes

- Write code following our style guide
- Add tests for new functionality
- Update documentation as needed

### 3. Run Quality Checks

```bash

# Run all checks
make check-all

# Or individually:
make lint        # Linting
make format      # Format code
make type-check  # Type checking
make security    # Security scan
make test        # Tests with coverage

```

### 4. Commit Changes

We use conventional commits:

```bash
git commit -m "feat: add new middleware for XYZ"
git commit -m "fix: resolve issue with rate limiting"
git commit -m "docs: update README with new examples"
git commit -m "test: add tests for compression middleware"

```

Prefixes:

- `feat:` - New feature

- `fix:` - Bug fix

- `docs:` - Documentation only

- `test:` - Adding tests

- `refactor:` - Code refactoring

- `perf:` - Performance improvement

- `chore:` - Maintenance tasks

### 5. Submit Pull Request

> ⚠️ **Note**: Direct pushes to `main` are disabled. All changes must go through a pull request.

1. Push your branch
2. Open a PR against `main`
3. Fill out the PR template
4. Wait for CI checks to pass
5. Get approval from a code owner
6. Merge (squash recommended)

See [Branch Protection Setup](.github/BRANCH_PROTECTION.md) for details on branch protection rules.

## Creating a New Middleware

### 1. Create the middleware file

```python

# fastmiddleware/your_middleware.py
"""
Your Middleware - Brief description.

This middleware does XYZ for FastAPI/Starlette applications.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Callable, Awaitable, Set

from starlette.requests import Request
from starlette.responses import Response

from .base import FastMVCMiddleware

if TYPE_CHECKING:
    from starlette.types import ASGIApp

@dataclass
class YourMiddlewareConfig:
    """Configuration for YourMiddleware.

    Attributes:
        option1: Description of option1.
        option2: Description of option2.
        exclude_paths: Paths to exclude from processing.
    """
    option1: str = "default"
    option2: int = 100
    exclude_paths: Set[str] = field(default_factory=set)

class YourMiddleware(FastMVCMiddleware):
    """Middleware that does XYZ.

    This middleware provides ABC functionality for FastAPI/Starlette apps.

    Example:
        ```python
        from fastmiddleware import YourMiddleware, YourMiddlewareConfig

        app.add_middleware(
            YourMiddleware,
            option1="value",
            option2=50,
        )
        ```

    Args:
        app: The ASGI application.
        config: Configuration object (optional).
        option1: Direct option (if not using config).
        option2: Direct option (if not using config).
        exclude_paths: Paths to exclude.
    """

    def __init__(
        self,
        app: ASGIApp,
        config: YourMiddlewareConfig | None = None,
        option1: str = "default",
        option2: int = 100,
        exclude_paths: Set[str] | None = None,
    ) -> None:
        super().__init__(app, exclude_paths=exclude_paths)

        if config:
            self.option1 = config.option1
            self.option2 = config.option2
        else:
            self.option1 = option1
            self.option2 = option2

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        """Process the request.

        Args:
            request: The incoming request.
            call_next: The next middleware/handler.

        Returns:
            The response from the application.
        """
        if self.should_skip(request):
            return await call_next(request)

        # Pre-processing
        # ...

        response = await call_next(request)

        # Post-processing
        # ...

        return response

```

### 2. Export in `__init__.py`

```python
from .your_middleware import YourMiddleware, YourMiddlewareConfig

```

### 3. Add tests

```python

# tests/test_your_middleware.py
import pytest
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.testclient import TestClient

from fastmiddleware import YourMiddleware, YourMiddlewareConfig

class TestYourMiddleware:
    def test_basic_functionality(self):
        app = Starlette()
        app.add_middleware(YourMiddleware)

        @app.route("/")
        async def homepage(request):
            return PlainTextResponse("OK")

        client = TestClient(app)
        response = client.get("/")

        assert response.status_code == 200
        # Add your assertions

    def test_with_config(self):
        config = YourMiddlewareConfig(option1="custom")
        # Test with config...

    def test_exclude_paths(self):
        # Test path exclusion...

```

### 4. Add documentation

Create `docs/middlewares/your-middleware.md`:

```markdown

# YourMiddleware

Brief description of what it does.

## Prerequisites

✅ No additional dependencies required.

## Installation

\`\`\`bash
pip install fastmvc-middleware
\`\`\`

## Usage

\`\`\`python
from fastmiddleware import YourMiddleware

app.add_middleware(YourMiddleware, option1="value")
\`\`\`

## Configuration

|Parameter|Type|Default|Description|
| ----------- | ------ | --------- | ------------- |
|`option1`|`str`|`"default"`|Description|
|`option2`|`int`|`100`|Description|

## Related Middlewares

- [RelatedMiddleware](related.md)

```

## Code Style

### Python

- Follow PEP 8
- Use type hints everywhere
- Maximum line length: 100 characters
- Use double quotes for strings
- Use `from __future__ import annotations` for modern typing

### Docstrings

Use Google-style docstrings:

```python
def function(arg1: str, arg2: int = 0) -> bool:
    """Brief description.

    Longer description if needed.

    Args:
        arg1: Description of arg1.
        arg2: Description of arg2.

    Returns:
        Description of return value.

    Raises:
        ValueError: When something is wrong.
    """

```

### Testing

- Minimum 80% coverage for new code
- Test both success and failure cases
- Test edge cases
- Use fixtures for common setup
- Use parametrize for similar tests

## Questions?

- Open a [Discussion](https://github.com/shregar1/fastmvc-middleware/discussions)
- Check existing [Issues](https://github.com/shregar1/fastmvc-middleware/issues)

Thank you for contributing! 🎉
