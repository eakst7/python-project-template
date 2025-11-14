sample — minimal Python package scaffold

This is a minimal Python package scaffold using the "src/" layout and modern packaging (pyproject.toml + setuptools). It includes pytest for testing, mypy for type checking, and ruff for linting.

## Installation

Install the package in editable mode with dev dependencies:

    pip install -e ".[dev]"

## Running the CLI

After installation, run the package as a shell command:

    sample

This calls the `main()` entry point defined in `src/sample/__main__.py`.

## Development

Run tests:

    pytest -q

Run type checker:

    mypy src tests

Run linter:

    ruff check src tests

## Requirements

- Python 3.14+
- setuptools, wheel (for building)
- pytest, mypy, ruff (for development)

