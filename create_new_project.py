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
    # Prompt for the new project name.
    new_name = input("Enter the new project name (valid Python identifier): ").strip()
    if not new_name:
        print("Project name cannot be empty.", file=sys.stderr)
        sys.exit(1)

    # Basic validation – the name must be a valid identifier.
    if not new_name.isidentifier():
        print(f"'{new_name}' is not a valid Python identifier.", file=sys.stderr)
        sys.exit(1)

    root = pathlib.Path(__file__).resolve().parent
    src_dir = root / "src"
    old_pkg = "sample"
    old_pkg_path = src_dir / old_pkg
    new_pkg_path = src_dir / new_name

    if not old_pkg_path.is_dir():
        print(f"Expected package directory {old_pkg_path} does not exist.", file=sys.stderr)
        sys.exit(1)

    # Rename the package directory.
    try:
        shutil.move(str(old_pkg_path), str(new_pkg_path))
    except OSError as exc:  # pragma: no cover
        print(f"Failed to rename package directory: {exc}", file=sys.stderr)
        sys.exit(1)

    # Files that may contain the package name.
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

    print(f"Project successfully renamed to '{new_name}'.")


if __name__ == "__main__":
    main()
