# PromptCraft CLI Makefile

.PHONY: help install install-dev test lint format clean build publish

PYTHON := python3
PIP := pip3

help:
	@echo "PromptCraft CLI - Available Commands:"
	@echo ""
	@echo "  make install      - Install the package"
	@echo "  make install-dev  - Install with development dependencies"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linters"
	@echo "  make format       - Format code with black"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make build        - Build distribution packages"
	@echo "  make publish      - Publish to PyPI (requires credentials)"
	@echo ""

install:
	$(PIP) install -e .

install-dev:
	$(PIP) install -e ".[dev,yaml,clipboard]"

test:
	pytest tests/ -v --cov=promptcraft --cov-report=term-missing

lint:
	flake8 promptcraft/ --max-line-length=100 --extend-ignore=E203,W503
	mypy promptcraft/ --ignore-missing-imports

format:
	black promptcraft/ tests/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

build: clean
	$(PYTHON) -m build

publish: build
	$(PYTHON) -m twine upload dist/*

# Development shortcuts
run:
	$(PYTHON) -m promptcraft

shell:
	$(PYTHON) -i -c "from promptcraft.core import *"

# Testing specific components
test-core:
	pytest tests/test_core.py -v

test-cli:
	pytest tests/test_cli.py -v

# Coverage report
coverage:
	pytest tests/ --cov=promptcraft --cov-report=html
	@echo "Coverage report generated in htmlcov/"

# Documentation
docs:
	@echo "Documentation is in README.md"
	@cat README.md | head -100
