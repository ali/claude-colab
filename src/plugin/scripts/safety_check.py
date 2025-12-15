#!/usr/bin/env python3
"""
PreToolUse safety hook for Claude Code in Google Colab.

Blocks or warns about dangerous commands that could:
- Delete critical system directories
- Kill the Colab session
- Accidentally delete Google Drive data

Exit codes:
- 0: Allow the command
- 2: Block with error message (non-zero = block)
"""

import json
import os
import re
import sys

# Patterns that should be BLOCKED (exit 2)
BLOCKED_PATTERNS = [
    # Delete root or home
    (r"rm\s+(-[rfvd]+\s+)*/([\s;|&]|$)", "Refusing to delete root directory /"),
    (r"rm\s+(-[rfvd]+\s+)*~([\s;|&/]|$)", "Refusing to delete home directory ~"),
    (r"rm\s+(-[rfvd]+\s+)*/\*", "Refusing to delete /*"),
    # Delete Google Drive
    (r"rm\s+(-[rfvd]+\s+)*/content/drive", "Refusing to delete Google Drive mount"),
    # Fork bombs and system killers
    (r":\(\)\s*\{\s*:\s*\|\s*:\s*&\s*\}\s*;", "Fork bomb detected"),
    (r"kill\s+(-\d+\s+)*(1|init)\b", "Refusing to kill init process"),
    # Dangerous dd commands
    (r"dd\s+.*of=/dev/(sd[a-z]|nvme|hd[a-z])", "Refusing to write directly to disk device"),
    # Chmod dangerous
    (r"chmod\s+(-[Rrf]+\s+)*777\s+/($|\s)", "Refusing chmod 777 on root"),
]

# Patterns that trigger a WARNING (printed but allowed)
WARN_PATTERNS = [
    (r"rm\s+(-[rfvd]+\s+)*/content(?!/drive)", "Warning: Deleting from /content workspace"),
    (r"pip\s+install\s+--user", "Warning: Installing packages with --user flag"),
]


def check_command(command: str) -> tuple[int, str | None]:
    """
    Check a command for dangerous patterns.

    Returns:
        (exit_code, message) - 0 for allow, 2 for block
    """
    # Check blocked patterns
    for pattern, message in BLOCKED_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return 2, message

    # Check warning patterns (print warning but allow)
    for pattern, message in WARN_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            print(f"\033[33m{message}\033[0m", file=sys.stderr)

    return 0, None


def main():
    """
    Read tool use from stdin and check for dangerous commands.

    Expected input format (JSON):
    {
        "tool_name": "Bash",
        "tool_input": {"command": "rm -rf /"}
    }
    """
    try:
        # Read input from stdin
        input_data = sys.stdin.read()
        if not input_data.strip():
            sys.exit(0)  # No input, allow

        data = json.loads(input_data)
        tool_name = data.get("tool_name", "")
        tool_input = data.get("tool_input", {})

        # Only check Bash commands
        if tool_name != "Bash":
            sys.exit(0)

        command = tool_input.get("command", "")
        if not command:
            sys.exit(0)

        exit_code, message = check_command(command)

        if exit_code != 0 and message:
            # Output as JSON for Claude Code to display
            result = {"status": "blocked", "message": message}
            print(json.dumps(result))

        sys.exit(exit_code)

    except json.JSONDecodeError:
        # If we can't parse input, allow (fail open)
        sys.exit(0)
    except Exception as e:
        # Log error but don't block
        print(f"Safety check error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
