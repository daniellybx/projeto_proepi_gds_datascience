"""Offer path discovery and normalization helpers for project scripts.

This module avoids hard-coded absolute paths and allows modules to run from
terminals, IDE, and CI contexts consistently.
"""

from __future__ import annotations

from pathlib import Path


def find_project_root(start: Path | None = None) -> Path:
    """Find project root by searching for canonical repository markers.

    Args:
        start (Path | None): Initial path to start the search from.

    Returns:
        Path: Absolute path to repository root.

    Example:
        >>> find_project_root()
    """
    base = (start or Path.cwd()).resolve()
    for candidate in [base, *base.parents]:
        markers = [candidate / "src", candidate / "notebooks", candidate / "requirements.txt"]
        if all(marker.exists() for marker in markers):
            return candidate
    raise FileNotFoundError(f"Could not locate repository root from: {base}")


def safe_filename(text: str, max_len: int = 120) -> str:
    """Convert arbitrary text to a safe filename token.

    Args:
        text (str): Raw text used as base name.
        max_len (int): Maximum resulting length.

    Returns:
        str: Sanitized filename-safe token.

    Example:
        >>> safe_filename("Dengue / Brasil")
    """
    clean = "".join(c if c.isalnum() or c in "-_" else "_" for c in str(text)).strip("_")
    return clean[:max_len] or "item"
