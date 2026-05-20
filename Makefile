.PHONY: help install install-dev test lint clean build publish

# Default target
help:
	@echo "PromptCraft-CLI Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  install      Install the package"
	@echo "  install-dev  Install in development mode"
	@echo "  test         Run tests"
	@echo "  lint         Run linting"
	@echo "  clean        Clean build artifacts"
	@echo "  build        Build distribution packages"
	@echo "  publish      Publish to PyPI"

# Installation
install:
	pip install .

install-dev:
	pip install -e .

# Testing
test:
	python -m pytest tests/ -v

test-coverage:
	python -m pytest tests/ --cov=promptcraft --cov-report=html

# Linting
lint:
	python -m flake8 promptcraft/ --max-line-length=100
	python -m pylint promptcraft/ --disable=C,R

format:
	python -m black promptcraft/ --line-length=100

# Cleaning
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

# Building
build: clean
	python setup.py sdist bdist_wheel

# Publishing
publish: build
	twine upload dist/*

publish-test: build
	twine upload --repository testpypi dist/*

# Development
run:
	python -m promptcraft

dev:
	python -m promptcraft.cli

# Platform-specific builds
build-windows:
	pyinstaller --onefile --name promptcraft promptcraft/cli.py

build-macos:
	pyinstaller --onefile --name promptcraft promptcraft/cli.py

build-linux:
	pyinstaller --onefile --name promptcraft promptcraft/cli.py

# Documentation
docs:
	cd docs && make html

# Release
release: clean build
	@echo "Built release packages:"
	@ls -lh dist/
