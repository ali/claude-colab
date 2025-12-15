#!/usr/bin/env python3
"""
Status line script for Claude Code Colab plugin.
Displays model, working directory, and Colab-specific info.
"""

import json
import os
import sys

try:
    # Read JSON input from stdin
    data = json.load(sys.stdin)

    model = data.get("model", {}).get("display_name", "unknown")
    cwd = data.get("cwd", os.getcwd())
    project_dir = data.get("workspace", {}).get("project_dir", cwd)

    # Shorten paths
    cwd_short = os.path.basename(cwd) if cwd != "/" else "/"
    project_short = os.path.basename(project_dir) if project_dir != "/" else "/"

    # Format status line with ANSI colors
    # Green for model, cyan for directory
    status = f"\033[32m{model}\033[0m | \033[36m{cwd_short}\033[0m"

    if cwd_short != project_short:
        status += f" (\033[33m{project_short}\033[0m)"

    # Add Colab indicator if in Colab
    if os.path.exists("/content") and os.environ.get("COLAB_RELEASE_TAG"):
        status += " | \033[35mColab\033[0m"

    print(status)

except Exception:
    # Fallback if JSON parsing fails
    cwd = os.getcwd()
    cwd_short = os.path.basename(cwd) if cwd != "/" else "/"
    print(f"Claude Code | {cwd_short}")
