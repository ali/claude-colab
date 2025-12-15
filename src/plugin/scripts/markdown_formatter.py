#!/usr/bin/env python3
"""
PostToolUse hook for markdown formatting.
Auto-formats markdown files after Edit/Write operations.
"""

import os
import subprocess
import sys


def get_markdown_files():
    """Get list of markdown files from CLAUDE_FILE_PATHS environment variable."""
    file_paths = os.environ.get("CLAUDE_FILE_PATHS", "")
    if not file_paths:
        return []

    files = []
    for path in file_paths.split(":"):
        path = path.strip()
        if path and path.endswith(".md") and os.path.isfile(path):
            files.append(path)
    return files


def format_markdown_file(filepath):
    """Format a single markdown file using available formatter."""
    # Try to use prettier if available
    try:
        result = subprocess.run(
            ["prettier", "--write", filepath], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    # Fallback: basic formatting (trailing whitespace, final newline)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Remove trailing whitespace from lines
        lines = [line.rstrip() for line in content.splitlines()]

        # Ensure single final newline
        formatted = "\n".join(lines)
        if formatted and not formatted.endswith("\n"):
            formatted += "\n"

        # Only write if changed
        if formatted != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(formatted)
            return True
    except Exception:
        pass

    return False


def main():
    """Main hook entry point."""
    files = get_markdown_files()

    if not files:
        return 0

    formatted_count = 0
    for filepath in files:
        if format_markdown_file(filepath):
            formatted_count += 1

    if formatted_count > 0:
        print(f"Formatted {formatted_count} markdown file(s)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
