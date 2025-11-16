"""Utility script to bootstrap a new Python project from this template.

The script assumes it is executed from the root of the cloned template
repository. It will:

1. Prompt the user for a new project name.
2. Rename the ``sample`` package directory under ``src/`` to the new name.
3. Update references to ``sample`` in the relevant source files and the
   ``pyproject.toml`` configuration.
4. Print a short success message.

The implementation performs a simple text replacement. It is sufficient for
the current template where the package name appears only in import statements,
the ``__init__`` docstring and the ``pyproject.toml`` metadata.
"""

from __future__ import annotations

import pathlib
import shutil
import sys
import subprocess


def _replace_in_file(file_path: pathlib.Path, old: str, new: str) -> None:
    """Replace all occurrences of *old* with *new* inside *file_path*.

    The file is read using UTF‑8 encoding, the replacement is performed on the
    whole text, and the file is written back with the same encoding.
    """
    try:
        text = file_path.read_text(encoding="utf-8")
    except OSError as exc:  # pragma: no cover – defensive programming
        print(f"Failed to read {file_path}: {exc}", file=sys.stderr)
        return
    new_text = text.replace(old, new)
    if new_text != text:
        try:
            file_path.write_text(new_text, encoding="utf-8")
        except OSError as exc:  # pragma: no cover
            print(f"Failed to write {file_path}: {exc}", file=sys.stderr)


def main() -> None:
    """Entry point that orchestrates the project bootstrap steps.

    The function is intentionally thin – each logical step is delegated to a
    dedicated helper function defined below. This improves readability and
    makes the script easier to test.
    """
    new_name = _prompt_project_name()
    _validate_project_name(new_name)

    # _rename_package now returns only ``root``, ``old_pkg_path`` and ``new_pkg_path``.
    root, old_pkg_path, new_pkg_path = _rename_package(new_name)

    _update_source_files(root, new_name, old_pkg_path.name, new_pkg_path)

    print(f"Project successfully renamed to '{new_name}'.")

    _setup_venv_and_install(root)

    _remove_git_dir(root)


def _prompt_project_name() -> str:
    """Prompt the user for a new project name and return the stripped value."""
    name = input("Enter the new project name (valid Python identifier): ").strip()
    if not name:
        print("Project name cannot be empty.", file=sys.stderr)
        sys.exit(1)
    return name


def _validate_project_name(name: str) -> None:
    """Validate that *name* is a valid Python identifier.

    Exits the script with an error message if the validation fails.
    """
    if not name.isidentifier():
        print(f"'{name}' is not a valid Python identifier.", file=sys.stderr)
        sys.exit(1)


def _rename_package(new_name: str) -> tuple[pathlib.Path, pathlib.Path, pathlib.Path]:
    """Rename the ``sample`` package directory to *new_name*.

    Returns a tuple ``(root, old_pkg_path, new_pkg_path)`` for later use.
    """
    root = pathlib.Path(__file__).resolve().parent
    src_dir = root / "src"
    old_pkg = "sample"
    old_pkg_path = src_dir / old_pkg
    new_pkg_path = src_dir / new_name

    if not old_pkg_path.is_dir():
        print(f"Expected package directory {old_pkg_path} does not exist.", file=sys.stderr)
        sys.exit(1)

    try:
        shutil.move(str(old_pkg_path), str(new_pkg_path))
    except OSError as exc:  # pragma: no cover
        print(f"Failed to rename package directory: {exc}", file=sys.stderr)
        sys.exit(1)

    return root, old_pkg_path, new_pkg_path


def _update_source_files(root: pathlib.Path, new_name: str, old_pkg: str, new_pkg_path: pathlib.Path) -> None:
    """Replace occurrences of the old package name with *new_name* in relevant files."""
    files_to_update = [
        root / "pyproject.toml",
        root / "README.md",
        new_pkg_path / "__init__.py",
        new_pkg_path / "main.py",
        new_pkg_path / "utils.py",
    ]

    for file_path in files_to_update:
        if file_path.is_file():
            _replace_in_file(file_path, old_pkg, new_name)


def _setup_venv_and_install(root: pathlib.Path) -> None:
    """Create a virtual environment in ``.venv`` and install the project editable."""
    venv_path = root / ".venv"
    if not venv_path.exists():
        print("Creating virtual environment...")
        try:
            subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
        except subprocess.CalledProcessError as exc:  # pragma: no cover
            print(f"Failed to create virtual environment: {exc}", file=sys.stderr)
            sys.exit(1)

    venv_python = venv_path / "bin" / "python"
    print("Installing project in editable mode...")
    try:
        subprocess.run([str(venv_python), "-m", "pip", "install", "-e", "."], cwd=str(root), check=True)
    except subprocess.CalledProcessError as exc:  # pragma: no cover
        print(f"Failed to install project: {exc}", file=sys.stderr)
        sys.exit(1)


def _remove_git_dir(root: pathlib.Path) -> None:
    """Delete the ``.git`` directory if it exists.

    This step is non‑fatal – failures are reported but do not abort the script.
    """
    git_dir = root / ".git"
    if git_dir.is_dir():
        try:
            shutil.rmtree(git_dir)
        except OSError as exc:  # pragma: no cover
            print(f"Failed to remove .git directory: {exc}", file=sys.stderr)


if __name__ == "__main__":
    main()
