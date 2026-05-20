# Contributing to PromptCraft CLI

Thank you for your interest in contributing to PromptCraft CLI! 🎉

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version)

### Suggesting Features

We welcome feature suggestions! Please open an issue with:
- A clear description of the feature
- Use cases and benefits
- Possible implementation approach (optional)

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting (`make test && make lint`)
5. Commit using [Conventional Commits](https://www.conventionalcommits.org/)
6. Push to your fork
7. Open a Pull Request

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build/process changes

Example:
```
feat(optimizer): add support for custom optimization rules

- Add config option for custom rules
- Implement rule parser
- Add tests

Closes #123
```

### Code Style

- Follow PEP 8
- Use Black for formatting (`make format`)
- Maximum line length: 100 characters
- Add docstrings for public functions

### Testing

- Write tests for new features
- Ensure all tests pass (`make test`)
- Aim for high code coverage

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/PromptCraft-CLI.git
cd PromptCraft-CLI

# Install in development mode
pip install -e ".[dev,yaml,clipboard]"

# Run tests
make test

# Run linting
make lint
```

## Questions?

Feel free to open an issue for any questions!

Thank you for contributing! 🚀
