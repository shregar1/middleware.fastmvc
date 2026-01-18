.PHONY: all install install-dev test test-fast test-cov lint format type-check security clean build publish publish-test check pre-commit help

# Default target
all: lint type-check test

# Installation
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	pre-commit install

# Testing
test:
	pytest tests/ -v --cov=fastMiddleware --cov-report=term-missing

test-fast:
	pytest tests/ -v -x --tb=short -q

test-cov:
	pytest tests/ --cov=fastMiddleware --cov-report=html --cov-report=xml
	@echo "Coverage report: htmlcov/index.html"

test-parallel:
	pytest tests/ -v -n auto --cov=fastMiddleware

# Code Quality
lint:
	ruff check fastMiddleware tests

lint-fix:
	ruff check fastMiddleware tests --fix

format:
	ruff format fastMiddleware tests

format-check:
	ruff format --check fastMiddleware tests

type-check:
	mypy fastMiddleware --ignore-missing-imports

security:
	bandit -c pyproject.toml -r fastMiddleware

# All checks (for CI)
check-all: format-check lint type-check security test

# Pre-commit
pre-commit:
	pre-commit run --all-files

pre-commit-install:
	pre-commit install
	pre-commit install --hook-type commit-msg

# Build and Publish
clean:
	rm -rf build dist *.egg-info .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage coverage.xml
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

check:
	twine check dist/*

publish-test: build check
	twine upload --repository testpypi dist/*

publish: build check
	twine upload dist/*

# Development
dev:
	uvicorn examples.app:app --reload --port 8000

# Documentation
docs-serve:
	@echo "Documentation available at: https://github.com/hyyre/fastmvc-middleware#readme"

# Version bump helpers
version-patch:
	@echo "Update version in pyproject.toml and fastMiddleware/__init__.py"
	@grep -E "^version = " pyproject.toml
	@grep -E "^__version__ = " fastMiddleware/__init__.py

version-check:
	@echo "Current versions:"
	@grep -E "^version = " pyproject.toml
	@grep -E "^__version__ = " fastMiddleware/__init__.py

# Help
help:
	@echo "FastMVC Middleware - Development Commands"
	@echo ""
	@echo "Installation:"
	@echo "  make install          Install package"
	@echo "  make install-dev      Install with dev dependencies + pre-commit"
	@echo ""
	@echo "Testing:"
	@echo "  make test             Run tests with coverage"
	@echo "  make test-fast        Run tests quickly (stop on first failure)"
	@echo "  make test-cov         Run tests with HTML coverage report"
	@echo "  make test-parallel    Run tests in parallel"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint             Run linter (ruff)"
	@echo "  make lint-fix         Run linter with auto-fix"
	@echo "  make format           Format code (ruff format)"
	@echo "  make format-check     Check code formatting"
	@echo "  make type-check       Run type checker (mypy)"
	@echo "  make security         Run security scan (bandit)"
	@echo "  make check-all        Run all checks (for CI)"
	@echo "  make pre-commit       Run all pre-commit hooks"
	@echo ""
	@echo "Build & Publish:"
	@echo "  make clean            Clean build artifacts"
	@echo "  make build            Build package"
	@echo "  make check            Check package with twine"
	@echo "  make publish-test     Publish to TestPyPI"
	@echo "  make publish          Publish to PyPI"
	@echo ""
	@echo "Other:"
	@echo "  make version-check    Check current version"
	@echo "  make help             Show this help"
